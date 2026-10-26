"""
game/settings.py
Constantes globales, configuraciones de pantalla, colores y controles del juego.
"""
import os
import pygame

# Título y metadatos
TITLE = "Crónicas de Brumavalle: La Llama Antigua"
SUBTITLE = "Un RPG medieval clásico en 2D"
AUTHOR = "Eric Fabricio García García"
VERSION = "1.0.0"

# Dimensiones de pantalla
# Resolución virtual interna para estética pixel art nítida (16:9)
VIRTUAL_WIDTH = 480
VIRTUAL_HEIGHT = 270

# Escala inicial y tamaño de la ventana
WINDOW_SCALE = 2  # 960 x 540
WINDOW_WIDTH = VIRTUAL_WIDTH * WINDOW_SCALE
WINDOW_HEIGHT = VIRTUAL_HEIGHT * WINDOW_SCALE

FPS = 60
TILE_SIZE = 16

# Rutas de carpetas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
DATA_DIR = os.path.join(BASE_DIR, "data")
SAVE_FILE_PATH = os.path.join(DATA_DIR, "savegame.json")

# Paleta de colores retro (16-bit)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BG_DARK = (16, 20, 28)
COLOR_UI_BG = (22, 26, 36)
COLOR_UI_BORDER = (196, 164, 102)
COLOR_UI_BORDER_DARK = (112, 88, 48)
COLOR_TEXT = (240, 235, 224)
COLOR_TEXT_MUTED = (160, 155, 145)
COLOR_TEXT_GOLD = (255, 215, 0)
COLOR_HP_GREEN = (46, 204, 113)
COLOR_HP_RED = (214, 48, 49)
COLOR_HP_DARK = (70, 20, 20)
COLOR_MANA_BLUE = (52, 152, 219)
COLOR_SLIME_PURPLE = (142, 68, 173)
COLOR_SHADOW = (10, 10, 15, 120)

# Colores de entorno
COLOR_GRASS = (58, 125, 68)
COLOR_DARK_GRASS = (43, 94, 52)
COLOR_DIRT_PATH = (168, 134, 94)
COLOR_COBBLESTONE = (130, 135, 140)
COLOR_WATER = (44, 120, 190)
COLOR_WATER_DEEP = (28, 80, 140)
COLOR_WOOD_WALL = (110, 72, 42)
COLOR_WOOD_ROOF = (142, 60, 40)
COLOR_STONE_WALL = (88, 92, 100)
COLOR_DUNGEON_FLOOR = (60, 64, 72)

# Teclas y controles
KEY_UP = [pygame.K_w, pygame.K_UP]
KEY_DOWN = [pygame.K_s, pygame.K_DOWN]
KEY_LEFT = [pygame.K_a, pygame.K_LEFT]
KEY_RIGHT = [pygame.K_d, pygame.K_RIGHT]
KEY_INTERACT = [pygame.K_e]
KEY_ATTACK = [pygame.K_SPACE]
KEY_INVENTORY = [pygame.K_i]
KEY_QUEST_LOG = [pygame.K_j]
KEY_PAUSE = [pygame.K_ESCAPE]
KEY_CONFIRM = [pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_e]
