"""
game/map_data.py
Diseño del mapa del mundo (Brumavalle, Bosque Susurrante y Ruinas de Kal-Drakor).
Define capas de suelo, obstáculos sólidos, colisiones y ubicaciones de entidades.
"""
import pygame
from game.settings import TILE_SIZE


class WorldMap:
    """Gestiona los tiles, colisiones, objetos decorativos e interactuables del mapa."""

    def __init__(self, asset_loader):
        self.assets = asset_loader
        self.width_tiles = 60
        self.height_tiles = 40
        self.pixel_width = self.width_tiles * TILE_SIZE
        self.pixel_height = self.height_tiles * TILE_SIZE

        # Cuadrículas de tiles (filas x columnas)
        self.ground_grid = []
        self.overlay_grid = []
        self.collision_rects = []
        self.interactables = []
        self.animated_torches = []

        # Estado del cofre y del altar
        self.chest_opened = False
        self.relic_taken = False

        self._build_map()

    def _build_map(self):
        """Construye las zonas del mapa de forma procedural y estructurada."""
        # Inicializar cuadrículas con None
        self.ground_grid = [[None for _ in range(self.width_tiles)] for _ in range(self.height_tiles)]
        self.overlay_grid = [[None for _ in range(self.width_tiles)] for _ in range(self.height_tiles)]
        self.collision_rects = []
        self.interactables = []
        self.animated_torches = []

        # ----------------------------------------------------
        # 1. GENERACIÓN DEL SUELO BASE
        # ----------------------------------------------------
        for y in range(self.height_tiles):
            for x in range(self.width_tiles):
                if x < 22:
                    # Región de Brumavalle (Pueblo)
                    # Caminos empedrados principales
                    if (10 <= y <= 12) or (8 <= x <= 10 and 4 <= y <= 26):
                        self.ground_grid[y][x] = "cobblestone"
                    elif (x + y) % 7 == 0:
                        self.ground_grid[y][x] = "grass_flowers"
                    else:
                        self.ground_grid[y][x] = "grass"
                elif x < 42:
                    # Bosque Susurrante
                    # Río que cruza el bosque en x=30, x=31
                    if x in (30, 31):
                        # Puente de madera en y=10..12
                        if 10 <= y <= 12:
                            self.ground_grid[y][x] = "bridge"
                        else:
                            self.ground_grid[y][x] = "water_0"
                    elif (10 <= y <= 12 and 22 <= x <= 42) or (24 <= y <= 26 and 32 <= x <= 39):
                        # Sendero de tierra
                        self.ground_grid[y][x] = "dirt"
                    elif (x * 3 + y * 5) % 11 == 0:
                        self.ground_grid[y][x] = "grass_flowers"
                    else:
                        self.ground_grid[y][x] = "grass"
                else:
                    # Ruinas de Kal-Drakor
                    self.ground_grid[y][x] = "ruins_floor"

        # Bordes exteriores impenetrables (árboles densos y muros de ruina)
        for x in range(self.width_tiles):
            self._set_solid(x, 0, "tree" if x < 42 else "stone_wall")
            self._set_solid(x, self.height_tiles - 1, "tree" if x < 42 else "stone_wall")
        for y in range(self.height_tiles):
            self._set_solid(0, y, "tree")
            self._set_solid(self.width_tiles - 1, y, "stone_wall")

        # ----------------------------------------------------
        # 2. CONSTRUCCIONES EN BRUMAVALLE (PUEBLO)
        # ----------------------------------------------------
        # Casa 1: Puesto de Guardia de Valeria (noroeste)
        self._build_building(3, 3, 5, 4, "Casa de la Guardia")
        # Casa 2: Herrería de Torin (suroeste con yunque/forja)
        self._build_building(3, 16, 5, 4, "Herrería de Torin")
        # Casa 3: Cabaña del Pueblo (centro-sur)
        self._build_building(13, 16, 5, 4, "Cabaña de Aldeano")

        # Vallas decorativas y jardines en el pueblo
        for x in range(2, 8):
            self._set_solid(x, 8, "fence")
        for y in range(8, 10):
            self._set_solid(8, y, "fence")

        for x in range(2, 8):
            self._set_solid(x, 21, "fence")

        # Antorchas en el pueblo
        self._add_torch(7, 10)
        self._add_torch(11, 10)
        self._add_torch(2, 4)
        self._add_torch(2, 17)

        # Cartel del pueblo
        self.interactables.append({
            "type": "sign",
            "rect": pygame.Rect(11 * TILE_SIZE, 9 * TILE_SIZE, TILE_SIZE, TILE_SIZE),
            "text": "Cartel de Brumavalle: 'Al este yace el Bosque Susurrante y las prohibidas Ruinas de Kal-Drakor.'",
            "name": "Cartel de Madera"
        })

        # ----------------------------------------------------
        # 3. BOSQUE SUSURRANTE (ÁRBOLES, RÍO Y SANTUARIO DE ELIRA)
        # ----------------------------------------------------
        # Árboles densos formando barreras naturales
        forest_trees = [
            (23, 3), (24, 3), (25, 4), (23, 7), (24, 8),
            (26, 14), (27, 15), (28, 16), (29, 17), (29, 18),
            (24, 20), (25, 22), (26, 24), (27, 26), (28, 28),
            (33, 4), (34, 5), (35, 6), (36, 4), (37, 5),
            (34, 15), (35, 16), (36, 17), (37, 18),
            (33, 22), (34, 23), (35, 25), (38, 22), (39, 23),
            (25, 30), (26, 31), (27, 32), (34, 31), (35, 32),
        ]
        for tx, ty in forest_trees:
            self._set_solid(tx, ty, "tree")

        # Santuario místico de Elira en el claro del bosque (x=36, y=8)
        # Columnas rúnicas rodeando su altar
        self._set_solid(35, 7, "pillar")
        self._set_solid(38, 7, "pillar")
        self._add_torch(35, 9)
        self._add_torch(38, 9)

        # Cofre secreto en el bosque (con pociones curativas)
        chest_rect = pygame.Rect(28 * TILE_SIZE, 6 * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.overlay_grid[6][28] = "chest_closed"
        self.collision_rects.append(chest_rect)
        self.interactables.append({
            "type": "chest",
            "rect": chest_rect,
            "x": 28,
            "y": 6,
            "item": "potion",
            "amount": 2,
            "name": "Cofre del Bosque"
        })

        # ----------------------------------------------------
        # 4. RUINAS DE KAL-DRAKOR (MUROS, COLUMNAS, GUARDIÁN Y ALTAR)
        # ----------------------------------------------------
        # Muro de entrada a las ruinas (x=42) con un arco de entrada en y=11
        for y in range(1, self.height_tiles - 1):
            if y not in (10, 11, 12):
                self._set_solid(42, y, "stone_wall")

        # Columnas del corredor de las ruinas
        ruin_pillars = [
            (45, 8), (48, 8), (51, 8), (54, 8),
            (45, 14), (48, 14), (51, 14), (54, 14),
            (46, 20), (50, 20), (54, 20),
            (46, 26), (50, 26), (54, 26),
        ]
        for px, py in ruin_pillars:
            self._set_solid(px, py, "pillar")

        # Antorchas místicas en las ruinas
        self._add_torch(43, 9)
        self._add_torch(43, 13)
        self._add_torch(51, 10)
        self._add_torch(57, 10)
        self._add_torch(51, 16)
        self._add_torch(57, 16)

        # Altar de la Llama Antigua en la cámara principal (x=55, y=11)
        altar_rect = pygame.Rect(55 * TILE_SIZE, 11 * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.overlay_grid[11][55] = "altar"
        self.collision_rects.append(altar_rect)
        self.interactables.append({
            "type": "altar",
            "rect": altar_rect,
            "x": 55,
            "y": 11,
            "name": "Altar de la Llama Antigua"
        })

    def _set_solid(self, x, y, tile_type):
        """Coloca un tile sólido y agrega su rectángulo a colisiones."""
        if 0 <= x < self.width_tiles and 0 <= y < self.height_tiles:
            self.overlay_grid[y][x] = tile_type
            self.collision_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    def _add_torch(self, x, y):
        """Agrega una antorcha animada."""
        if 0 <= x < self.width_tiles and 0 <= y < self.height_tiles:
            self.overlay_grid[y][x] = "torch_0"
            self.animated_torches.append((x, y))

    def _build_building(self, start_x, start_y, width, height, label):
        """Construye una cabaña con tejado, paredes, ventana y puerta con colisión."""
        for dy in range(height):
            for dx in range(width):
                gx = start_x + dx
                gy = start_y + dy
                if dy == 0:
                    self._set_solid(gx, gy, "roof")
                elif dy == 1:
                    if dx == 1 or dx == width - 2:
                        self._set_solid(gx, gy, "window")
                    else:
                        self._set_solid(gx, gy, "wood_wall")
                else:
                    if dy == height - 1 and dx == width // 2:
                        # Puerta de entrada (permite pararse enfrente)
                        self.overlay_grid[gy][gx] = "door"
                    else:
                        self._set_solid(gx, gy, "wood_wall")

    def update_animations(self, anim_frame):
        """Alterna frames de antorchas y agua según el tick de animación."""
        torch_sprite = f"torch_{anim_frame % 2}"
        water_sprite = f"water_{anim_frame % 2}"

        # Actualizar antorchas
        for tx, ty in self.animated_torches:
            self.overlay_grid[ty][tx] = torch_sprite

        # Actualizar tiles de agua
        for y in range(self.height_tiles):
            for x in (30, 31):
                if self.ground_grid[y][x] and self.ground_grid[y][x].startswith("water_"):
                    self.ground_grid[y][x] = water_sprite

    def open_chest(self, chest_data):
        """Abre un cofre y actualiza su sprite visual a cofre abierto."""
        x, y = chest_data["x"], chest_data["y"]
        self.overlay_grid[y][x] = "chest_open"
        self.chest_opened = True

    def remove_relic_from_altar(self):
        """Quita la reliquia del altar una vez reclamada."""
        self.relic_taken = True

    def draw_ground(self, surface, camera):
        """Dibuja la capa inferior de suelo visible por la cámara."""
        start_col = max(0, camera.rect.left // TILE_SIZE)
        end_col = min(self.width_tiles, (camera.rect.right // TILE_SIZE) + 1)
        start_row = max(0, camera.rect.top // TILE_SIZE)
        end_row = min(self.height_tiles, (camera.rect.bottom // TILE_SIZE) + 1)

        for y in range(start_row, end_row):
            for x in range(start_col, end_col):
                tile_name = self.ground_grid[y][x]
                if tile_name and tile_name in self.assets.tiles:
                    surface.blit(
                        self.assets.tiles[tile_name],
                        camera.apply_pos(x * TILE_SIZE, y * TILE_SIZE)
                    )

    def draw_overlay(self, surface, camera):
        """Dibuja obstáculos, edificios, vallas, antorchas y decoraciones."""
        start_col = max(0, camera.rect.left // TILE_SIZE)
        end_col = min(self.width_tiles, (camera.rect.right // TILE_SIZE) + 1)
        start_row = max(0, camera.rect.top // TILE_SIZE)
        end_row = min(self.height_tiles, (camera.rect.bottom // TILE_SIZE) + 1)

        for y in range(start_row, end_row):
            for x in range(start_col, end_col):
                tile_name = self.overlay_grid[y][x]
                if not tile_name:
                    continue

                screen_pos = camera.apply_pos(x * TILE_SIZE, y * TILE_SIZE)

                if tile_name == "tree":
                    # Árbol ocupa 2 tiles: copa arriba y tronco
                    surface.blit(self.assets.tiles["tree_trunk"], screen_pos)
                    surface.blit(self.assets.tiles["tree_top"], (screen_pos[0], screen_pos[1] - 8))
                elif tile_name in self.assets.tiles:
                    surface.blit(self.assets.tiles[tile_name], screen_pos)
