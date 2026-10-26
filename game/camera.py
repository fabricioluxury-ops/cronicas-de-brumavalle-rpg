"""
game/camera.py
Sistema de cámara 2D con seguimiento suave del jugador y sujeción a los límites del mapa.
"""
import pygame
from game.settings import VIRTUAL_WIDTH, VIRTUAL_HEIGHT


class Camera:
    """Controla el visor de la pantalla sobre el mapa del mundo."""

    def __init__(self, map_pixel_width, map_pixel_height):
        self.rect = pygame.Rect(0, 0, VIRTUAL_WIDTH, VIRTUAL_HEIGHT)
        self.map_width = map_pixel_width
        self.map_height = map_pixel_height
        self.x = 0.0
        self.y = 0.0

    def update(self, target_rect):
        """Centra la cámara en el objetivo y limita el desplazamiento a los bordes del mapa."""
        # Objetivo en el centro de la pantalla virtual
        target_x = target_rect.centerx - (VIRTUAL_WIDTH // 2)
        target_y = target_rect.centery - (VIRTUAL_HEIGHT // 2)

        # Suave interpolación (LERP) para evitar sacudidas
        self.x += (target_x - self.x) * 0.15
        self.y += (target_y - self.y) * 0.15

        # Limitar dentro de los bordes del mapa
        max_x = max(0, self.map_width - VIRTUAL_WIDTH)
        max_y = max(0, self.map_height - VIRTUAL_HEIGHT)

        self.x = max(0.0, min(float(max_x), self.x))
        self.y = max(0.0, min(float(max_y), self.y))

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def apply(self, entity_or_rect):
        """Devuelve un nuevo Rect desplazado por la posición de la cámara."""
        if hasattr(entity_or_rect, "rect"):
            r = entity_or_rect.rect
        else:
            r = entity_or_rect
        return pygame.Rect(r.x - self.rect.x, r.y - self.rect.y, r.width, r.height)

    def apply_pos(self, x, y):
        """Convierte una coordenada del mundo a coordenadas de pantalla."""
        return x - self.rect.x, y - self.rect.y
