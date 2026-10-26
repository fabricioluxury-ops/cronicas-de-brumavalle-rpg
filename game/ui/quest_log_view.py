"""
game/ui/quest_log_view.py
Diario y registro detallado de la misión principal (tecla J).
Muestra etapas completadas, objetivo activo y trasfondo narrativo.
"""
import pygame
from game.settings import (
    VIRTUAL_WIDTH, VIRTUAL_HEIGHT, COLOR_UI_BORDER,
    COLOR_TEXT, COLOR_TEXT_GOLD, COLOR_TEXT_MUTED, COLOR_HP_GREEN
)
from game.audio import audio


class QuestLogView:
    """Ventana de consulta del registro de misiones y progreso."""

    def __init__(self, font_title, font_body):
        self.font_title = font_title
        self.font_body = font_body
        self.active = False

        self.width = 340
        self.height = 200
        self.x = (VIRTUAL_WIDTH - self.width) // 2
        self.y = (VIRTUAL_HEIGHT - self.height) // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def toggle(self):
        """Abre o cierra el registro de misiones."""
        self.active = not self.active
        if self.active:
            audio.play("select")

    def handle_input(self, event):
        """Cierra la ventana con J o ESC."""
        if not self.active:
            return
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_j, pygame.K_ESCAPE, pygame.K_RETURN):
                self.active = False
                audio.play("select")

    def draw(self, surface, quest_manager):
        """Dibuja el diario de misiones con casilla de verificación y resumen."""
        if not self.active:
            return

        # 1. Fondo sombreado
        backdrop = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
        backdrop.fill((10, 12, 16, 170))
        surface.blit(backdrop, (0, 0))

        # 2. Marco del diario
        panel = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        panel.fill((20, 24, 34, 245))
        surface.blit(panel, (self.x, self.y))
        pygame.draw.rect(surface, COLOR_UI_BORDER, self.rect, 2)
        pygame.draw.rect(surface, (100, 75, 35), self.rect.inflate(-4, -4), 1)

        # 3. Título
        title_surf = self.font_title.render("DIARIO DE MISIONES", True, COLOR_TEXT_GOLD)
        surface.blit(title_surf, ((VIRTUAL_WIDTH - title_surf.get_width()) // 2, self.y + 8))

        # 4. Nombre de la misión
        quest_name = "Misión Principal: La Llama Antigua de Brumavalle"
        q_surf = self.font_body.render(quest_name, True, COLOR_TEXT_GOLD)
        surface.blit(q_surf, (self.x + 16, self.y + 30))

        # 5. Pasos de la misión
        steps = [
            (0, "Habla con la Sabia Elira en el claro del bosque."),
            (1, "Derrota al Guardián de las Sombras en Kal-Drakor."),
            (2, "Recupera la Reliquia de la Llama Antigua del altar."),
            (3, "Entrega la reliquia a la Guardiana Valeria en el pueblo."),
        ]

        cur_stage = quest_manager.stage
        step_y = self.y + 50

        for stage_req, step_text in steps:
            # Estado del paso
            if cur_stage > stage_req:
                box_icon = "[✓]"
                color = COLOR_HP_GREEN
            elif cur_stage == stage_req:
                box_icon = "[►]"
                color = COLOR_TEXT_GOLD
            else:
                box_icon = "[ ]"
                color = COLOR_TEXT_MUTED

            line_surf = self.font_body.render(f"{box_icon} {step_text}", True, color)
            surface.blit(line_surf, (self.x + 16, step_y))
            step_y += 18

        # 6. Descripción del estado actual
        info = quest_manager.get_current_info()
        desc_box = pygame.Rect(self.x + 16, self.y + 130, self.width - 32, 44)
        pygame.draw.rect(surface, (28, 32, 44), desc_box)
        pygame.draw.rect(surface, (100, 75, 35), desc_box, 1)

        note_surf = self.font_body.render(f"Detalle: {info['desc'][:50]}...", True, COLOR_TEXT)
        surface.blit(note_surf, (desc_box.x + 6, desc_box.y + 6))

        target_surf = self.font_body.render(f"Próximo paso: {info['target']}", True, COLOR_TEXT_GOLD)
        surface.blit(target_surf, (desc_box.x + 6, desc_box.y + 22))

        # 7. Ayuda al pie
        hint_surf = self.font_body.render("[J o ESC] Cerrar diario", True, COLOR_TEXT_MUTED)
        surface.blit(hint_surf, ((VIRTUAL_WIDTH - hint_surf.get_width()) // 2, self.y + self.height - 18))
