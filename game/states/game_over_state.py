"""
game/states/game_over_state.py
Pantalla de fin de partida (Game Over) al agotarse los puntos de vida.
Permite reintentar cargando el último guardado o volver al menú principal.
"""
import pygame
from game.states.base_state import BaseState
from game.settings import (
    VIRTUAL_WIDTH, VIRTUAL_HEIGHT, COLOR_UI_BORDER,
    COLOR_TEXT, COLOR_TEXT_GOLD, COLOR_HP_RED, COLOR_TEXT_MUTED
)
from game.save_manager import SaveManager
from game.audio import audio


class GameOverState(BaseState):
    """Pantalla de derrota."""

    def __init__(self, state_machine, fonts):
        super().__init__(state_machine)
        self.fonts = fonts
        self.options = [
            ("Reintentar (Cargar último guardado)", "retry"),
            ("Volver al Menú Principal", "menu")
        ]
        self.selected_idx = 0
        self.has_save = False

    def enter(self, **kwargs):
        self.has_save = SaveManager.save_exists()
        self.selected_idx = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected_idx = (self.selected_idx - 1) % len(self.options)
                audio.play("select")
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_idx = (self.selected_idx + 1) % len(self.options)
                audio.play("select")
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE, pygame.K_e):
                self._execute_option()

    def _execute_option(self):
        opt_key = self.options[self.selected_idx][1]
        audio.play("select")

        if opt_key == "retry":
            if self.has_save:
                save_data, _ = SaveManager.load_game()
                self.state_machine.change_state("play", load_data=save_data)
            else:
                self.state_machine.change_state("play")
        elif opt_key == "menu":
            self.state_machine.change_state("menu")

    def draw(self, surface):
        surface.fill((20, 10, 12))

        # Marco carmesí
        pygame.draw.rect(surface, (140, 30, 30), (14, 14, VIRTUAL_WIDTH - 28, VIRTUAL_HEIGHT - 28), 2)
        pygame.draw.rect(surface, (70, 15, 15), (18, 18, VIRTUAL_WIDTH - 36, VIRTUAL_HEIGHT - 36), 1)

        # Título de derrota
        title_surf = self.fonts["large"].render("HAS CAÍDO EN COMBATE", True, COLOR_HP_RED)
        surface.blit(title_surf, ((VIRTUAL_WIDTH - title_surf.get_width()) // 2, 60))

        sub_surf = self.fonts["small"].render("Las sombras han cubierto los valles de Brumavalle...", True, COLOR_TEXT_MUTED)
        surface.blit(sub_surf, ((VIRTUAL_WIDTH - sub_surf.get_width()) // 2, 90))

        # Opciones
        start_y = 135
        spacing = 24

        for idx, (label, _) in enumerate(self.options):
            is_sel = (idx == self.selected_idx)
            text = f"► {label} ◄" if is_sel else label
            color = COLOR_TEXT_GOLD if is_sel else COLOR_TEXT

            opt_surf = self.fonts["medium"].render(text, True, color)
            opt_x = (VIRTUAL_WIDTH - opt_surf.get_width()) // 2
            opt_y = start_y + idx * spacing

            if is_sel:
                sel_box = pygame.Rect(opt_x - 10, opt_y - 2, opt_surf.get_width() + 20, opt_surf.get_height() + 4)
                pygame.draw.rect(surface, (50, 20, 25), sel_box, border_radius=4)
                pygame.draw.rect(surface, (180, 50, 50), sel_box, 1, border_radius=4)

            surface.blit(opt_surf, (opt_x, opt_y))
