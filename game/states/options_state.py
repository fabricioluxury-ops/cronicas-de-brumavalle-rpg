"""
game/states/options_state.py
Menú de opciones de audio y guía de controles del juego.
Permite alternar sonido, ajustar volumen y consultar atajos de teclado.
"""
import pygame
from game.states.base_state import BaseState
from game.settings import (
    VIRTUAL_WIDTH, VIRTUAL_HEIGHT, COLOR_UI_BORDER,
    COLOR_TEXT, COLOR_TEXT_GOLD, COLOR_TEXT_MUTED, COLOR_HP_GREEN
)
from game.audio import audio


class OptionsState(BaseState):
    """Menú de configuración y controles."""

    def __init__(self, state_machine, fonts):
        super().__init__(state_machine)
        self.fonts = fonts
        self.selected_idx = 0
        self.options = [
            "Efectos de Sonido",
            "Volumen",
            "Volver"
        ]

        self.width = 320
        self.height = 210
        self.x = (VIRTUAL_WIDTH - self.width) // 2
        self.y = (VIRTUAL_HEIGHT - self.height) // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

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
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self._adjust_option(-1)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self._adjust_option(1)
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE, pygame.K_e):
                if self.selected_idx == 0:
                    self._adjust_option(1)
                elif self.selected_idx == 1:
                    self._adjust_option(1)
                elif self.selected_idx == 2:
                    audio.play("select")
                    self.state_machine.pop_state()

    def _adjust_option(self, delta):
        if self.selected_idx == 0:
            audio.toggle()
            audio.play("select")
        elif self.selected_idx == 1:
            new_vol = round(audio.volume + delta * 0.1, 1)
            audio.set_volume(new_vol)
            audio.play("select")

    def draw(self, surface):
        # Fondo oscuro
        backdrop = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
        backdrop.fill((10, 12, 16, 210))
        surface.blit(backdrop, (0, 0))

        # Panel
        panel = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        panel.fill((20, 24, 34, 245))
        surface.blit(panel, (self.x, self.y))
        pygame.draw.rect(surface, COLOR_UI_BORDER, self.rect, 2)
        pygame.draw.rect(surface, (100, 75, 35), self.rect.inflate(-4, -4), 1)

        # Título
        title_surf = self.fonts["large"].render("OPCIONES Y CONTROLES", True, COLOR_TEXT_GOLD)
        surface.blit(title_surf, ((VIRTUAL_WIDTH - title_surf.get_width()) // 2, self.y + 10))

        # Opciones ajustables
        start_y = self.y + 35
        for idx, name in enumerate(self.options):
            is_sel = (idx == self.selected_idx)
            val_text = ""
            if idx == 0:
                val_text = "[ Activado ]" if audio.enabled else "[ Silenciado ]"
            elif idx == 1:
                val_text = f"< {int(audio.volume * 100)}% >"

            text = f"► {name}: {val_text}" if val_text else f"► {name}"
            if not is_sel:
                text = f"  {name}: {val_text}" if val_text else f"  {name}"

            color = COLOR_TEXT_GOLD if is_sel else COLOR_TEXT
            opt_surf = self.fonts["small"].render(text, True, color)
            surface.blit(opt_surf, (self.x + 20, start_y + idx * 18))

        # Separador y guía de controles
        line_y = self.y + 95
        pygame.draw.line(surface, (100, 75, 35), (self.x + 16, line_y), (self.x + self.width - 16, line_y))

        guide_title = self.fonts["small"].render("— Mapa de Controles —", True, COLOR_TEXT_GOLD)
        surface.blit(guide_title, ((VIRTUAL_WIDTH - guide_title.get_width()) // 2, line_y + 6))

        controls_lines = [
            ("WASD o Flechas:", "Moverse por el reino en 4 direcciones"),
            ("ESPACIO:", "Atacar con la espada de acero"),
            ("E o ENTER:", "Interactuar, hablar y abrir cofres"),
            ("I:", "Abrir inventario (beber pociones con U/Enter)"),
            ("J:", "Consultar el diario de misiones"),
            ("ESC:", "Menú de pausa y retroceder"),
        ]

        cy = line_y + 22
        for k_label, k_desc in controls_lines:
            kl_surf = self.fonts["small"].render(k_label, True, COLOR_TEXT_GOLD)
            kd_surf = self.fonts["small"].render(k_desc, True, COLOR_TEXT)
            surface.blit(kl_surf, (self.x + 20, cy))
            surface.blit(kd_surf, (self.x + 115, cy))
            cy += 12

        # Pie
        hint_surf = self.fonts["small"].render("[ESC o ENTER] Volver", True, COLOR_TEXT_MUTED)
        surface.blit(hint_surf, ((VIRTUAL_WIDTH - hint_surf.get_width()) // 2, self.y + self.height - 15))
