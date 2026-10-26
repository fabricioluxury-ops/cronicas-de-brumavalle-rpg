"""
game/states/menu_state.py
Menú Principal con navegación completa por teclado y opciones funcionales:
Nueva Partida, Continuar, Opciones, Créditos y Salir.
"""
import sys
import pygame
from game.states.base_state import BaseState
from game.settings import (
    VIRTUAL_WIDTH, VIRTUAL_HEIGHT, COLOR_UI_BORDER,
    COLOR_TEXT, COLOR_TEXT_GOLD, COLOR_TEXT_MUTED, TITLE, SUBTITLE, AUTHOR
)
from game.save_manager import SaveManager
from game.audio import audio


class MenuState(BaseState):
    """Menú principal del juego."""

    def __init__(self, state_machine, fonts):
        super().__init__(state_machine)
        self.fonts = fonts
        self.options = [
            ("Nueva Partida", "new_game"),
            ("Continuar", "continue"),
            ("Opciones", "options"),
            ("Créditos", "credits"),
            ("Salir", "exit")
        ]
        self.selected_idx = 0
        self.notice_msg = ""
        self.notice_timer = 0
        self.has_save = False

    def enter(self, **kwargs):
        self.has_save = SaveManager.save_exists()
        self.notice_msg = ""
        self.notice_timer = 0
        # Si hay partida guardada, podemos sugerir 'Continuar' o mantener 'Nueva Partida'
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

        if opt_key == "new_game":
            # Iniciar pantalla narrativa introductoria
            self.state_machine.change_state("intro")
        elif opt_key == "continue":
            if SaveManager.save_exists():
                save_data, msg = SaveManager.load_game()
                if save_data:
                    self.state_machine.change_state("play", load_data=save_data)
                else:
                    self.notice_msg = msg
                    self.notice_timer = 150
            else:
                self.notice_msg = "No hay partida guardada. Selecciona 'Nueva Partida'."
                self.notice_timer = 150
        elif opt_key == "options":
            self.state_machine.push_state("options")
        elif opt_key == "credits":
            self.state_machine.push_state("credits")
        elif opt_key == "exit":
            pygame.quit()
            sys.exit(0)

    def update(self):
        if self.notice_timer > 0:
            self.notice_timer -= 1
            if self.notice_timer == 0:
                self.notice_msg = ""

    def draw(self, surface):
        surface.fill((16, 20, 28))

        # Marco decorativo estilo pergamino/altar
        pygame.draw.rect(surface, COLOR_UI_BORDER, (10, 10, VIRTUAL_WIDTH - 20, VIRTUAL_HEIGHT - 20), 2)
        pygame.draw.rect(surface, (100, 75, 35), (14, 14, VIRTUAL_WIDTH - 28, VIRTUAL_HEIGHT - 28), 1)

        # Título del juego
        title_surf = self.fonts["large"].render(TITLE, True, COLOR_TEXT_GOLD)
        surface.blit(title_surf, ((VIRTUAL_WIDTH - title_surf.get_width()) // 2, 35))

        sub_surf = self.fonts["small"].render(SUBTITLE, True, COLOR_TEXT_MUTED)
        surface.blit(sub_surf, ((VIRTUAL_WIDTH - sub_surf.get_width()) // 2, 58))

        # Lista de opciones del menú
        start_y = 95
        spacing = 22

        for idx, (label, key) in enumerate(self.options):
            is_sel = (idx == self.selected_idx)
            is_disabled = (key == "continue" and not self.has_save)

            if is_sel:
                text = f"► {label} ◄"
                color = COLOR_TEXT_GOLD
            else:
                text = label
                color = (120, 115, 110) if is_disabled else COLOR_TEXT

            opt_surf = self.fonts["medium"].render(text, True, color)
            opt_x = (VIRTUAL_WIDTH - opt_surf.get_width()) // 2
            opt_y = start_y + idx * spacing

            # Fondo sutil al elemento seleccionado
            if is_sel:
                sel_box = pygame.Rect(opt_x - 12, opt_y - 2, opt_surf.get_width() + 24, opt_surf.get_height() + 4)
                pygame.draw.rect(surface, (30, 40, 55), sel_box, border_radius=4)
                pygame.draw.rect(surface, COLOR_UI_BORDER, sel_box, 1, border_radius=4)

            surface.blit(opt_surf, (opt_x, opt_y))

        # Mensaje de advertencia o aviso temporal
        if self.notice_msg:
            notice_surf = self.fonts["small"].render(self.notice_msg, True, (231, 76, 60))
            surface.blit(notice_surf, ((VIRTUAL_WIDTH - notice_surf.get_width()) // 2, 215))

        # Crédito del autor y pie
        credit_text = f"Creado por {AUTHOR} | Proyecto Educativo Python & Pygame"
        credit_surf = self.fonts["small"].render(credit_text, True, COLOR_TEXT_MUTED)
        surface.blit(credit_surf, ((VIRTUAL_WIDTH - credit_surf.get_width()) // 2, VIRTUAL_HEIGHT - 24))
