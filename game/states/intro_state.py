"""
game/states/intro_state.py
Pantalla de introducción narrativa: presenta el trasfondo del reino de Brumavalle
y permite continuar pulsando ENTER o ESPACIO.
"""
import pygame
from game.states.base_state import BaseState
from game.settings import (
    VIRTUAL_WIDTH, VIRTUAL_HEIGHT, COLOR_UI_BORDER,
    COLOR_TEXT, COLOR_TEXT_GOLD, COLOR_TEXT_MUTED
)
from game.audio import audio


class IntroState(BaseState):
    """Pantalla con prólogo de la historia."""

    STORY_PARAGRAPHS = [
        "Durante generaciones, la 'Llama Antigua' ardió en el pedestal sagrado de",
        "Kal-Drakor, proyectando un manto protector sobre los valles de Brumavalle.",
        "",
        "Pero una noche silenciosa, las sombras ancestrales despertaron en las ruinas.",
        "El fuego sagrado fue arrebatado y una densa bruma cubrió los senderos del bosque.",
        "Criaturas oscuras ahora acechan a las afueras de la aldea...",
        "",
        "La capitana Valeria ha apostado a sus guardias, pero las leyendas dicen que",
        "solo aquel que consulte a la Sabia Elira y empuñe el acero contra las sombras",
        "podrá recuperar la reliquia y salvar el reino de una noche eterna.",
        "",
        "Tu viaje comienza a las puertas de Brumavalle..."
    ]

    def __init__(self, state_machine, fonts):
        super().__init__(state_machine)
        self.fonts = fonts
        self.fade_alpha = 255

    def enter(self, **kwargs):
        self.fade_alpha = 255

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE, pygame.K_e):
                audio.play("select")
                self.state_machine.change_state("play")

    def update(self):
        if self.fade_alpha > 0:
            self.fade_alpha = max(0, self.fade_alpha - 8)

    def draw(self, surface):
        surface.fill((14, 18, 24))

        # Marco pergamino
        pygame.draw.rect(surface, COLOR_UI_BORDER, (16, 16, VIRTUAL_WIDTH - 32, VIRTUAL_HEIGHT - 32), 2)
        pygame.draw.rect(surface, (100, 75, 35), (20, 20, VIRTUAL_WIDTH - 40, VIRTUAL_HEIGHT - 40), 1)

        # Título
        title_surf = self.fonts["large"].render("CRÓNICAS DE BRUMAVALLE", True, COLOR_TEXT_GOLD)
        surface.blit(title_surf, ((VIRTUAL_WIDTH - title_surf.get_width()) // 2, 28))

        sub_surf = self.fonts["small"].render("— Prólogo de la Aventura —", True, COLOR_TEXT_MUTED)
        surface.blit(sub_surf, ((VIRTUAL_WIDTH - sub_surf.get_width()) // 2, 48))

        # Texto del prólogo
        text_y = 70
        for line in self.STORY_PARAGRAPHS:
            if line == "":
                text_y += 6
                continue
            line_surf = self.fonts["small"].render(line, True, COLOR_TEXT)
            surface.blit(line_surf, ((VIRTUAL_WIDTH - line_surf.get_width()) // 2, text_y))
            text_y += 12

        # Indicación al pie para continuar
        prompt_surf = self.fonts["medium"].render("[ Presiona ENTER o ESPACIO para comenzar ]", True, COLOR_TEXT_GOLD)
        surface.blit(prompt_surf, ((VIRTUAL_WIDTH - prompt_surf.get_width()) // 2, VIRTUAL_HEIGHT - 32))

        # Cortina de fade in
        if self.fade_alpha > 0:
            fade_surf = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
            fade_surf.fill((0, 0, 0))
            fade_surf.set_alpha(self.fade_alpha)
            surface.blit(fade_surf, (0, 0))
