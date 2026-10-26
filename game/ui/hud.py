"""
game/ui/hud.py
Interfaz en pantalla (HUD): barra de vida del jugador, nombre, objetivo de misión
activo y recordatorio de controles principales en formato pixel art retro.
"""
import pygame
from game.settings import (
    VIRTUAL_WIDTH, VIRTUAL_HEIGHT, COLOR_UI_BG, COLOR_UI_BORDER,
    COLOR_TEXT, COLOR_TEXT_GOLD, COLOR_HP_RED, COLOR_HP_GREEN,
    COLOR_BLACK, COLOR_TEXT_MUTED
)


class HUD:
    """Gestiona la información superpuesta durante el juego en tiempo real."""

    def __init__(self, font_small, font_medium):
        self.font_small = font_small
        self.font_medium = font_medium

    def draw(self, surface, player, quest_manager):
        """Dibuja todos los elementos del HUD sobre la superficie virtual."""
        # ==========================================
        # 1. TARJETA DEL JUGADOR Y VIDA (Superior Izquierda)
        # ==========================================
        card_w = 130
        card_h = 32
        card_rect = pygame.Rect(6, 6, card_w, card_h)

        # Fondo translúcido oscuro con borde dorado
        bg_surf = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        bg_surf.fill((20, 24, 32, 220))
        surface.blit(bg_surf, (card_rect.x, card_rect.y))
        pygame.draw.rect(surface, COLOR_UI_BORDER, card_rect, 1)

        # Nombre del personaje
        name_surf = self.font_small.render(f"Héroe: {player.name}", True, COLOR_TEXT_GOLD)
        surface.blit(name_surf, (card_rect.x + 6, card_rect.y + 4))

        # Barra de salud (PV)
        bar_x = card_rect.x + 6
        bar_y = card_rect.y + 17
        bar_w = 118
        bar_h = 9

        # Fondo barra de vida
        pygame.draw.rect(surface, (40, 10, 10), (bar_x, bar_y, bar_w, bar_h))
        # Relleno de vida proporcional
        ratio = max(0.0, min(1.0, player.hp / player.max_hp))
        fill_w = int(bar_w * ratio)
        if fill_w > 0:
            color = COLOR_HP_GREEN if ratio > 0.3 else COLOR_HP_RED
            pygame.draw.rect(surface, color, (bar_x, bar_y, fill_w, bar_h))
        # Borde de la barra
        pygame.draw.rect(surface, (150, 140, 120), (bar_x, bar_y, bar_w, bar_h), 1)

        # Texto numérico de vida
        hp_text = self.font_small.render(f"PV: {player.hp}/{player.max_hp}", True, COLOR_TEXT)
        surface.blit(hp_text, (bar_x + 24, bar_y - 1))

        # ==========================================
        # 2. BANNER DE OBJETIVO ACTUAL (Superior Derecha)
        # ==========================================
        quest_info = quest_manager.get_current_info()
        obj_text = f"Objetivo: {quest_info['target']}"
        obj_surf = self.font_small.render(obj_text, True, COLOR_TEXT)

        banner_w = obj_surf.get_width() + 16
        banner_h = 20
        banner_x = VIRTUAL_WIDTH - banner_w - 6
        banner_y = 6
        banner_rect = pygame.Rect(banner_x, banner_y, banner_w, banner_h)

        bg_banner = pygame.Surface((banner_w, banner_h), pygame.SRCALPHA)
        bg_banner.fill((20, 24, 32, 220))
        surface.blit(bg_banner, (banner_rect.x, banner_rect.y))
        pygame.draw.rect(surface, COLOR_UI_BORDER, banner_rect, 1)

        surface.blit(obj_surf, (banner_rect.x + 8, banner_rect.y + 4))

        # ==========================================
        # 3. BARRA INFERIOR DE CONTROLES RÁPIDOS
        # ==========================================
        ctrl_text = "[WASD/Flechas] Mover | [Espacio] Atacar | [E] Hablar/Abrir | [I] Inventario | [J] Misión | [ESC] Pausa"
        ctrl_surf = self.font_small.render(ctrl_text, True, COLOR_TEXT_MUTED)

        ctrl_bg = pygame.Surface((VIRTUAL_WIDTH, 14), pygame.SRCALPHA)
        ctrl_bg.fill((10, 12, 18, 200))
        surface.blit(ctrl_bg, (0, VIRTUAL_HEIGHT - 14))

        surface.blit(ctrl_surf, ((VIRTUAL_WIDTH - ctrl_surf.get_width()) // 2, VIRTUAL_HEIGHT - 13))
