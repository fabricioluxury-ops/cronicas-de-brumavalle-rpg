"""
game/entities/enemy.py
Inteligencia artificial, combate y estados de los enemigos:
- Slimes Sombríos: Criaturas errantes en el Bosque Susurrante.
- Guardián Sombrío: Poderoso guerrero oscuro que custodia el altar de las Ruinas de Kal-Drakor.
"""
import random
import pygame
from game.settings import TILE_SIZE, COLOR_HP_RED, COLOR_HP_GREEN, COLOR_BLACK
from game.audio import audio


class Enemy:
    """Clase base de enemigo con patrulla, detección, persecución, daño y retroceso."""

    def __init__(self, enemy_id, name, x, y, enemy_type="slime", max_hp=40, attack_power=10, speed=1.0):
        self.id = enemy_id
        self.name = name
        self.enemy_type = enemy_type
        self.x = float(x)
        self.y = float(y)
        self.origin_x = float(x)
        self.origin_y = float(y)
        self.width = 14
        self.height = 14
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)

        self.max_hp = max_hp
        self.hp = max_hp
        self.attack_power = attack_power
        self.speed = speed
        self.aggro_radius = 80 if enemy_type == "slime" else 110
        self.attack_cooldown = 0
        self.hurt_timer = 0
        self.is_alive = True

        # Animación y patrulla aleatoria
        self.anim_timer = 0
        self.anim_frame = 0
        self.patrol_timer = random.randint(30, 90)
        self.patrol_dir = (0, 0)

    def update(self, player, collision_rects):
        """Actualiza la IA: persigue al jugador si entra en rango; si no, patrulla pacíficamente."""
        if not self.is_alive:
            return

        if self.hurt_timer > 0:
            self.hurt_timer -= 1

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Animación
        self.anim_timer += 1
        if self.anim_timer >= 15:
            self.anim_timer = 0
            self.anim_frame = (self.anim_frame + 1) % 2

        # Distancia al jugador
        dx_to_player = player.rect.centerx - self.rect.centerx
        dy_to_player = player.rect.centery - self.rect.centery
        dist = (dx_to_player ** 2 + dy_to_player ** 2) ** 0.5

        # Movimiento
        move_x, move_y = 0.0, 0.0

        if dist < self.aggro_radius and dist > 4:
            # Perseguir al jugador
            move_x = (dx_to_player / dist) * self.speed
            move_y = (dy_to_player / dist) * self.speed
        else:
            # Patrulla errática cerca del punto de origen
            self.patrol_timer -= 1
            if self.patrol_timer <= 0:
                self.patrol_timer = random.randint(40, 100)
                # Volver al origen si se alejó demasiado
                dist_from_origin = ((self.x - self.origin_x)**2 + (self.y - self.origin_y)**2)**0.5
                if dist_from_origin > 60:
                    ox = self.origin_x - self.x
                    oy = self.origin_y - self.y
                    od = max(1.0, (ox**2 + oy**2)**0.5)
                    self.patrol_dir = (ox / od, oy / od)
                else:
                    self.patrol_dir = random.choice([(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)])

            move_x = self.patrol_dir[0] * (self.speed * 0.5)
            move_y = self.patrol_dir[1] * (self.speed * 0.5)

        # Aplicar movimiento con resolución de obstáculos
        if move_x != 0:
            self.x += move_x
            self.rect.x = int(self.x)
            for obs in collision_rects:
                if self.rect.colliderect(obs):
                    if move_x > 0:
                        self.rect.right = obs.left
                    else:
                        self.rect.left = obs.right
                    self.x = float(self.rect.x)

        if move_y != 0:
            self.y += move_y
            self.rect.y = int(self.y)
            for obs in collision_rects:
                if self.rect.colliderect(obs):
                    if move_y > 0:
                        self.rect.bottom = obs.top
                    else:
                        self.rect.top = obs.bottom
                    self.y = float(self.rect.y)

        # Atacar al jugador si colisiona con él
        if self.rect.colliderect(player.rect) and self.attack_cooldown <= 0:
            # Calcular vector de retroceso para empujar al jugador
            p_dx = player.rect.centerx - self.rect.centerx
            p_dy = player.centery if hasattr(player, 'centery') else (player.rect.centery - self.rect.centery)
            p_dist = max(1.0, (p_dx**2 + p_dy**2)**0.5)
            knockback = ((p_dx / p_dist) * 8.0, (p_dy / p_dist) * 8.0)
            if player.take_damage(self.attack_power, knockback):
                self.attack_cooldown = 40

    def take_hit(self, damage, knockback_vector=None):
        """Recibe daño del ataque de la espada y aplica retroceso."""
        if not self.is_alive or self.hurt_timer > 0:
            return False

        self.hp -= damage
        self.hurt_timer = 12
        audio.play("hit")

        if knockback_vector:
            kx, ky = knockback_vector
            self.x += kx
            self.y += ky
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)

        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False
            return True  # Murió con este golpe
        return False

    def draw(self, surface, camera, asset_loader):
        """Dibuja el sprite del enemigo y su mini barra de vida si ha recibido daño."""
        if not self.is_alive:
            return

        screen_pos = camera.apply_pos(self.rect.x, self.rect.y)

        # Si está herido, parpadea en blanco/rojo
        if self.hurt_timer > 0 and (self.hurt_timer // 2) % 2 == 1:
            tint_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            tint_surf.fill((255, 255, 255))
            surface.blit(tint_surf, screen_pos, special_flags=pygame.BLEND_RGB_ADD)
            return

        if self.enemy_type == "slime":
            sprites = asset_loader.sprites.get("enemy_slime", [])
            if sprites:
                surface.blit(sprites[self.anim_frame % len(sprites)], screen_pos)
        elif self.enemy_type == "guardian":
            sprite = asset_loader.sprites.get("enemy_guardian")
            if sprite:
                surface.blit(sprite, screen_pos)

        # Dibujar mini barra de salud si está herido
        if self.hp < self.max_hp:
            bar_w = 16
            bar_h = 3
            bx = screen_pos[0] - 1
            by = screen_pos[1] - 5
            fill_w = int((self.hp / self.max_hp) * bar_w)
            pygame.draw.rect(surface, COLOR_BLACK, (bx, by, bar_w, bar_h))
            pygame.draw.rect(surface, COLOR_HP_RED, (bx, by, bar_w, bar_h))
            pygame.draw.rect(surface, COLOR_HP_GREEN, (bx, by, fill_w, bar_h))


def create_all_enemies():
    """Genera slimes en el bosque y el Guardián en las Ruinas de Kal-Drakor."""
    enemies = []

    # 1. Slimes Sombríos en el Bosque Susurrante
    slime_spawns = [
        ("slime_1", "Slime Sombrío", 26 * TILE_SIZE, 11 * TILE_SIZE),
        ("slime_2", "Slime Sombrío", 34 * TILE_SIZE, 19 * TILE_SIZE),
        ("slime_3", "Slime Sombrío", 28 * TILE_SIZE, 24 * TILE_SIZE),
        ("slime_4", "Slime Sombrío", 38 * TILE_SIZE, 26 * TILE_SIZE),
    ]
    for eid, name, ex, ey in slime_spawns:
        enemies.append(Enemy(
            enemy_id=eid,
            name=name,
            x=ex,
            y=ey,
            enemy_type="slime",
            max_hp=40,
            attack_power=8,
            speed=0.9
        ))

    # 2. Miniboss: Guardián Sombrío en la antecámara del altar de Kal-Drakor
    boss_guardian = Enemy(
        enemy_id="boss_guardian",
        name="Guardián de las Sombras",
        x=50 * TILE_SIZE,
        y=11 * TILE_SIZE,
        enemy_type="guardian",
        max_hp=90,
        attack_power=14,
        speed=1.1
    )
    enemies.append(boss_guardian)

    return enemies
