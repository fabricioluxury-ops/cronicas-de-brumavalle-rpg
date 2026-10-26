"""
game/ui/inventory_view.py
Pantalla y ventana modal de inventario (tecla I).
Muestra equipamiento, pociones, objetos clave y permite consumir brebajes curativos.
"""
import pygame
from game.settings import (
    VIRTUAL_WIDTH, VIRTUAL_HEIGHT, COLOR_UI_BORDER,
    COLOR_TEXT, COLOR_TEXT_GOLD, COLOR_TEXT_MUTED, COLOR_HP_GREEN
)
from game.audio import audio


class InventoryView:
    """Ventana interactiva de inventario y gestión de objetos."""

    def __init__(self, font_title, font_body, asset_loader):
        self.font_title = font_title
        self.font_body = font_body
        self.assets = asset_loader
        self.active = False
        self.selected_idx = 0
        self.status_message = ""
        self.status_timer = 0

        self.width = 340
        self.height = 200
        self.x = (VIRTUAL_WIDTH - self.width) // 2
        self.y = (VIRTUAL_HEIGHT - self.height) // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def toggle(self):
        """Abre o cierra la vista del inventario."""
        self.active = not self.active
        self.selected_idx = 0
        self.status_message = ""
        if self.active:
            audio.play("select")

    def handle_input(self, event, player):
        """Maneja la navegación y uso de objetos en el inventario."""
        if not self.active:
            return

        items = player.inventory
        if not items:
            return

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected_idx = (self.selected_idx - 1) % len(items)
                audio.play("select")
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_idx = (self.selected_idx + 1) % len(items)
                audio.play("select")
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_u):
                # Usar objeto seleccionado
                sel_item = items[self.selected_idx]
                if sel_item.get("id") == "potion":
                    success, msg = player.use_potion()
                    self.status_message = msg
                    self.status_timer = 120
                    # Si se acabaron las pociones, ajustar índice
                    if sel_item.get("count", 0) <= 0:
                        # Mantenerlo en inventario con count 0 o seleccionarlo
                        pass
                else:
                    self.status_message = "Este objeto no puede ser consumido directamente."
                    self.status_timer = 90
            elif event.key in (pygame.K_ESCAPE, pygame.K_i):
                self.active = False
                audio.play("select")

    def update(self):
        """Actualiza temporizador de mensajes de estado."""
        if self.status_timer > 0:
            self.status_timer -= 1
            if self.status_timer == 0:
                self.status_message = ""

    def draw(self, surface, player):
        """Renderiza la ventana de inventario con lista de objetos e información detallada."""
        if not self.active:
            return

        # 1. Fondo sombreado completo de la pantalla
        backdrop = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
        backdrop.fill((10, 12, 16, 170))
        surface.blit(backdrop, (0, 0))

        # 2. Marco del panel de inventario
        panel = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        panel.fill((20, 24, 34, 245))
        surface.blit(panel, (self.x, self.y))
        pygame.draw.rect(surface, COLOR_UI_BORDER, self.rect, 2)
        pygame.draw.rect(surface, (100, 75, 35), self.rect.inflate(-4, -4), 1)

        # 3. Título de la ventana
        title_surf = self.font_title.render("INVENTARIO DEL HÉROE", True, COLOR_TEXT_GOLD)
        surface.blit(title_surf, ((VIRTUAL_WIDTH - title_surf.get_width()) // 2, self.y + 8))

        # 4. Lista de objetos a la izquierda
        list_x = self.x + 14
        list_y = self.y + 32
        items = player.inventory

        for idx, item in enumerate(items):
            is_sel = (idx == self.selected_idx)
            item_y = list_y + idx * 24

            # Resaltado de selección
            if is_sel:
                sel_rect = pygame.Rect(list_x - 4, item_y - 2, 160, 20)
                pygame.draw.rect(surface, (50, 60, 80), sel_rect)
                pygame.draw.rect(surface, COLOR_UI_BORDER, sel_rect, 1)

            # Icono del objeto
            icon_key = item.get("id", "")
            icon_surf = self.assets.icons.get(icon_key)
            if icon_surf:
                surface.blit(icon_surf, (list_x, item_y))

            # Nombre y cantidad
            display_name = item.get("name", "Objeto")
            if "count" in item:
                display_name += f" x{item['count']}"
            elif item.get("equipped"):
                display_name += " [Eq]"

            text_color = COLOR_TEXT_GOLD if is_sel else COLOR_TEXT
            name_surf = self.font_body.render(display_name[:18], True, text_color)
            surface.blit(name_surf, (list_x + 20, item_y + 3))

        # 5. Panel de detalles a la derecha
        detail_x = self.x + 180
        detail_y = self.y + 32
        detail_w = 145
        detail_h = 135
        detail_rect = pygame.Rect(detail_x, detail_y, detail_w, detail_h)
        pygame.draw.rect(surface, (28, 32, 44), detail_rect)
        pygame.draw.rect(surface, (100, 75, 35), detail_rect, 1)

        if items and 0 <= self.selected_idx < len(items):
            cur_item = items[self.selected_idx]
            # Nombre completo
            d_name = self.font_body.render(cur_item.get("name", ""), True, COLOR_TEXT_GOLD)
            surface.blit(d_name, (detail_x + 6, detail_y + 6))

            # Tipo
            item_type = "Arma" if cur_item.get("type") == "weapon" else "Consumible" if cur_item.get("type") == "consumable" else "Objeto Clave"
            t_surf = self.font_body.render(f"Tipo: {item_type}", True, COLOR_TEXT_MUTED)
            surface.blit(t_surf, (detail_x + 6, detail_y + 20))

            # Descripción ajustada
            desc_words = cur_item.get("desc", "").split(" ")
            d_lines = []
            curr_line = ""
            for w in desc_words:
                test = curr_line + (" " if curr_line else "") + w
                if self.font_body.size(test)[0] < (detail_w - 12):
                    curr_line = test
                else:
                    d_lines.append(curr_line)
                    curr_line = w
            if curr_line:
                d_lines.append(curr_line)

            for dy_idx, dl in enumerate(d_lines[:5]):
                dl_surf = self.font_body.render(dl, True, COLOR_TEXT)
                surface.blit(dl_surf, (detail_x + 6, detail_y + 36 + dy_idx * 13))

            # Instrucción de uso
            if cur_item.get("id") == "potion":
                use_hint = self.font_body.render("[ENTER / U] Beber poción", True, COLOR_HP_GREEN)
                surface.blit(use_hint, (detail_x + 6, detail_y + detail_h - 18))

        # 6. Mensaje de estado (inferior)
        if self.status_message:
            msg_surf = self.font_body.render(self.status_message, True, COLOR_HP_GREEN)
            surface.blit(msg_surf, (self.x + 14, self.y + self.height - 24))
        else:
            hint_surf = self.font_body.render("[W/S o Flechas] Navegar | [I o ESC] Cerrar", True, COLOR_TEXT_MUTED)
            surface.blit(hint_surf, (self.x + 14, self.y + self.height - 22))
