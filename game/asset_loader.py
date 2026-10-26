"""
game/asset_loader.py
Generador y cargador de recursos visuales y sprites en estilo pixel art 16-bit original.
Crea todos los sprites del jugador, NPCs, enemigos, tiles, iconos y retratos por código
y los guarda en disco en assets/images/ para cumplir con la originalidad absoluta.
"""
import os
import pygame
from game.settings import IMAGES_DIR, TILE_SIZE


def draw_pixel_grid(surf, ox, oy, grid, pal):
    """Dibuja una cuadrícula de caracteres asignados a colores en la paleta."""
    for r, line in enumerate(grid):
        for c, ch in enumerate(line):
            if ch in pal and pal[ch] is not None:
                surf.set_at((ox + c, oy + r), pal[ch])


class AssetLoader:
    """Genera, administra y suministra todos los sprites del juego."""

    def __init__(self):
        self.sprites = {}
        self.portraits = {}
        self.tiles = {}
        self.icons = {}

    def initialize_all(self):
        """Genera y carga todos los recursos del juego."""
        self._generate_tiles()
        self._generate_player_sprites()
        self._generate_npc_sprites()
        self._generate_enemy_sprites()
        self._generate_item_icons()
        self._generate_portraits()
        self._export_to_disk()

    # ==========================================
    # GENERACIÓN DE TILES DEL MUNDO
    # ==========================================
    def _generate_tiles(self):
        # 1. Pasto base
        t_grass = pygame.Surface((TILE_SIZE, TILE_SIZE))
        t_grass.fill((58, 125, 68))
        pal_grass = {
            'D': (45, 102, 53),
            'L': (76, 150, 88),
            'F': (240, 210, 80),   # Pequeña flor amarilla
            'W': (240, 240, 240),  # Pétalo blanco
        }
        grid_grass = [
            "................",
            "...D............",
            "........L.......",
            "....D.......D...",
            ".........D......",
            "..L.............",
            ".......D...L....",
            "................",
            "....L.......D...",
            ".......D........",
            "..D.............",
            "........L.......",
            ".............D..",
            "....D...L.......",
            "..L.............",
            "................",
        ]
        draw_pixel_grid(t_grass, 0, 0, grid_grass, pal_grass)
        self.tiles["grass"] = t_grass

        # 1b. Pasto con flores
        t_grass_flowers = t_grass.copy()
        grid_flowers = [
            "................",
            ".....WFW........",
            "......W.........",
            "................",
            "...........WFW..",
            "............W...",
            "................",
            "................",
            "................",
            "...WFW..........",
            "....W...........",
            "................",
            "..........WFW...",
            "...........W....",
            "................",
            "................",
        ]
        draw_pixel_grid(t_grass_flowers, 0, 0, grid_flowers, pal_grass)
        self.tiles["grass_flowers"] = t_grass_flowers

        # 2. Camino de tierra
        t_dirt = pygame.Surface((TILE_SIZE, TILE_SIZE))
        t_dirt.fill((168, 134, 94))
        pal_dirt = {
            'D': (138, 106, 70),
            'L': (190, 156, 114),
            'S': (110, 82, 52),
        }
        grid_dirt = [
            "..D........L....",
            "......L.D.......",
            ".L..........S...",
            ".....S...L......",
            "...L........D...",
            ".D......S.......",
            "....L.......L...",
            ".......D........",
            "..S........L....",
            ".....L...D......",
            ".L..........S...",
            "....D...L.......",
            ".......S....D...",
            "..L.............",
            ".....D...L......",
            "..S.........L...",
        ]
        draw_pixel_grid(t_dirt, 0, 0, grid_dirt, pal_dirt)
        self.tiles["dirt"] = t_dirt

        # 3. Adoquín de piedra de pueblo (Cobblestone)
        t_cobble = pygame.Surface((TILE_SIZE, TILE_SIZE))
        t_cobble.fill((125, 130, 135))
        pal_cobble = {
            'L': (165, 170, 175),
            'D': (85, 90, 95),
            'S': (55, 60, 65),
        }
        grid_cobble = [
            "LLLLD..LLLLD.LLD",
            "L...D..L...D.L.D",
            "DDDDD..DDDDD.DDD",
            "SSSSSS.SSSSSS.SS",
            "..LLLLD..LLLLD..",
            "..L...D..L...D..",
            "..DDDDD..DDDDD..",
            "..SSSSSS.SSSSSS.",
            "LLLLD..LLLLD.LLD",
            "L...D..L...D.L.D",
            "DDDDD..DDDDD.DDD",
            "SSSSSS.SSSSSS.SS",
            "..LLLLD..LLLLD..",
            "..L...D..L...D..",
            "..DDDDD..DDDDD..",
            "..SSSSSS.SSSSSS.",
        ]
        draw_pixel_grid(t_cobble, 0, 0, grid_cobble, pal_cobble)
        self.tiles["cobblestone"] = t_cobble

        # 4. Suelo de ruinas oscuras
        t_ruins_floor = pygame.Surface((TILE_SIZE, TILE_SIZE))
        t_ruins_floor.fill((65, 70, 78))
        pal_ruins_floor = {
            'D': (45, 50, 58),
            'L': (85, 90, 100),
            'C': (35, 38, 45),  # Grieta
        }
        grid_ruins_floor = [
            "................",
            "...L............",
            "....CC..........",
            ".....C..........",
            "......C.........",
            ".......CC.......",
            ".........C...D..",
            ".........C......",
            "..D......CC.....",
            "..........C.....",
            "..........C..L..",
            "................",
            "...L........D...",
            "......D.........",
            "................",
            "................",
        ]
        draw_pixel_grid(t_ruins_floor, 0, 0, grid_ruins_floor, pal_ruins_floor)
        self.tiles["ruins_floor"] = t_ruins_floor

        # 5. Muro de piedra de pueblo / ruinas
        t_wall = pygame.Surface((TILE_SIZE, TILE_SIZE))
        t_wall.fill((88, 92, 100))
        pal_wall = {
            'L': (130, 135, 145),
            'D': (55, 58, 65),
            'B': (35, 38, 45),
        }
        grid_wall = [
            "LLLLLLLLLLLLLLLL",
            "L..............D",
            "L..............D",
            "DDDDDDDDDDDDDDDD",
            "BBBBBBBBBBBBBBBB",
            "LLLLLLL..LLLLLLL",
            "L.....D..L.....D",
            "DDDDDDD..DDDDDDD",
            "BBBBBBB..BBBBBBB",
            "LLLLLLLLLLLLLLLL",
            "L..............D",
            "L..............D",
            "DDDDDDDDDDDDDDDD",
            "BBBBBBBBBBBBBBBB",
            "LLLLLLL..LLLLLLL",
            "DDDDDDD..DDDDDDD",
        ]
        draw_pixel_grid(t_wall, 0, 0, grid_wall, pal_wall)
        self.tiles["stone_wall"] = t_wall

        # 6. Pared de madera de cabaña
        t_wood = pygame.Surface((TILE_SIZE, TILE_SIZE))
        t_wood.fill((115, 76, 46))
        pal_wood = {
            'L': (148, 104, 68),
            'D': (80, 50, 28),
            'S': (55, 32, 16),
        }
        grid_wood = [
            "LLLLLLLLLLLLLLLL",
            "................",
            "DDDDDDDDDDDDDDDD",
            "SSSSSSSSSSSSSSSS",
            "LLLLLLLLLLLLLLLL",
            "................",
            "DDDDDDDDDDDDDDDD",
            "SSSSSSSSSSSSSSSS",
            "LLLLLLLLLLLLLLLL",
            "................",
            "DDDDDDDDDDDDDDDD",
            "SSSSSSSSSSSSSSSS",
            "LLLLLLLLLLLLLLLL",
            "................",
            "DDDDDDDDDDDDDDDD",
            "SSSSSSSSSSSSSSSS",
        ]
        draw_pixel_grid(t_wood, 0, 0, grid_wood, pal_wood)
        self.tiles["wood_wall"] = t_wood

        # 7. Tejado de tejas rojas
        t_roof = pygame.Surface((TILE_SIZE, TILE_SIZE))
        t_roof.fill((145, 60, 42))
        pal_roof = {
            'L': (178, 88, 66),
            'D': (105, 38, 24),
            'S': (72, 22, 12),
        }
        grid_roof = [
            "LLLLLLLLLLLLLLLL",
            "................",
            "DDDDDDDDDDDDDDDD",
            "SSSSSSSSSSSSSSSS",
            "LLLL.LLLL.LLLL.L",
            ".... ..... ... .",
            "DDDD.DDDD.DDDD.D",
            "SSSS.SSSS.SSSS.S",
            "LLLLLLLLLLLLLLLL",
            "................",
            "DDDDDDDDDDDDDDDD",
            "SSSSSSSSSSSSSSSS",
            ".LLLL.LLLL.LLLL.",
            " ....  ...  ... ",
            ".DDDD.DDDD.DDDD.",
            ".SSSS.SSSS.SSSS.",
        ]
        draw_pixel_grid(t_roof, 0, 0, grid_roof, pal_roof)
        self.tiles["roof"] = t_roof

        # 8. Agua con ondas
        t_water1 = pygame.Surface((TILE_SIZE, TILE_SIZE))
        t_water1.fill((44, 120, 190))
        t_water2 = pygame.Surface((TILE_SIZE, TILE_SIZE))
        t_water2.fill((44, 120, 190))
        pal_water = {
            'L': (130, 200, 240),
            'D': (28, 80, 145),
        }
        grid_water1 = [
            "................",
            "....LLLL........",
            "....DDDD........",
            "................",
            "..........LLLL..",
            "..........DDDD..",
            "................",
            "..LLLL..........",
            "..DDDD..........",
            "................",
            "........LLLL....",
            "........DDDD....",
            "................",
            "....LLLL........",
            "....DDDD........",
            "................",
        ]
        grid_water2 = [
            "................",
            "..........LLLL..",
            "..........DDDD..",
            "................",
            "....LLLL........",
            "....DDDD........",
            "................",
            "........LLLL....",
            "........DDDD....",
            "................",
            "..LLLL..........",
            "..DDDD..........",
            "................",
            "..........LLLL..",
            "..........DDDD..",
            "................",
        ]
        draw_pixel_grid(t_water1, 0, 0, grid_water1, pal_water)
        draw_pixel_grid(t_water2, 0, 0, grid_water2, pal_water)
        self.tiles["water_0"] = t_water1
        self.tiles["water_1"] = t_water2

        # 9. Puente de madera sobre agua
        t_bridge = pygame.Surface((TILE_SIZE, TILE_SIZE))
        t_bridge.fill((132, 90, 52))
        pal_bridge = {
            'L': (168, 120, 78),
            'D': (92, 60, 32),
            'R': (65, 40, 20),  # Clavos
        }
        grid_bridge = [
            "RRRRRRRRRRRRRRRR",
            "LLLLLLLLLLLLLLLL",
            "................",
            "DDDDDDDDDDDDDDDD",
            "LLLLLLLLLLLLLLLL",
            "................",
            "DDDDDDDDDDDDDDDD",
            "LLLLLLLLLLLLLLLL",
            "................",
            "DDDDDDDDDDDDDDDD",
            "LLLLLLLLLLLLLLLL",
            "................",
            "DDDDDDDDDDDDDDDD",
            "LLLLLLLLLLLLLLLL",
            "................",
            "RRRRRRRRRRRRRRRR",
        ]
        draw_pixel_grid(t_bridge, 0, 0, grid_bridge, pal_bridge)
        self.tiles["bridge"] = t_bridge

        # 10. Copa y tronco de árbol (2 tiles: arriba copa 16x16, abajo tronco 16x16)
        t_tree_top = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pal_tree = {
            'G': (34, 112, 50),
            'L': (58, 160, 78),
            'D': (20, 75, 32),
            'T': (105, 68, 38),
            'S': (72, 44, 22),
        }
        grid_tree_top = [
            "......LLLL......",
            "....LLLLLLLL....",
            "...LLGGGGGGLL...",
            "..LLGGGGGGGGLL..",
            ".LLGGDDDDGGGGLL.",
            ".LGGDDDDDDGGGGLL",
            "LGGDDDDDDDDGGGGL",
            "LGGDDDDDDDDGGGGL",
            "LGGDDDDDDDDGGGGL",
            "LGGDDDDDDDDGGGGL",
            ".LGGDDDDDDGGGGLL",
            ".LLGGDDDDGGGGLL.",
            "..LLGGGGGGGGLL..",
            "...LLGGGGGGLL...",
            "....LLLLLLLL....",
            "......LLLL......",
        ]
        draw_pixel_grid(t_tree_top, 0, 0, grid_tree_top, pal_tree)
        self.tiles["tree_top"] = t_tree_top

        t_tree_trunk = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        grid_tree_trunk = [
            ".....GGGGGG.....",
            "....GGDDDDGG....",
            ".....TTTTTT.....",
            ".....TSSSS.....",
            ".....TTTTTT.....",
            ".....TSSSS.....",
            ".....TTTTTT.....",
            ".....TSSSS.....",
            ".....TTTTTT.....",
            ".....TSSSS.....",
            ".....TTTTTT.....",
            ".....TSSSS.....",
            "....TTTTTTTT....",
            "...TTSSSSSTTT...",
            "..TTSSSSSSSTT...",
            "................",
        ]
        draw_pixel_grid(t_tree_trunk, 0, 0, grid_tree_trunk, pal_tree)
        self.tiles["tree_trunk"] = t_tree_trunk

        # 11. Puerta de casa
        t_door = pygame.Surface((TILE_SIZE, TILE_SIZE))
        t_door.fill((115, 76, 46))
        pal_door = {
            'F': (65, 40, 20),
            'P': (95, 60, 35),
            'G': (240, 200, 80),  # Pomo dorado
        }
        grid_door = [
            "FFFFFFFFFFFFFFFF",
            "FPPPPPPPPPPPPPPF",
            "FPPPPPPPPPPPPPPF",
            "FPP..........PPF",
            "FPP..........PPF",
            "FPP...G......PPF",
            "FPP..........PPF",
            "FPPPPPPPPPPPPPPF",
            "FPPPPPPPPPPPPPPF",
            "FPP..........PPF",
            "FPP..........PPF",
            "FPP..........PPF",
            "FPP..........PPF",
            "FPPPPPPPPPPPPPPF",
            "FPPPPPPPPPPPPPPF",
            "FFFFFFFFFFFFFFFF",
        ]
        draw_pixel_grid(t_door, 0, 0, grid_door, pal_door)
        self.tiles["door"] = t_door

        # 12. Ventana con cristal
        t_window = pygame.Surface((TILE_SIZE, TILE_SIZE))
        t_window.fill((115, 76, 46))
        pal_window = {
            'F': (65, 40, 20),
            'G': (180, 220, 245),
            'D': (120, 160, 190),
            'L': (240, 250, 255),
        }
        grid_window = [
            "FFFFFFFFFFFFFFFF",
            "FLLLLLLFFLLLLLLF",
            "FLGGGGGFDFGGGGGF",
            "FLGGGGGFDFGGGGGF",
            "FLGGGGGFDFGGGGGF",
            "FLGGGGGFDFGGGGGF",
            "FFFFFFFFFFFFFFFF",
            "FFFFFFFFFFFFFFFF",
            "FLGGGGGFDFGGGGGF",
            "FLGGGGGFDFGGGGGF",
            "FLGGGGGFDFGGGGGF",
            "FLGGGGGFDFGGGGGF",
            "FDDDDDDFDFDDDDDF",
            "FFFFFFFFFFFFFFFF",
            "................",
            "................",
        ]
        draw_pixel_grid(t_window, 0, 0, grid_window, pal_window)
        self.tiles["window"] = t_window

        # 13. Columna de ruinas
        t_pillar = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pal_pillar = {
            'L': (180, 185, 195),
            'M': (130, 135, 145),
            'D': (80, 85, 95),
            'S': (50, 52, 60),
        }
        grid_pillar = [
            "..LLLLLLLLLLLL..",
            "..LMMMMMMMMMMD..",
            "..LMMMMMMMMMMD..",
            "...DDDDDDDDDDS..",
            "....LMMMMMMD....",
            "....LMMMMMMD....",
            "....LMMMMMMD....",
            "....LMMMMMMD....",
            "....LMMMMMMD....",
            "....LMMMMMMD....",
            "....LMMMMMMD....",
            "....LMMMMMMD....",
            "...LLLLLLLLLL...",
            "..LMMMMMMMMMMD..",
            "..LMMMMMMMMMMD..",
            "..DDDDDDDDDDDD..",
        ]
        draw_pixel_grid(t_pillar, 0, 0, grid_pillar, pal_pillar)
        self.tiles["pillar"] = t_pillar

        # 14. Valla de madera (Fence)
        t_fence = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pal_fence = {
            'L': (168, 124, 82),
            'M': (132, 94, 58),
            'D': (88, 58, 32),
        }
        grid_fence = [
            "..LM.....LM.....",
            "..MD.....MD.....",
            "LLLLLLLLLLLLLLLL",
            "MMMMMMMMMMMMMMMM",
            "DDDDDDDDDDDDDDDD",
            "..LM.....LM.....",
            "..MD.....MD.....",
            "LLLLLLLLLLLLLLLL",
            "MMMMMMMMMMMMMMMM",
            "DDDDDDDDDDDDDDDD",
            "..LM.....LM.....",
            "..MD.....MD.....",
            "..LM.....LM.....",
            "..MD.....MD.....",
            "..LM.....LM.....",
            "..MD.....MD.....",
        ]
        draw_pixel_grid(t_fence, 0, 0, grid_fence, pal_fence)
        self.tiles["fence"] = t_fence

        # 15. Antorcha encendida (2 frames de animación de fuego)
        pal_torch = {
            'W': (110, 72, 42),
            'I': (80, 50, 30),
            'R': (235, 75, 45),
            'O': (255, 150, 30),
            'Y': (255, 235, 90),
        }
        t_torch1 = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        grid_torch1 = [
            "................",
            ".......OO.......",
            "......OYYO......",
            ".....OYYYYO.....",
            ".....RYYYYR.....",
            "......RRRR......",
            ".......WW.......",
            ".......II.......",
            ".......WW.......",
            ".......II.......",
            ".......WW.......",
            ".......II.......",
            ".......WW.......",
            ".......II.......",
            "................",
            "................",
        ]
        t_torch2 = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        grid_torch2 = [
            "................",
            "......RO........",
            ".....ROYYO......",
            ".....OYYYYO.....",
            ".....RYYYYR.....",
            "......RRRR......",
            ".......WW.......",
            ".......II.......",
            ".......WW.......",
            ".......II.......",
            ".......WW.......",
            ".......II.......",
            ".......WW.......",
            ".......II.......",
            "................",
            "................",
        ]
        draw_pixel_grid(t_torch1, 0, 0, grid_torch1, pal_torch)
        draw_pixel_grid(t_torch2, 0, 0, grid_torch2, pal_torch)
        self.tiles["torch_0"] = t_torch1
        self.tiles["torch_1"] = t_torch2

        # 16. Pedestal / Altar de la Llama Antigua
        t_altar = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pal_altar = {
            'G': (255, 215, 0),
            'D': (180, 140, 20),
            'S': (90, 95, 105),
            'L': (150, 155, 165),
            'F': (52, 152, 219),  # Fuego sagrado azul/dorado
            'W': (240, 245, 255),
        }
        grid_altar = [
            "......FWF.......",
            ".....FFFFF......",
            ".....GGGGG......",
            "....GDDDDDG.....",
            ".....GGGGG......",
            "......DDD.......",
            "......LLL.......",
            ".....LLLLLL.....",
            ".....LSSSSM.....",
            ".....LLLLLL.....",
            "....LLLLLLLL....",
            "...LLSSSSSSLL...",
            "..LLLLLLLLLLLL..",
            ".LLSSSSSSSSSSLL.",
            ".SSSSSSSSSSSSSS.",
            "................",
        ]
        draw_pixel_grid(t_altar, 0, 0, grid_altar, pal_altar)
        self.tiles["altar"] = t_altar

        # 17. Cofre (Cerrado y Abierto)
        pal_chest = {
            'W': (150, 95, 45),
            'D': (95, 55, 25),
            'G': (255, 215, 0),
            'B': (40, 20, 10),
            'S': (30, 30, 35),
        }
        t_chest_c = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        grid_chest_c = [
            "................",
            "................",
            "...WWWWWWWWWW...",
            "..WWDDDDDDDDWW..",
            "..WWDGGGGGGDWW..",
            "..WWDDDDDDDDWW..",
            "..SSSSSSSSSSSS..",
            "..WWWWWWWWWWWW..",
            "..WWDDDGDDDDWW..",
            "..WWDGGGGDDDWW..",
            "..WWDDDGDDDDWW..",
            "..WWDDDDDDDDWW..",
            "..WWWWWWWWWWWW..",
            "..SSSSSSSSSSSS..",
            "................",
            "................",
        ]
        t_chest_o = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        grid_chest_o = [
            "...WWWWWWWWWW...",
            "..WWDDDDDDDDWW..",
            "..WWDGGGGGGDWW..",
            "..WWDDDDDDDDWW..",
            "....BBBBBBBB....",
            "....BGGGGGBB....",
            "..SSSSSSSSSSSS..",
            "..WWWWWWWWWWWW..",
            "..WWDDDDDDDDWW..",
            "..WWDDDDDDDDWW..",
            "..WWDDDDDDDDWW..",
            "..WWWWWWWWWWWW..",
            "..SSSSSSSSSSSS..",
            "................",
            "................",
            "................",
        ]
        draw_pixel_grid(t_chest_c, 0, 0, grid_chest_c, pal_chest)
        draw_pixel_grid(t_chest_o, 0, 0, grid_chest_o, pal_chest)
        self.tiles["chest_closed"] = t_chest_c
        self.tiles["chest_open"] = t_chest_o

    # ==========================================
    # GENERACIÓN DEL JUGADOR (4 DIRECCIONES x 3 FRAMES)
    # ==========================================
    def _generate_player_sprites(self):
        pal_player = {
            'H': (110, 60, 30),     # Cabello castaño oscuro
            'S': (245, 205, 175),   # Piel
            'E': (30, 30, 40),      # Ojos
            'T': (41, 128, 185),    # Túnica azul de aventurero
            'C': (52, 73, 94),      # Capa / acento
            'A': (189, 195, 199),   # Pechera / armadura acero
            'D': (127, 140, 141),   # Sombra acero
            'B': (95, 55, 25),      # Botas y cinturón
            'G': (241, 196, 15),    # Hebilla dorada
        }

        # Mirando abajo (Frame 0: reposo, Frame 1: paso izq, Frame 2: paso der)
        p_down_0 = [
            "......HHHH......",
            ".....HHHHHH.....",
            "....HHHHHHHH....",
            "....HSSSSHSS....",
            "....HSEESEHS....",
            "....HSSSSSSH....",
            ".....SSSSSS.....",
            "....AAATTAAA....",
            "...AATTGGAATTA..",
            "...AATTTTTTAAA..",
            "...AATTTTTTAAA..",
            "....DTTTTTTD....",
            "....DDTTTTDD....",
            "....BB....BB....",
            "...BBB....BBB...",
            "................",
        ]
        p_down_1 = [
            "......HHHH......",
            ".....HHHHHH.....",
            "....HHHHHHHH....",
            "....HSSSSHSS....",
            "....HSEESEHS....",
            "....HSSSSSSH....",
            ".....SSSSSS.....",
            "....AAATTAAA....",
            "...AATTGGAATTA..",
            "...AATTTTTTAAA..",
            "...AATTTTTTAAA..",
            "....DTTTTTTD....",
            "....DDTTTTDD....",
            "...BBB....BB....",
            "..BBBB.....B....",
            "................",
        ]
        p_down_2 = [
            "......HHHH......",
            ".....HHHHHH.....",
            "....HHHHHHHH....",
            "....HSSSSHSS....",
            "....HSEESEHS....",
            "....HSSSSSSH....",
            ".....SSSSSS.....",
            "....AAATTAAA....",
            "...AATTGGAATTA..",
            "...AATTTTTTAAA..",
            "...AATTTTTTAAA..",
            "....DTTTTTTD....",
            "....DDTTTTDD....",
            "....BB....BBB...",
            "....B.....BBBB..",
            "................",
        ]

        # Mirando arriba
        p_up_0 = [
            "......HHHH......",
            ".....HHHHHH.....",
            "....HHHHHHHH....",
            "....HHHHHHHH....",
            "....HHHHHHHH....",
            "....HHHHHHHH....",
            ".....CCCCCC.....",
            "....CCCCCCCA....",
            "...AACCCCCAA....",
            "...AACCCCCAA....",
            "...AACCCCCAA....",
            "....DCCCCCD.....",
            "....DDCCCDD.....",
            "....BB....BB....",
            "...BBB....BBB...",
            "................",
        ]
        p_up_1 = [
            "......HHHH......",
            ".....HHHHHH.....",
            "....HHHHHHHH....",
            "....HHHHHHHH....",
            "....HHHHHHHH....",
            "....HHHHHHHH....",
            ".....CCCCCC.....",
            "....CCCCCCCA....",
            "...AACCCCCAA....",
            "...AACCCCCAA....",
            "...AACCCCCAA....",
            "....DCCCCCD.....",
            "....DDCCCDD.....",
            "...BBB....BB....",
            "..BBBB.....B....",
            "................",
        ]
        p_up_2 = [
            "......HHHH......",
            ".....HHHHHH.....",
            "....HHHHHHHH....",
            "....HHHHHHHH....",
            "....HHHHHHHH....",
            "....HHHHHHHH....",
            ".....CCCCCC.....",
            "....CCCCCCCA....",
            "...AACCCCCAA....",
            "...AACCCCCAA....",
            "...AACCCCCAA....",
            "....DCCCCCD.....",
            "....DDCCCDD.....",
            "....BB....BBB...",
            "....B.....BBBB..",
            "................",
        ]

        # Mirando izquierda
        p_left_0 = [
            ".....HHHH.......",
            "....HHHHHH......",
            "...HHHHHHH......",
            "...HSSSSH.......",
            "...HSEESH.......",
            "...HSSSS........",
            "....SSSS........",
            "...AAATTT.......",
            "..AAATTGG.......",
            "..AAATTTT.......",
            "..AAATTTT.......",
            "...DDTTTD.......",
            "...DDTTTD.......",
            "....BB.BB.......",
            "...BBB.BBB......",
            "................",
        ]
        p_left_1 = [
            ".....HHHH.......",
            "....HHHHHH......",
            "...HHHHHHH......",
            "...HSSSSH.......",
            "...HSEESH.......",
            "...HSSSS........",
            "....SSSS........",
            "...AAATTT.......",
            "..AAATTGG.......",
            "..AAATTTT.......",
            "..AAATTTT.......",
            "...DDTTTD.......",
            "...DDTTTD.......",
            "....BBBB........",
            "...BBBB.........",
            "................",
        ]
        p_left_2 = [
            ".....HHHH.......",
            "....HHHHHH......",
            "...HHHHHHH......",
            "...HSSSSH.......",
            "...HSEESH.......",
            "...HSSSS........",
            "....SSSS........",
            "...AAATTT.......",
            "..AAATTGG.......",
            "..AAATTTT.......",
            "..AAATTTT.......",
            "...DDTTTD.......",
            "...DDTTTD.......",
            "......BBBB......",
            ".......BBBB.....",
            "................",
        ]

        # Generar dirección derecha reflejando izquierda
        frames_dict = {
            "down": [p_down_0, p_down_1, p_down_2],
            "up": [p_up_0, p_up_1, p_up_2],
            "left": [p_left_0, p_left_1, p_left_2],
        }

        self.sprites["player"] = {}
        for dir_name, grids in frames_dict.items():
            self.sprites["player"][dir_name] = []
            for g in grids:
                s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                draw_pixel_grid(s, 0, 0, g, pal_player)
                self.sprites["player"][dir_name].append(s)

        # Reflejo para derecha
        self.sprites["player"]["right"] = []
        for s in self.sprites["player"]["left"]:
            self.sprites["player"]["right"].append(pygame.transform.flip(s, True, False))

    # ==========================================
    # GENERACIÓN DE NPCS
    # ==========================================
    def _generate_npc_sprites(self):
        # 1. Valeria (Guardiana de Brumavalle) - Armadura plateada, capa escarlata
        pal_valeria = {
            'H': (220, 180, 80),    # Cabello rubio recogido
            'S': (245, 205, 175),   # Piel
            'E': (40, 90, 180),     # Ojos azules
            'A': (215, 220, 225),   # Armadura plateada reluciente
            'D': (140, 145, 155),   # Sombra metal
            'C': (192, 57, 43),     # Capa escarlata
            'B': (70, 75, 80),      # Botas de acero
            'G': (241, 196, 15),    # Detalles dorados
        }
        valeria_grid = [
            "......HHHH......",
            ".....HHHHHH.....",
            "....HHHHHHHH....",
            "....HSSSSHSS....",
            "....HSEESEHS....",
            "....HSSSSSSH....",
            ".....SSSSSS.....",
            "....AAAGAAAA....",
            "...CAAAAAACAC...",
            "..CCAAAAAACAC...",
            "..CCAAAAAACAC...",
            "...CDAAAADCC....",
            "...CDAAAADCC....",
            "....BB....BB....",
            "...BBB....BBB...",
            "................",
        ]
        s_val = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        draw_pixel_grid(s_val, 0, 0, valeria_grid, pal_valeria)
        self.sprites["npc_valeria"] = s_val

        # 2. Torin (El Herrero) - Delantal de cuero, barba tupida, martillo
        pal_torin = {
            'H': (50, 45, 45),      # Cabello y barba oscuros
            'S': (220, 175, 140),   # Piel tostada de forja
            'E': (20, 20, 20),      # Ojos
            'L': (140, 85, 45),     # Delantal de cuero
            'D': (90, 50, 25),      # Sombra cuero
            'T': (180, 180, 185),   # Camisa gris
            'M': (150, 150, 160),   # Martillo
            'B': (60, 40, 25),      # Botas pesadas
        }
        torin_grid = [
            ".....HHHHHH.....",
            "....HHHHHHHH....",
            "....HSSSSHSS....",
            "....HSEESEHS....",
            "....HHHHHHHH....",
            "....HHHHHHHH....",
            ".....HHHHHH.....",
            "...TTLLLLTTT....",
            "..TTTLLLLTTTM...",
            "..SSTLLLLTSSM...",
            "..SSTDDDDTSMM...",
            "....TLLLLT..M...",
            "....TDDDDT......",
            "....BB..BB......",
            "...BBB..BBB.....",
            "................",
        ]
        s_tor = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        draw_pixel_grid(s_tor, 0, 0, torin_grid, pal_torin)
        self.sprites["npc_torin"] = s_tor

        # 3. Elira (La Anciana Sabia) - Túnica mística violeta, báculo de madera
        pal_elira = {
            'H': (210, 215, 220),   # Cabello canoso
            'S': (235, 195, 170),   # Piel envejecida
            'E': (60, 120, 90),     # Ojos verdes profundos
            'R': (90, 45, 125),     # Túnica púrpura mística
            'D': (55, 25, 80),      # Sombra túnica
            'G': (241, 196, 15),    # Amuleto rúnico dorado
            'W': (120, 75, 40),     # Báculo de madera
            'C': (52, 152, 219),    # Cristal de báculo
        }
        elira_grid = [
            "....RRRRRRRR....",
            "...RRRRRRRRRR...",
            "...RHHHHHHHHR...",
            "...RHSSSSHSHR...",
            "...RHSEESEHHR...",
            "...RHSSSSSHHR.C.",
            "....RSSSSR..RWW.",
            "...RRRGGRRRR.WW.",
            "..RRRRGGRRRR.WW.",
            "..RRRRRRRRRR.WW.",
            "..RRRRRRRRRR.WW.",
            "..DDDDDDDDDD.WW.",
            "..DDDDDDDDDD.WW.",
            "...DDDDDDDD..WW.",
            "...DD....DD..WW.",
            "................",
        ]
        s_eli = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        draw_pixel_grid(s_eli, 0, 0, elira_grid, pal_elira)
        self.sprites["npc_elira"] = s_eli

    # ==========================================
    # GENERACIÓN DE ENEMIGOS
    # ==========================================
    def _generate_enemy_sprites(self):
        # 1. Slime Sombrío (Gota gelatinosa morada con ojos rojos luminosos)
        pal_slime = {
            'P': (142, 68, 173),
            'D': (92, 40, 115),
            'L': (187, 143, 206),
            'E': (231, 76, 60),    # Ojos rojos brillantes
            'W': (255, 255, 255),  # Brillo pupila
        }
        slime_f0 = [
            "................",
            "................",
            ".......LL.......",
            ".....LLLLLL.....",
            "....LLPPPPLL....",
            "...LLPPPPPPLL...",
            "..LLPPEPPEEPLL..",
            "..LLPPEPPEEPLL..",
            "..LPPPEWPEWPDD..",
            "..LPPPPPPPPPDD..",
            "..LPPPPPPPPPDD..",
            "..LPPPPPPPPPDD..",
            "...DPPPPPPPPD...",
            "...DDDDDDDDDD...",
            "................",
            "................",
        ]
        slime_f1 = [
            "................",
            "................",
            "................",
            "......LLLL......",
            "....LLLLLLLL....",
            "...LLPPPPPPLL...",
            "..LLPPEPPEEPLL..",
            ".LLLPPEPPEEPLLD.",
            ".LLPPPEWPEWPDDD.",
            ".LLPPPPPPPPPDDD.",
            ".LLPPPPPPPPPDDD.",
            "..DPPPPPPPPPDD..",
            "...DDDDDDDDDD...",
            "................",
            "................",
            "................",
        ]
        s_sli0 = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        s_sli1 = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        draw_pixel_grid(s_sli0, 0, 0, slime_f0, pal_slime)
        draw_pixel_grid(s_sli1, 0, 0, slime_f1, pal_slime)
        self.sprites["enemy_slime"] = [s_sli0, s_sli1]

        # 2. Guardián Sombrío (Miniboss de las Ruinas de Kal-Drakor)
        pal_guardian = {
            'A': (40, 42, 50),     # Armadura negra obsidiana
            'D': (20, 22, 28),     # Sombra oscura
            'L': (70, 75, 90),     # Brillo acero oscuro
            'E': (231, 76, 60),    # Ojos rojos demoníacos
            'C': (88, 24, 69),     # Capa carmesí oscura
            'S': (192, 57, 43),    # Espada sombría
            'G': (241, 196, 15),   # Emblema antiguo
        }
        guard_grid = [
            ".....LLAAAA.....",
            "....LLAAAAAA....",
            "...LLAAAAAAAA...",
            "...LLAEEEAEAA...",
            "...LLAEEEAEAA...",
            "...LLAAAAAAAA...",
            "....LLAAAAAA....",
            "...CCAAGAAACC.S.",
            "..CCCAAAAAACCCS.",
            "..CCCAAAAAACCCS.",
            "..CCCDAAAADCCCS.",
            "...CDDAAAADD.CS.",
            "...CDDAAAADD..S.",
            "....DDA..ADD....",
            "...DDD....DDD...",
            "................",
        ]
        s_guard = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        draw_pixel_grid(s_guard, 0, 0, guard_grid, pal_guardian)
        self.sprites["enemy_guardian"] = s_guard

    # ==========================================
    # GENERACIÓN DE ICONOS DE ITEMS
    # ==========================================
    def _generate_item_icons(self):
        # 1. Espada de Hierro
        pal_sword = {
            'B': (189, 195, 199),
            'D': (127, 140, 141),
            'H': (110, 72, 42),
            'G': (241, 196, 15),
            'W': (255, 255, 255),
        }
        sword_grid = [
            "..............WB",
            ".............WBD",
            "............WBD.",
            "...........WBD..",
            "..........WBD...",
            ".........WBD....",
            "........WBD.....",
            ".......WBD......",
            "......WBD.......",
            ".....WBD........",
            "....GGG.........",
            "...GHG..........",
            "..H.G...........",
            ".H..............",
            "G...............",
            "................",
        ]
        s_sword = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        draw_pixel_grid(s_sword, 0, 0, sword_grid, pal_sword)
        self.icons["sword"] = s_sword

        # 2. Poción de Vida
        pal_potion = {
            'C': (140, 95, 55),    # Corcho
            'G': (200, 230, 245),  # Vidrio frasco
            'R': (231, 76, 60),    # Líquido curativo rojo
            'D': (150, 30, 30),    # Sombra líquido
            'W': (255, 255, 255),  # Brillo frasco
        }
        potion_grid = [
            "......CCCC......",
            "......CCCC......",
            ".......GG.......",
            "......GGGG......",
            "....GGGGGGGG....",
            "...GGWRRRRRRGG..",
            "..GGWWRRRRRRRGG.",
            "..GGWWRRRRRRRGG.",
            "..GGWWRRRRRRDDG.",
            "..GGWWRRRRRRDDG.",
            "..GGWWRRRRRRDDG.",
            "..GGWWRRRRRRDDG.",
            "...GGWRRRRRRDDG.",
            "....GGDDDDDDGG..",
            "......GGGGGG....",
            "................",
        ]
        s_potion = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        draw_pixel_grid(s_potion, 0, 0, potion_grid, pal_potion)
        self.icons["potion"] = s_potion

        # 3. Reliquia de la Llama Antigua
        pal_relic = {
            'G': (241, 196, 15),
            'D': (180, 140, 20),
            'F': (52, 152, 219),
            'W': (230, 245, 255),
            'R': (231, 76, 60),
        }
        relic_grid = [
            ".......WW.......",
            "......FWWF......",
            ".....FFFFFF.....",
            "....FFFFFFFF....",
            "....FRFFFFRF....",
            "....FFRRRRFF....",
            "....GGGGGGGG....",
            "...GDDDDDDDDG...",
            "...GGGGGGGGGG...",
            "....GDDDDDDG....",
            ".....GGGGGG.....",
            "......GDDG......",
            ".....GGGGGG.....",
            "....GDDDDDDG....",
            "...GGGGGGGGGG...",
            "................",
        ]
        s_relic = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        draw_pixel_grid(s_relic, 0, 0, relic_grid, pal_relic)
        self.icons["relic"] = s_relic

    # ==========================================
    # GENERACIÓN DE RETRATOS (32x32)
    # ==========================================
    def _generate_portraits(self):
        # 1. Retrato de Valeria (32x32)
        p_val = pygame.Surface((32, 32))
        p_val.fill((30, 35, 45))
        # Fondo con marco
        pygame.draw.rect(p_val, (196, 164, 102), (0, 0, 32, 32), 1)
        # Cabello rubio
        pygame.draw.rect(p_val, (220, 180, 80), (8, 4, 16, 18))
        # Rostro
        pygame.draw.rect(p_val, (245, 205, 175), (10, 8, 12, 12))
        # Ojos
        p_val.set_at((12, 12), (40, 90, 180))
        p_val.set_at((19, 12), (40, 90, 180))
        # Armadura hombros y pecho
        pygame.draw.rect(p_val, (215, 220, 225), (6, 20, 20, 11))
        # Detalles dorados
        pygame.draw.line(p_val, (241, 196, 15), (15, 20), (16, 30))
        # Capa escarlata a los costados
        pygame.draw.rect(p_val, (192, 57, 43), (2, 22, 4, 9))
        pygame.draw.rect(p_val, (192, 57, 43), (26, 22, 4, 9))
        self.portraits["valeria"] = p_val

        # 2. Retrato de Torin (32x32)
        p_tor = pygame.Surface((32, 32))
        p_tor.fill((30, 35, 45))
        pygame.draw.rect(p_tor, (196, 164, 102), (0, 0, 32, 32), 1)
        # Cabello oscuro
        pygame.draw.rect(p_tor, (50, 45, 45), (8, 4, 16, 10))
        # Rostro
        pygame.draw.rect(p_tor, (220, 175, 140), (9, 8, 14, 11))
        # Ojos
        p_tor.set_at((12, 11), (20, 20, 20))
        p_tor.set_at((19, 11), (20, 20, 20))
        # Barba espesa
        pygame.draw.rect(p_tor, (50, 45, 45), (8, 15, 16, 9))
        # Camisa y delantal
        pygame.draw.rect(p_tor, (140, 85, 45), (6, 23, 20, 8))
        pygame.draw.rect(p_tor, (180, 180, 185), (2, 23, 4, 8))
        pygame.draw.rect(p_tor, (180, 180, 185), (26, 23, 4, 8))
        self.portraits["torin"] = p_tor

        # 3. Retrato de Elira (32x32)
        p_eli = pygame.Surface((32, 32))
        p_eli.fill((30, 35, 45))
        pygame.draw.rect(p_eli, (196, 164, 102), (0, 0, 32, 32), 1)
        # Capucha púrpura
        pygame.draw.rect(p_eli, (90, 45, 125), (6, 2, 20, 22))
        # Cabello canoso
        pygame.draw.rect(p_eli, (210, 215, 220), (9, 7, 14, 13))
        # Rostro anciana
        pygame.draw.rect(p_eli, (235, 195, 170), (10, 9, 12, 11))
        # Ojos verdes
        p_eli.set_at((13, 13), (60, 120, 90))
        p_eli.set_at((18, 13), (60, 120, 90))
        # Manto y amuleto
        pygame.draw.rect(p_eli, (90, 45, 125), (4, 21, 24, 10))
        pygame.draw.circle(p_eli, (241, 196, 15), (16, 24), 2)
        self.portraits["elira"] = p_eli

        # 4. Retrato del Jugador (Eric) (32x32)
        p_ply = pygame.Surface((32, 32))
        p_ply.fill((30, 35, 45))
        pygame.draw.rect(p_ply, (196, 164, 102), (0, 0, 32, 32), 1)
        # Cabello castaño
        pygame.draw.rect(p_ply, (110, 60, 30), (8, 4, 16, 12))
        # Rostro
        pygame.draw.rect(p_ply, (245, 205, 175), (9, 9, 14, 11))
        # Ojos
        p_ply.set_at((12, 13), (30, 30, 40))
        p_ply.set_at((19, 13), (30, 30, 40))
        # Túnica azul y armadura
        pygame.draw.rect(p_ply, (41, 128, 185), (6, 21, 20, 10))
        pygame.draw.rect(p_ply, (189, 195, 199), (10, 21, 12, 10))
        self.portraits["player"] = p_ply

    # ==========================================
    # EXPORTACIÓN A DISCO EN ASSETS/IMAGES
    # ==========================================
    def _export_to_disk(self):
        """Exporta todos los sprites generados a PNG para persistencia en el repositorio."""
        try:
            os.makedirs(IMAGES_DIR, exist_ok=True)
            for name, surf in self.tiles.items():
                pygame.image.save(surf, os.path.join(IMAGES_DIR, f"tile_{name}.png"))
            for name, surf in self.portraits.items():
                pygame.image.save(surf, os.path.join(IMAGES_DIR, f"portrait_{name}.png"))
            for name, surf in self.icons.items():
                pygame.image.save(surf, os.path.join(IMAGES_DIR, f"icon_{name}.png"))
            for name, surf in self.sprites.items():
                if isinstance(surf, pygame.Surface):
                    pygame.image.save(surf, os.path.join(IMAGES_DIR, f"sprite_{name}.png"))
                elif isinstance(surf, list):
                    for idx, s in enumerate(surf):
                        pygame.image.save(s, os.path.join(IMAGES_DIR, f"sprite_{name}_{idx}.png"))
                elif isinstance(surf, dict):
                    for subname, subval in surf.items():
                        if isinstance(subval, list):
                            for idx, s in enumerate(subval):
                                pygame.image.save(s, os.path.join(IMAGES_DIR, f"sprite_{name}_{subname}_{idx}.png"))
        except Exception as e:
            print(f"[Assets] Aviso al guardar imágenes en disco: {e}")


# Instancia global de recursos
assets = AssetLoader()
