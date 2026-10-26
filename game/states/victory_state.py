"""
game/states/victory_state.py
Pantalla triunfal de victoria al culminar la misión principal de la Llama Antigua.
Permite iniciar una nueva partida o volver al menú principal.
"""
import pygame
from game.states.base_state import BaseState
from game.settings import (
    VIRTUAL_WIDTH, VIRTUAL_HEIGHT, COLOR_UI_BORDER,
    COLOR_TEXT, COLOR_TEXT_GOLD, COLOR_TEXT_MUTED, COLOR_HP_GREEN, AUTHOR
)
from game.audio import audio


class VictoryState(BaseState):
    """Pantalla conmemorativa de misión completada."""

    def __init__(self, state_machine, fonts):
        super().__init__(state_machine)
        self.fonts = fonts
        self.options = [
            ("Comenzar Nueva Aventura", "replay"),
            ("Volver al Menú Principal", "menu")
        ]
        self.selected_idx = 0

    def enter(self, **kwargs):
        self.selected_idx = 0
        audio.play("quest")

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

        if opt_key == "replay":
            self.state_machine.change_state("play")
        elif opt_key == "menu":
            self.state_machine.change_state("menu")

    def draw(self, surface):
        surface.fill((16, 26, 22))

        # Marco dorado y esmeralda
        pygame.draw.rect(surface, COLOR_UI_BORDER, (14, 14, VIRTUAL_WIDTH - 28, VIRTUAL_HEIGHT - 28), 2)
        pygame.draw.rect(surface, (46, 204, 113), (18, 18, VIRTUAL_WIDTH - 36, VIRTUAL_HEIGHT - 36), 1)

        # Título triunfal
        title_surf = self.fonts["large"].render("¡LA LLAMA ANTIGUA HA SIDO RESTAURADA!", True, COLOR_TEXT_GOLD)
        surface.blit(title_surf, ((VIRTUAL_WIDTH - title_surf.get_width()) // 2, 35))

        sub_surf = self.fonts["small"].render("— La paz y la luz regresan a Brumavalle —", True, COLOR_HP_GREEN)
        surface.blit(sub_surf, ((VIRTUAL_WIDTH - sub_surf.get_width()) // 2, 58))

        # Texto narrativo de victoria
        narrative = [
            "Con valentía y destreza, cruzaste el Bosque Susurrante,",
            "derrotaste al temible Guardián de las Sombras en las Ruinas de Kal-Drakor",
            "y recuperaste el fuego sagrado de nuestros ancestros.",
            "",
            "La Guardiana Valeria ha colocado la Llama en la plaza principal,",
            "la sabia Elira sonríe en su santuario y Torin levanta su copa en tu honor.",
            "¡El reino de Brumavalle está a salvo gracias a ti!",
        ]

        ny = 78
        for line in narrative:
            if not line:
                ny += 4
                continue
            line_surf = self.fonts["small"].render(line, True, COLOR_TEXT)
            surface.blit(line_surf, ((VIRTUAL_WIDTH - line_surf.get_width()) // 2, ny))
            ny += 11

        # Opciones
        start_y = 175
        spacing = 20

        for idx, (label, _) in enumerate(self.options):
            is_sel = (idx == self.selected_idx)
            text = f"► {label} ◄" if is_sel else label
            color = COLOR_TEXT_GOLD if is_sel else COLOR_TEXT

            opt_surf = self.fonts["medium"].render(text, True, color)
            opt_x = (VIRTUAL_WIDTH - opt_surf.get_width()) // 2
            opt_y = start_y + idx * spacing

            if is_sel:
                sel_box = pygame.Rect(opt_x - 10, opt_y - 2, opt_surf.get_width() + 20, opt_surf.get_height() + 4)
                pygame.draw.rect(surface, (25, 45, 35), sel_box, border_radius=4)
                pygame.draw.rect(surface, COLOR_UI_BORDER, sel_box, 1, border_radius=4)

            surface.blit(opt_surf, (opt_x, opt_y))

        # Autor
        foot_surf = self.fonts["small"].render(f"Proyecto creado por {AUTHOR}", True, COLOR_TEXT_MUTED)
        surface.blit(foot_surf, ((VIRTUAL_WIDTH - foot_surf.get_width()) // 2, VIRTUAL_HEIGHT - 22))
