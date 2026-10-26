"""
test_game.py
Batería de pruebas automatizadas y comprobación de integridad para
"Crónicas de Brumavalle: La Llama Antigua".
Se puede ejecutar sin pantalla gráfica (Headless / CI).
"""
import os
import sys
import tempfile
import unittest

# Configurar modo headless para Pygame
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

# Agregar ruta al path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import pygame
from game.asset_loader import AssetLoader
from game.entities.player import Player
from game.entities.npc import create_all_npcs
from game.entities.enemy import create_all_enemies, Enemy
from game.map_data import WorldMap
from game.save_manager import QuestManager, SaveManager
from game.states.state_machine import StateMachine
from game.states.loading_state import LoadingState
from game.states.menu_state import MenuState
from game.states.intro_state import IntroState
from game.states.play_state import PlayState
from game.states.pause_state import PauseState
from game.states.options_state import OptionsState
from game.states.credits_state import CreditsState
from game.states.game_over_state import GameOverState
from game.states.victory_state import VictoryState


class TestBrumavalleRPG(unittest.TestCase):
    """Pruebas unitarias de mecánicas, estados, datos y estabilidad."""

    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.font.init()
        cls.dummy_screen = pygame.display.set_mode((480, 270))
        cls.assets = AssetLoader()
        cls.assets.initialize_all()
        cls.fonts = {
            "small": pygame.font.Font(None, 14),
            "medium": pygame.font.Font(None, 18),
            "large": pygame.font.Font(None, 24),
        }

    def test_01_asset_generation(self):
        """Verifica que todos los sprites, tiles, iconos y retratos se generen correctamente."""
        self.assertIn("grass", self.assets.tiles)
        self.assertIn("cobblestone", self.assets.tiles)
        self.assertIn("stone_wall", self.assets.tiles)
        self.assertIn("altar", self.assets.tiles)
        self.assertIn("player", self.assets.sprites)
        self.assertIn("npc_valeria", self.assets.sprites)
        self.assertIn("npc_torin", self.assets.sprites)
        self.assertIn("npc_elira", self.assets.sprites)
        self.assertIn("enemy_slime", self.assets.sprites)
        self.assertIn("enemy_guardian", self.assets.sprites)
        self.assertIn("sword", self.assets.icons)
        self.assertIn("potion", self.assets.icons)
        self.assertIn("relic", self.assets.icons)
        self.assertIn("valeria", self.assets.portraits)
        self.assertIn("player", self.assets.portraits)

    def test_02_player_mechanics(self):
        """Verifica movimiento, colisiones, ataque y uso de pociones del jugador."""
        player = Player(100, 100, self.assets, name="Eric")
        self.assertEqual(player.name, "Eric")
        self.assertEqual(player.hp, 100)

        # Prueba de daño
        damaged = player.take_damage(25)
        self.assertTrue(damaged)
        self.assertEqual(player.hp, 75)

        # Prueba de uso de poción
        success, msg = player.use_potion()
        self.assertTrue(success)
        self.assertGreater(player.hp, 75)

        # Prueba de activación de ataque con espada
        attacked = player.trigger_attack()
        self.assertTrue(attacked)
        self.assertTrue(player.is_attacking)
        self.assertIsNotNone(player.attack_hitbox)

    def test_03_quest_system(self):
        """Verifica la progresión por etapas de la misión principal."""
        qm = QuestManager(0)
        self.assertEqual(qm.stage, 0)
        info0 = qm.get_current_info()
        self.assertIn("Sabia Elira", info0["target"])

        # Avanzar a etapa 1 (Ruinas)
        qm.advance_to(1)
        self.assertEqual(qm.stage, 1)

        # Avanzar a etapa 4 (Victoria)
        qm.advance_to(4)
        self.assertTrue(qm.is_completed())

    def test_04_save_and_load_system(self):
        """Verifica la persistencia de datos en JSON y manejo ante archivos corruptos."""
        player = Player(80, 90, self.assets, name="Eric")
        player.hp = 65
        qm = QuestManager(1)
        world_map = WorldMap(self.assets)
        enemies = create_all_enemies()

        # Guardar partida
        saved, msg = SaveManager.save_game(player, qm, world_map, enemies)
        self.assertTrue(saved)
        self.assertTrue(SaveManager.save_exists())

        # Cargar partida
        data, load_msg = SaveManager.load_game()
        self.assertIsNotNone(data)
        self.assertEqual(data["player"]["hp"], 65)
        self.assertEqual(data["quest"]["stage"], 1)

        # Prueba de resistencia ante JSON corrupto
        save_file = os.path.join(BASE_DIR, "data", "savegame.json")
        with open(save_file, "w", encoding="utf-8") as f:
            f.write("{ corrupt_json: [invalid syntax")
        corrupt_data, error_msg = SaveManager.load_game()
        self.assertIsNone(corrupt_data)
        self.assertIn("corrupto", error_msg.lower())

        # Limpiar archivo temporal corrupto para pruebas posteriores
        if os.path.exists(save_file):
            os.remove(save_file)

    def test_05_npcs_and_enemies(self):
        """Verifica la creación y comportamiento de NPCs y enemigos."""
        npcs = create_all_npcs()
        self.assertEqual(len(npcs), 3)
        valeria = next(n for n in npcs if n.id == "valeria")
        torin = next(n for n in npcs if n.id == "torin")
        elira = next(n for n in npcs if n.id == "elira")
        self.assertIsNotNone(valeria)
        self.assertIsNotNone(torin)
        self.assertIsNotNone(elira)

        enemies = create_all_enemies()
        self.assertGreaterEqual(len(enemies), 4)
        boss = next(e for e in enemies if e.id == "boss_guardian")
        self.assertIsNotNone(boss)

        # Dañar al boss
        initial_hp = boss.hp
        killed = boss.take_hit(25)
        self.assertFalse(killed)
        self.assertEqual(boss.hp, initial_hp - 25)

    def test_06_state_machine_flow(self):
        """Simula transiciones de estados del juego sin generar errores."""
        sm = StateMachine()
        sm.register("loading", LoadingState(sm, self.fonts))
        sm.register("menu", MenuState(sm, self.fonts))
        sm.register("intro", IntroState(sm, self.fonts))
        sm.register("play", PlayState(sm, self.fonts))
        sm.register("pause", PauseState(sm, self.fonts))
        sm.register("options", OptionsState(sm, self.fonts))
        sm.register("credits", CreditsState(sm, self.fonts))
        sm.register("game_over", GameOverState(sm, self.fonts))
        sm.register("victory", VictoryState(sm, self.fonts))

        # Inicializar y avanzar varios ticks
        sm.change_state("loading")
        self.assertEqual(sm.current_state.__class__.__name__, "LoadingState")
        for _ in range(5):
            sm.update()
            sm.draw(self.dummy_screen)

        sm.change_state("menu")
        self.assertEqual(sm.current_state.__class__.__name__, "MenuState")
        sm.update()
        sm.draw(self.dummy_screen)

        sm.change_state("play")
        self.assertEqual(sm.current_state.__class__.__name__, "PlayState")
        for _ in range(30):
            sm.update()
            sm.draw(self.dummy_screen)

        # Pausa superpuesta
        sm.push_state("pause", play_state=sm.current_state)
        self.assertEqual(sm.current_state.__class__.__name__, "PauseState")
        sm.draw(self.dummy_screen)
        sm.pop_state()
        self.assertEqual(sm.current_state.__class__.__name__, "PlayState")

        # Pantalla de victoria
        sm.change_state("victory")
        self.assertEqual(sm.current_state.__class__.__name__, "VictoryState")
        sm.draw(self.dummy_screen)


if __name__ == "__main__":
    unittest.main()
