"""
game/ui/dialogue_box.py
Ventana de diálogo clásica de RPG medieval con retrato, nombre del interlocutor
y navegación fluida mediante teclas E o ENTER.
"""
import pygame
from game.settings import (
    VIRTUAL_WIDTH, VIRTUAL_HEIGHT, COLOR_UI_BORDER,
    COLOR_TEXT, COLOR_TEXT_GOLD, COLOR_TEXT_MUTED
)
from game.audio import audio


class DialogueBox:
    """Administra la visualización y avance de diálogos."""

    def __init__(self, font_name, font_dialogue):
        self.font_name = font_name
        self.font_dialogue = font_dialogue
        self.active = False
        self.lines = []
        self.current_line_idx = 0
        self.speaker_name = ""
        self.portrait = None
        self.on_complete_callback = None

        # Dimensiones del panel de diálogo
        self.width = VIRTUAL_WIDTH - 24
        self.height = 68
        self.x = 12
        self.y = VIRTUAL_HEIGHT - self.height - 18
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def start_dialogue(self, speaker_name, lines, portrait=None, on_complete=None):
        """Inicia una conversación con las líneas dadas."""
        self.active = True
        self.speaker_name = speaker_name
        self.lines = lines if isinstance(lines, list) else [lines]
        self.current_line_idx = 0
        self.portrait = portrait
        self.on_complete_callback = on_complete
        audio.play("talk")

    def advance(self):
        """Avanza a la siguiente línea de diálogo o cierra la ventana al terminar."""
        if not self.active:
            return

        self.current_line_idx += 1
        if self.current_line_idx >= len(self.lines):
            self.active = False
            if self.on_complete_callback:
                self.on_complete_callback()
        else:
            audio.play("talk")

    def close(self):
        """Cierra el diálogo inmediatamente."""
        self.active = False
        if self.on_complete_callback:
            self.on_complete_callback()

    def draw(self, surface):
        """Dibuja la caja de diálogo con marco dorado, retrato y texto con ajuste de línea."""
        if not self.active or not self.lines:
            return

        # 1. Fondo oscuro translúcido con marco decorativo
        bg_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        bg_surf.fill((16, 20, 28, 235))
        surface.blit(bg_surf, (self.x, self.y))
        pygame.draw.rect(surface, COLOR_UI_BORDER, self.rect, 2)
        pygame.draw.rect(surface, (100, 75, 35), self.rect.inflate(-4, -4), 1)

        # 2. Retrato del personaje a la izquierda
        text_start_x = self.x + 12
        if self.portrait:
            # Marco del retrato
            portrait_rect = pygame.Rect(self.x + 8, self.y + 8, 36, 36)
            pygame.draw.rect(surface, (30, 35, 45), portrait_rect)
            pygame.draw.rect(surface, COLOR_UI_BORDER, portrait_rect, 1)
            # Dibujar retrato escalado o centrado
            surface.blit(self.portrait, (portrait_rect.x + 2, portrait_rect.y + 2))
            text_start_x = self.x + 50

        # 3. Nombre del hablante
        name_surf = self.font_name.render(self.speaker_name, True, COLOR_TEXT_GOLD)
        surface.blit(name_surf, (text_start_x, self.y + 8))

        # 4. Texto del diálogo (con ajuste de líneas para que no se salga de la pantalla)
        raw_text = self.lines[self.current_line_idx]
        # Si el texto ya contiene el prefijo "Nombre: 'texto'", removerlo si ya tenemos el nombre arriba
        clean_text = raw_text
        if ":" in raw_text and raw_text.startswith(self.speaker_name):
            clean_text = raw_text.split(":", 1)[1].strip().strip("'\"")

        words = clean_text.split(" ")
        lines_to_draw = []
        current_line = ""
        max_line_w = (self.x + self.width - 24) - text_start_x

        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if self.font_dialogue.size(test_line)[0] < max_line_w:
                current_line = test_line
            else:
                lines_to_draw.append(current_line)
                current_line = word
        if current_line:
            lines_to_draw.append(current_line)

        text_y = self.y + 24
        for l in lines_to_draw[:3]:  # Hasta 3 líneas en el cuadro
            l_surf = self.font_dialogue.render(l, True, COLOR_TEXT)
            surface.blit(l_surf, (text_start_x, text_y))
            text_y += 13

        # 5. Indicador de continuar [E / ENTER ►]
        prompt_surf = self.font_dialogue.render("[E / ENTER] ►", True, COLOR_TEXT_GOLD)
        surface.blit(prompt_surf, (self.x + self.width - prompt_surf.get_width() - 8, self.y + self.height - 15))
