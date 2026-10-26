"""
game/states/loading_state.py
Pantalla inicial de carga con barra animada y mensajes de preparación del reino.
Genera los recursos pixel art proceduralmente sin trabarse ni quedarse congelada.
"""
import pygame
from game.states.base_state import BaseState
from game.settings import (
    VIRTUAL_WIDTH, VIRTUAL_HEIGHT, COLOR_UI_BORDER,
    COLOR_TEXT, COLOR_TEXT_GOLD, COLOR_TEXT_MUTED, TITLE, SUBTITLE
)
from game.asset_loader import assets


class LoadingState(BaseState):
    """Pantalla de carga con inicialización progresiva de recursos."""

    MESSAGES = [
        (0.15, "Preparando el reino de Brumavalle..."),
        (0.35, "Cargando personajes y armaduras..."),
        (0.60, "Encendiendo las antorchas del bosque..."),
        (0.85, "Despertando a los guardianes antiguos..."),
        (1.00, "¡El reino está listo!"),
    ]

    def __init__(self, state_machine, fonts):
        super().__init__(state_machine)
        self.fonts = fonts
        self.progress = 0.0
        self.target_progress = 0.0
        self.current_msg = "Iniciando..."
        self.step = 0
        self.finish_delay = 20

    def enter(self, **kwargs):
        self.progress = 0.0
        self.step = 0
        self.target_progress = 0.1
        self.current_msg = self.MESSAGES[0][1]

    def update(self):
        # Avanzar el progreso suavemente
        if self.progress < self.target_progress:
            self.progress += 0.02
            if self.progress > self.target_progress:
                self.progress = self.target_progress

        # Ejecución secuencial de la carga
        if self.progress >= self.target_progress:
            if self.step == 0:
                assets.initialize_all()
                self.step = 1
                self.target_progress = 0.4
                self.current_msg = self.MESSAGES[1][1]
            elif self.step == 1:
                self.step = 2
                self.target_progress = 0.7
                self.current_msg = self.MESSAGES[2][1]
            elif self.step == 2:
                self.step = 3
                self.target_progress = 0.9
                self.current_msg = self.MESSAGES[3][1]
            elif self.step == 3:
                self.step = 4
                self.target_progress = 1.0
                self.current_msg = self.MESSAGES[4][1]
            elif self.step == 4:
                self.finish_delay -= 1
                if self.finish_delay <= 0:
                    self.state_machine.change_state("menu")

    def draw(self, surface):
        surface.fill((16, 20, 28))

        # Marco decorativo exterior
        margin = 12
        pygame.draw.rect(surface, COLOR_UI_BORDER, (margin, margin, VIRTUAL_WIDTH - margin * 2, VIRTUAL_HEIGHT - margin * 2), 1)

        # Título principal
        title_surf = self.fonts["large"].render(TITLE, True, COLOR_TEXT_GOLD)
        surface.blit(title_surf, ((VIRTUAL_WIDTH - title_surf.get_width()) // 2, 70))

        sub_surf = self.fonts["small"].render(SUBTITLE, True, COLOR_TEXT_MUTED)
        surface.blit(sub_surf, ((VIRTUAL_WIDTH - sub_surf.get_width()) // 2, 95))

        # Barra de progreso
        bar_w = 260
        bar_h = 12
        bar_x = (VIRTUAL_WIDTH - bar_w) // 2
        bar_y = 150

        # Fondo barra
        pygame.draw.rect(surface, (30, 35, 45), (bar_x, bar_y, bar_w, bar_h))
        # Relleno de la barra
        fill_w = int(bar_w * self.progress)
        if fill_w > 0:
            pygame.draw.rect(surface, (196, 164, 102), (bar_x, bar_y, fill_w, bar_h))
        # Borde dorado
        pygame.draw.rect(surface, COLOR_UI_BORDER, (bar_x, bar_y, bar_w, bar_h), 1)

        # Mensaje de carga animado
        msg_surf = self.fonts["small"].render(self.current_msg, True, COLOR_TEXT)
        surface.blit(msg_surf, ((VIRTUAL_WIDTH - msg_surf.get_width()) // 2, bar_y + 20))
