"""
game/states/credits_state.py
Pantalla de créditos del juego con mención de autoría y nota educativa.
Nombre de autor exacto: "Eric Fabricio García García".
"""
import pygame
from game.states.base_state import BaseState
from game.settings import (
    VIRTUAL_WIDTH, VIRTUAL_HEIGHT, COLOR_UI_BORDER,
    COLOR_TEXT, COLOR_TEXT_GOLD, COLOR_TEXT_MUTED, TITLE, AUTHOR
)
from game.audio import audio


class CreditsState(BaseState):
    """Pantalla con información de autoría, herramientas y licencias educativas."""

    def __init__(self, state_machine, fonts):
        super().__init__(state_machine)
        self.fonts = fonts

        self.width = 380
        self.height = 220
        self.x = (VIRTUAL_WIDTH - self.width) // 2
        self.y = (VIRTUAL_HEIGHT - self.height) // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE, pygame.K_e):
                audio.play("select")
                self.state_machine.pop_state()

    def draw(self, surface):
        # Fondo oscuro
        backdrop = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
        backdrop.fill((10, 12, 16, 215))
        surface.blit(backdrop, (0, 0))

        # Panel
        panel = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        panel.fill((20, 24, 34, 250))
        surface.blit(panel, (self.x, self.y))
        pygame.draw.rect(surface, COLOR_UI_BORDER, self.rect, 2)
        pygame.draw.rect(surface, (100, 75, 35), self.rect.inflate(-4, -4), 1)

        # Título
        title_surf = self.fonts["large"].render("CRÉDITOS", True, COLOR_TEXT_GOLD)
        surface.blit(title_surf, ((VIRTUAL_WIDTH - title_surf.get_width()) // 2, self.y + 12))

        game_title_surf = self.fonts["small"].render(TITLE, True, COLOR_TEXT)
        surface.blit(game_title_surf, ((VIRTUAL_WIDTH - game_title_surf.get_width()) // 2, self.y + 32))

        pygame.draw.line(surface, (100, 75, 35), (self.x + 24, self.y + 48), (self.x + self.width - 24, self.y + 48))

        # Autoría exacta
        author_label = self.fonts["small"].render("Dirección, Programación y Diseño de Juego:", True, COLOR_TEXT_MUTED)
        surface.blit(author_label, ((VIRTUAL_WIDTH - author_label.get_width()) // 2, self.y + 58))

        author_name = self.fonts["medium"].render(f"Creado por {AUTHOR}", True, COLOR_TEXT_GOLD)
        surface.blit(author_name, ((VIRTUAL_WIDTH - author_name.get_width()) // 2, self.y + 74))

        # Nota educativa y de originalidad
        notes = [
            "— NOTA EDUCATIVA Y DE ORIGINALIDAD —",
            "Este proyecto fue desarrollado con fines educativos y de demostración",
            "para la materia de programación con Python y la biblioteca Pygame.",
            "",
            "Todos los personajes (Valeria, Torin, Elira, Eric), la historia de",
            "Brumavalle, los diálogos, el mapa y los recursos visuales de pixel art",
            "fueron diseñados originalmente y generados mediante código Python,",
            "garantizando la total ausencia de material protegido por copyright de terceros."
        ]

        ny = self.y + 98
        for line in notes:
            if not line:
                ny += 4
                continue
            is_header = line.startswith("—")
            color = COLOR_TEXT_GOLD if is_header else COLOR_TEXT
            n_surf = self.fonts["small"].render(line, True, color)
            surface.blit(n_surf, ((VIRTUAL_WIDTH - n_surf.get_width()) // 2, ny))
            ny += 11

        # Pie
        hint_surf = self.fonts["small"].render("[ Presiona ESC o ENTER para volver ]", True, COLOR_TEXT_MUTED)
        surface.blit(hint_surf, ((VIRTUAL_WIDTH - hint_surf.get_width()) // 2, self.y + self.height - 16))
