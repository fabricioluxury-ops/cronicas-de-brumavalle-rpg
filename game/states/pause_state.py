"""
game/states/pause_state.py
Menú de pausa superpuesto al juego activo (tecla ESC).
Permite reanudar, guardar la partida en disco, ajustar opciones, volver al menú o salir.
"""
import sys
import pygame
from game.states.base_state import BaseState
from game.settings import (
    VIRTUAL_WIDTH, VIRTUAL_HEIGHT, COLOR_UI_BORDER,
    COLOR_TEXT, COLOR_TEXT_GOLD, COLOR_TEXT_MUTED
)
from game.save_manager import SaveManager
from game.audio import audio


class PauseState(BaseState):
    """Menú modal de pausa."""

    def __init__(self, state_machine, fonts):
        super().__init__(state_machine)
        self.fonts = fonts
        self.play_state = None
        self.options = [
            ("Continuar Aventura", "resume"),
            ("Guardar Partida", "save"),
            ("Opciones y Controles", "options"),
            ("Volver al Menú Principal", "menu"),
            ("Salir del Juego", "exit")
        ]
        self.selected_idx = 0
        self.status_msg = ""
        self.status_timer = 0

        self.width = 220
        self.height = 160
        self.x = (VIRTUAL_WIDTH - self.width) // 2
        self.y = (VIRTUAL_HEIGHT - self.height) // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def enter(self, play_state=None, **kwargs):
        self.play_state = play_state
        self.selected_idx = 0
        self.status_msg = ""
        self.status_timer = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE,):
                audio.play("select")
                self.state_machine.pop_state()
            elif event.key in (pygame.K_UP, pygame.K_w):
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

        if opt_key == "resume":
            self.state_machine.pop_state()
        elif opt_key == "save":
            if self.play_state:
                success, msg = SaveManager.save_game(
                    self.play_state.player,
                    self.play_state.quest_manager,
                    self.play_state.world_map,
                    self.play_state.enemies
                )
                self.status_msg = "¡Partida guardada!" if success else "Error al guardar"
                self.status_timer = 120
        elif opt_key == "options":
            self.state_machine.push_state("options")
        elif opt_key == "menu":
            self.state_machine.change_state("menu")
        elif opt_key == "exit":
            pygame.quit()
            sys.exit(0)

    def update(self):
        if self.status_timer > 0:
            self.status_timer -= 1
            if self.status_timer == 0:
                self.status_msg = ""

    def draw(self, surface):
        # 1. Capa oscura semitransparente sobre el juego pausado
        backdrop = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
        backdrop.fill((10, 12, 16, 175))
        surface.blit(backdrop, (0, 0))

        # 2. Panel central
        panel = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        panel.fill((20, 24, 34, 245))
        surface.blit(panel, (self.x, self.y))
        pygame.draw.rect(surface, COLOR_UI_BORDER, self.rect, 2)
        pygame.draw.rect(surface, (100, 75, 35), self.rect.inflate(-4, -4), 1)

        # 3. Título de pausa
        title_surf = self.fonts["large"].render("PAUSA", True, COLOR_TEXT_GOLD)
        surface.blit(title_surf, ((VIRTUAL_WIDTH - title_surf.get_width()) // 2, self.y + 10))

        # 4. Opciones
        start_y = self.y + 36
        spacing = 20

        for idx, (label, _) in enumerate(self.options):
            is_sel = (idx == self.selected_idx)
            text = f"► {label}" if is_sel else label
            color = COLOR_TEXT_GOLD if is_sel else COLOR_TEXT

            opt_surf = self.fonts["small"].render(text, True, color)
            opt_x = self.x + 22
            opt_y = start_y + idx * spacing

            if is_sel:
                sel_box = pygame.Rect(opt_x - 6, opt_y - 2, self.width - 32, 16)
                pygame.draw.rect(surface, (40, 50, 68), sel_box, border_radius=3)
                pygame.draw.rect(surface, COLOR_UI_BORDER, sel_box, 1, border_radius=3)

            surface.blit(opt_surf, (opt_x, opt_y))

        # 5. Mensaje de estado (guardado)
        if self.status_msg:
            msg_surf = self.fonts["small"].render(self.status_msg, True, (46, 204, 113))
            surface.blit(msg_surf, ((VIRTUAL_WIDTH - msg_surf.get_width()) // 2, self.y + self.height - 18))
