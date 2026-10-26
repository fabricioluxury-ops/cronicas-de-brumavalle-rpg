"""
game/states/play_state.py
Estado principal del juego: mundo abierto top-down, cámara dinámica, física de colisiones,
combate en tiempo real contra slimes y el Guardián de las Sombras, interacción con NPCs,
apertura de cofres, reclamo de la Llama Antigua y finalización de la misión.
"""
import pygame
from game.states.base_state import BaseState
from game.settings import (
    TILE_SIZE, KEY_ATTACK, KEY_INTERACT, KEY_INVENTORY,
    KEY_QUEST_LOG, KEY_PAUSE
)
from game.asset_loader import assets
from game.camera import Camera
from game.map_data import WorldMap
from game.entities.player import Player
from game.entities.npc import create_all_npcs
from game.entities.enemy import create_all_enemies
from game.save_manager import QuestManager, SaveManager
from game.ui.hud import HUD
from game.ui.dialogue_box import DialogueBox
from game.ui.inventory_view import InventoryView
from game.ui.quest_log_view import QuestLogView
from game.audio import audio


class PlayState(BaseState):
    """Controlador del ciclo de juego activo."""

    def __init__(self, state_machine, fonts):
        super().__init__(state_machine)
        self.fonts = fonts

        self.world_map = None
        self.camera = None
        self.player = None
        self.npcs = []
        self.enemies = []
        self.quest_manager = None

        self.hud = None
        self.dialogue_box = None
        self.inventory_view = None
        self.quest_log_view = None

        self.anim_tick = 0
        self.banner_message = ""
        self.banner_timer = 0

    def enter(self, load_data=None):
        """Inicializa una nueva partida o carga el estado guardado."""
        self.world_map = WorldMap(assets)
        self.camera = Camera(self.world_map.pixel_width, self.world_map.pixel_height)

        # Crear jugador y entidades por defecto
        # Spawn en la plaza del pueblo de Brumavalle (x=10, y=11)
        self.player = Player(10 * TILE_SIZE, 11 * TILE_SIZE, assets, name="Eric")
        self.npcs = create_all_npcs()
        self.enemies = create_all_enemies()
        self.quest_manager = QuestManager(0)

        # Interfaz de usuario
        self.hud = HUD(self.fonts["small"], self.fonts["medium"])
        self.dialogue_box = DialogueBox(self.fonts["medium"], self.fonts["small"])
        self.inventory_view = InventoryView(self.fonts["medium"], self.fonts["small"], assets)
        self.quest_log_view = QuestLogView(self.fonts["medium"], self.fonts["small"])

        self.anim_tick = 0
        self.banner_message = ""
        self.banner_timer = 0

        # Si se solicitó cargar una partida guardada
        if load_data:
            self._apply_save_data(load_data)

    def _apply_save_data(self, data):
        """Restaura todos los datos de la partida guardada."""
        try:
            p_data = data.get("player", {})
            self.player.name = p_data.get("name", "Eric")
            self.player.x = float(p_data.get("x", 10 * TILE_SIZE))
            self.player.y = float(p_data.get("y", 11 * TILE_SIZE))
            self.player.rect.x = int(self.player.x)
            self.player.rect.y = int(self.player.y)
            self.player.hp = p_data.get("hp", 100)
            self.player.max_hp = p_data.get("max_hp", 100)
            self.player.direction = p_data.get("direction", "down")
            if "inventory" in p_data:
                self.player.inventory = p_data["inventory"]

            q_data = data.get("quest", {})
            self.quest_manager.stage = q_data.get("stage", 0)

            w_data = data.get("world", {})
            if w_data.get("chest_opened"):
                self.world_map.chest_opened = True
                self.world_map.overlay_grid[6][28] = "chest_open"
            if w_data.get("relic_taken"):
                self.world_map.relic_taken = True

            e_data = data.get("enemies", {})
            for e in self.enemies:
                if e.id in e_data:
                    e.is_alive = e_data[e.id].get("is_alive", True)
                    e.hp = e_data[e.id].get("hp", e.max_hp)

            self.banner_message = "¡Partida cargada exitosamente!"
            self.banner_timer = 120
        except Exception as err:
            print(f"[Save] Error aplicando datos cargados: {err}")

    def handle_event(self, event):
        # 1. Si el inventario está abierto, recibe los eventos exclusivamente
        if self.inventory_view.active:
            self.inventory_view.handle_input(event, self.player)
            return

        # 2. Si el registro de misiones está abierto, recibe los eventos
        if self.quest_log_view.active:
            self.quest_log_view.handle_input(event)
            return

        # 3. Si el cuadro de diálogo está activo, avanzar con E o ENTER
        if self.dialogue_box.active:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_e, pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    self.dialogue_box.advance()
            return

        # 4. Controles principales de juego
        if event.type == pygame.KEYDOWN:
            # Pausa (ESC)
            if event.key in KEY_PAUSE:
                audio.play("select")
                self.state_machine.push_state("pause", play_state=self)
                return

            # Abrir/cerrar inventario (I)
            if event.key in KEY_INVENTORY:
                self.inventory_view.toggle()
                return

            # Abrir/cerrar registro de misiones (J)
            if event.key in KEY_QUEST_LOG:
                self.quest_log_view.toggle()
                return

            # Atacar con espada (ESPACIO)
            if event.key in KEY_ATTACK:
                self.player.trigger_attack()
                return

            # Interactuar con NPC o entorno (E)
            if event.key in KEY_INTERACT:
                self._handle_interaction()

    def _handle_interaction(self):
        """Gestiona la interacción con NPCs, cofres, altar de la reliquia y carteles."""
        # A. Verificar NPCs cercanos
        for npc in self.npcs:
            if npc.is_player_nearby(self.player.rect):
                has_relic = self.player.has_item("relic")
                lines = npc.get_dialogue_for_quest_stage(self.quest_manager.stage, has_relic=has_relic)
                portrait = assets.portraits.get(npc.portrait_key)

                def on_dialogue_finished(spoken_npc=npc):
                    # Avanzar misiones según el interlocutor
                    if spoken_npc.id == "elira" and self.quest_manager.stage == 0:
                        self.quest_manager.advance_to(1)
                        audio.play("quest")
                        self.banner_message = "¡Nuevo objetivo: Ve a las Ruinas de Kal-Drakor!"
                        self.banner_timer = 150
                    elif spoken_npc.id == "valeria" and self.player.has_item("relic"):
                        self.quest_manager.advance_to(4)
                        audio.play("quest")
                        # Transición a victoria al completar diálogo
                        self.state_machine.change_state("victory")

                self.dialogue_box.start_dialogue(npc.name, lines, portrait=portrait, on_complete=on_dialogue_finished)
                return

        # B. Verificar objetos interactuables en el mapa (cofre, altar, letrero)
        interaction_rect = self.player.get_interaction_rect()
        for item in self.world_map.interactables:
            if interaction_rect.colliderect(item["rect"]):
                item_type = item.get("type")

                if item_type == "sign":
                    self.dialogue_box.start_dialogue(item["name"], [item["text"]])
                    return

                elif item_type == "chest":
                    if not self.world_map.chest_opened:
                        self.world_map.open_chest(item)
                        audio.play("potion")
                        self.player.add_item({
                            "id": "potion",
                            "name": "Poción de Vida",
                            "desc": "Brebaje medicinal que restaura 40 puntos de salud.",
                            "type": "consumable",
                            "count": item.get("amount", 2),
                            "heal": 40
                        })
                        self.dialogue_box.start_dialogue("Cofre del Bosque", [
                            f"¡Has abierto el cofre antiguo!",
                            f"Encontraste {item.get('amount', 2)} Pociones de Vida."
                        ])
                    else:
                        self.dialogue_box.start_dialogue("Cofre del Bosque", ["El cofre ya está vacío."])
                    return

                elif item_type == "altar":
                    if self.player.has_item("relic"):
                        self.dialogue_box.start_dialogue("Altar de Kal-Drakor", ["El pedestal ahora descansa en calma."])
                    else:
                        # Verificar si el Guardián de las Sombras fue derrotado
                        boss = next((e for e in self.enemies if e.id == "boss_guardian"), None)
                        if boss and boss.is_alive:
                            self.dialogue_box.start_dialogue("Altar Sagrado", [
                                "Una barrera oscura sella el pedestal.",
                                "¡Debes derrotar al Guardián de las Sombras para disipar el sello!"
                            ])
                        else:
                            # Reclamar la Llama Antigua
                            self.world_map.remove_relic_from_altar()
                            self.player.add_item({
                                "id": "relic",
                                "name": "Reliquia de la Llama Antigua",
                                "desc": "El fuego sagrado ancestral que purifica las tinieblas de Brumavalle.",
                                "type": "key_item"
                            })
                            self.quest_manager.advance_to(3)
                            audio.play("quest")
                            self.dialogue_box.start_dialogue("Altar de Kal-Drakor", [
                                "¡Has recuperado la Reliquia de la Llama Antigua!",
                                "El fuego sagrado danza en tus manos con una calidez reconfortante.",
                                "Regresa de inmediato con la Guardiana Valeria en el pueblo de Brumavalle."
                            ])
                    return

    def update(self):
        # Si hay diálogo, inventario o registro abierto, pausar el movimiento del mundo
        if self.dialogue_box.active:
            return
        if self.inventory_view.active:
            self.inventory_view.update()
            return
        if self.quest_log_view.active:
            return

        # 1. Entrada de teclado continua para movimiento
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys, self.world_map.collision_rects)
        self.player.update()

        # 2. Combate: comprobar colisión de espada con enemigos
        if self.player.is_attacking and self.player.attack_hitbox:
            for enemy in self.enemies:
                if enemy.is_alive and self.player.attack_hitbox.colliderect(enemy.rect):
                    # Calcular retroceso lejos del jugador
                    edx = enemy.rect.centerx - self.player.rect.centerx
                    edy = enemy.rect.centery - self.player.rect.centery
                    dist = max(1.0, (edx**2 + edy**2)**0.5)
                    knock = ((edx / dist) * 12.0, (edy / dist) * 12.0)

                    killed = enemy.take_hit(self.player.attack_power, knock)
                    if killed:
                        if enemy.id == "boss_guardian":
                            audio.play("quest")
                            self.quest_manager.advance_to(2)
                            self.banner_message = "¡Guardián derrotado! Recupera la Llama Antigua del altar."
                            self.banner_timer = 180
                            # Soltar poción garantizada
                            self.player.add_item({
                                "id": "potion",
                                "name": "Poción de Vida",
                                "desc": "Brebaje medicinal que restaura 40 puntos de salud.",
                                "type": "consumable",
                                "count": 1,
                                "heal": 40
                            })
                        else:
                            # Slime derrotado
                            self.banner_message = f"¡{enemy.name} derrotado!"
                            self.banner_timer = 60

        # 3. Actualizar enemigos
        for enemy in self.enemies:
            enemy.update(self.player, self.world_map.collision_rects)

        # 4. Comprobar derrota del jugador (Game Over)
        if self.player.hp <= 0:
            audio.play("defeat")
            self.state_machine.change_state("game_over")
            return

        # 5. Actualizar cámara centrada en el jugador
        self.camera.update(self.player.rect)

        # 6. Actualizar animaciones ambientales (antorchas, agua)
        self.anim_tick += 1
        if self.anim_tick % 20 == 0:
            self.world_map.update_animations(self.anim_tick // 20)

        # 7. Actualizar temporizador de banner
        if self.banner_timer > 0:
            self.banner_timer -= 1
            if self.banner_timer == 0:
                self.banner_message = ""

    def draw(self, surface):
        # 1. Dibujar suelo del mundo
        self.world_map.draw_ground(surface, self.camera)

        # 2. Dibujar capa de obstáculos / edificios
        self.world_map.draw_overlay(surface, self.camera)

        # 3. Dibujar NPCs
        for npc in self.npcs:
            npc.draw(surface, self.camera, assets)
            if not self.dialogue_box.active and npc.is_player_nearby(self.player.rect):
                npc.draw_prompt(surface, self.camera, self.fonts["small"])

        # 4. Dibujar Enemigos
        for enemy in self.enemies:
            enemy.draw(surface, self.camera, assets)

        # 5. Dibujar Jugador
        self.player.draw(surface, self.camera)

        # 6. Dibujar Banner de evento / notificación
        if self.banner_message:
            b_surf = self.fonts["small"].render(self.banner_message, True, (255, 235, 120))
            bw = b_surf.get_width() + 16
            bh = 18
            bx = (surface.get_width() - bw) // 2
            by = 38
            pygame.draw.rect(surface, (16, 20, 28, 220), (bx, by, bw, bh), border_radius=4)
            pygame.draw.rect(surface, (241, 196, 15), (bx, by, bw, bh), 1, border_radius=4)
            surface.blit(b_surf, (bx + 8, by + 3))

        # 7. Dibujar HUD principal
        self.hud.draw(surface, self.player, self.quest_manager)

        # 8. Dibujar Ventana de diálogo si está activa
        if self.dialogue_box.active:
            self.dialogue_box.draw(surface)

        # 9. Dibujar Inventario si está abierto
        if self.inventory_view.active:
            self.inventory_view.draw(surface, self.player)

        # 10. Dibujar Diario de misiones si está abierto
        if self.quest_log_view.active:
            self.quest_log_view.draw(surface, self.quest_manager)
