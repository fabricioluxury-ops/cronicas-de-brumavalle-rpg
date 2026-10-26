"""
game/entities/player.py
Control y comportamiento del Personaje Principal (Eric).
Maneja movimiento 4 direcciones, animaciones, colisiones con entorno,
ataque de espada con arco visual, vida, inventario e interacción.
"""
import pygame
from game.settings import (
    TILE_SIZE, KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT,
    KEY_ATTACK, COLOR_WHITE
)
from game.audio import audio


class Player:
    """Clase del héroe jugable de Brumavalle."""

    def __init__(self, x, y, asset_loader, name="Eric"):
        self.name = name
        self.assets = asset_loader

        # Posición y dimensiones físicas (hitbox ajustada para colisión precisa)
        self.x = float(x)
        self.y = float(y)
        self.width = 14
        self.height = 14
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)

        # Atributos de movimiento
        self.speed = 2.0
        self.direction = "down"
        self.moving = False
        self.anim_timer = 0
        self.anim_frame = 0

        # Atributos de combate
        self.max_hp = 100
        self.hp = 100
        self.attack_power = 25
        self.is_attacking = False
        self.attack_timer = 0
        self.attack_duration = 14  # Frames de duración del tajo
        self.attack_cooldown = 0
        self.attack_hitbox = None
        self.hurt_invincible_timer = 0

        # Inventario inicial
        self.inventory = [
            {
                "id": "sword",
                "name": "Espada de Acero de Brumavalle",
                "desc": "Espada forjada por el herrero Torin. Daño base: 25.",
                "type": "weapon",
                "equipped": True,
            },
            {
                "id": "potion",
                "name": "Poción de Vida",
                "desc": "Brebaje medicinal que restaura 40 puntos de salud.",
                "type": "consumable",
                "count": 2,
                "heal": 40,
            }
        ]

    def handle_input(self, keys, collision_rects):
        """Procesa las teclas de dirección y movimiento con resolución de colisiones por eje."""
        if self.is_attacking:
            return  # Queda fijo brevemente durante la animación de ataque

        dx = 0.0
        dy = 0.0

        if any(keys[k] for k in KEY_UP if k < len(keys)):
            dy -= self.speed
            self.direction = "up"
        if any(keys[k] for k in KEY_DOWN if k < len(keys)):
            dy += self.speed
            self.direction = "down"
        if any(keys[k] for k in KEY_LEFT if k < len(keys)):
            dx -= self.speed
            self.direction = "left"
        if any(keys[k] for k in KEY_RIGHT if k < len(keys)):
            dx += self.speed
            self.direction = "right"

        # Normalizar movimiento diagonal para mantener velocidad constante
        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        self.moving = (dx != 0 or dy != 0)

        # Mover en eje X y verificar colisiones
        if dx != 0:
            self.x += dx
            self.rect.x = int(self.x)
            for obstacle in collision_rects:
                if self.rect.colliderect(obstacle):
                    if dx > 0:
                        self.rect.right = obstacle.left
                    elif dx < 0:
                        self.rect.left = obstacle.right
                    self.x = float(self.rect.x)

        # Mover en eje Y y verificar colisiones
        if dy != 0:
            self.y += dy
            self.rect.y = int(self.y)
            for obstacle in collision_rects:
                if self.rect.colliderect(obstacle):
                    if dy > 0:
                        self.rect.bottom = obstacle.top
                    elif dy < 0:
                        self.rect.top = obstacle.bottom
                    self.y = float(self.rect.y)

        # Actualizar animación de caminata
        if self.moving:
            self.anim_timer += 1
            if self.anim_timer >= 8:
                self.anim_timer = 0
                self.anim_frame = (self.anim_frame + 1) % 3
        else:
            self.anim_frame = 0

    def trigger_attack(self):
        """Inicia el ataque con espada si no está en enfriamiento."""
        if self.attack_cooldown <= 0 and not self.is_attacking:
            self.is_attacking = True
            self.attack_timer = self.attack_duration
            self.attack_cooldown = 22
            audio.play("attack")
            self._generate_attack_hitbox()
            return True
        return False

    def _generate_attack_hitbox(self):
        """Crea el área de daño del tajo frente al jugador según su dirección."""
        reach = 18
        if self.direction == "down":
            self.attack_hitbox = pygame.Rect(self.rect.x - 4, self.rect.bottom, self.rect.width + 8, reach)
        elif self.direction == "up":
            self.attack_hitbox = pygame.Rect(self.rect.x - 4, self.rect.top - reach, self.rect.width + 8, reach)
        elif self.direction == "left":
            self.attack_hitbox = pygame.Rect(self.rect.left - reach, self.rect.y - 4, reach, self.rect.height + 8)
        elif self.direction == "right":
            self.attack_hitbox = pygame.Rect(self.rect.right, self.rect.y - 4, reach, self.rect.height + 8)

    def update(self):
        """Actualiza temporizadores de ataque y períodos de invulnerabilidad."""
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if self.is_attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.is_attacking = False
                self.attack_hitbox = None

        if self.hurt_invincible_timer > 0:
            self.hurt_invincible_timer -= 1

    def take_damage(self, amount, knockback_vector=None):
        """Aplica daño al jugador y retroceso físico si no es invulnerable."""
        if self.hurt_invincible_timer > 0:
            return False

        self.hp = max(0, self.hp - amount)
        self.hurt_invincible_timer = 35  # Frames de invulnerabilidad tras ser golpeado
        audio.play("hit")

        if knockback_vector:
            kx, ky = knockback_vector
            self.x += kx
            self.y += ky
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)

        return True

    def use_potion(self):
        """Usa una poción de vida del inventario si la salud no está completa."""
        if self.hp >= self.max_hp:
            return False, "¡Tu salud ya está al máximo!"

        potion_item = next((i for i in self.inventory if i.get("id") == "potion"), None)
        if potion_item and potion_item.get("count", 0) > 0:
            heal_amount = potion_item.get("heal", 40)
            self.hp = min(self.max_hp, self.hp + heal_amount)
            potion_item["count"] -= 1
            audio.play("potion")
            return True, f"Recuperaste {heal_amount} PV. Vida actual: {self.hp}/{self.max_hp}."
        return False, "No tienes pociones disponibles."

    def add_item(self, item_dict):
        """Añade un objeto o incrementa su cantidad si es apilable."""
        existing = next((i for i in self.inventory if i.get("id") == item_dict.get("id")), None)
        if existing and "count" in existing:
            existing["count"] += item_dict.get("count", 1)
        else:
            self.inventory.append(item_dict)

    def has_item(self, item_id):
        """Verifica si el jugador posee un ítem en su inventario."""
        return any(i.get("id") == item_id for i in self.inventory)

    def get_interaction_rect(self):
        """Devuelve un rectángulo de detección frente al jugador para interactuar con E."""
        reach = 14
        if self.direction == "down":
            return pygame.Rect(self.rect.x, self.rect.bottom, self.rect.width, reach)
        elif self.direction == "up":
            return pygame.Rect(self.rect.x, self.rect.top - reach, self.rect.width, reach)
        elif self.direction == "left":
            return pygame.Rect(self.rect.left - reach, self.rect.y, reach, self.rect.height)
        elif self.direction == "right":
            return pygame.Rect(self.rect.right, self.rect.y, reach, self.rect.height)
        return self.rect

    def draw(self, surface, camera):
        """Dibuja el sprite del jugador con parpadeo al estar herido y arco de tajo."""
        # Parpadeo de invulnerabilidad
        if self.hurt_invincible_timer > 0 and (self.hurt_invincible_timer // 4) % 2 == 1:
            return

        screen_pos = camera.apply_pos(self.rect.x, self.rect.y)

        # Seleccionar frame de animación
        dir_sprites = self.assets.sprites["player"].get(self.direction, [])
        if dir_sprites:
            sprite = dir_sprites[self.anim_frame % len(dir_sprites)]
            # Compensar un poco la posición para que el sprite 16x16 cuadre con la hitbox de 14x14
            surface.blit(sprite, (screen_pos[0] - 1, screen_pos[1] - 2))

        # Dibujar efecto visual del tajo de la espada
        if self.is_attacking and self.attack_hitbox:
            hb = camera.apply(self.attack_hitbox)
            # Dibujar arco curvo de tajo luminoso
            progress = (self.attack_duration - self.attack_timer) / self.attack_duration
            if self.direction == "down":
                pygame.draw.arc(surface, COLOR_WHITE, hb, 3.14, 6.28, 2)
            elif self.direction == "up":
                pygame.draw.arc(surface, COLOR_WHITE, hb, 0, 3.14, 2)
            elif self.direction == "left":
                pygame.draw.arc(surface, COLOR_WHITE, hb, 1.57, 4.71, 2)
            elif self.direction == "right":
                pygame.draw.arc(surface, COLOR_WHITE, hb, 4.71, 1.57, 2)
