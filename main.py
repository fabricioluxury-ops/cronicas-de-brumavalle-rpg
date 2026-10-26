"""
main.py
Punto de entrada principal para "Crónicas de Brumavalle: La Llama Antigua".
Configura el motor Pygame, la resolución virtual escalada a ventana retro,
el bucle de eventos a 60 FPS y la máquina de estados completa.
"""
import sys
import os

# Asegurar que el directorio del proyecto esté en sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import pygame
from game.settings import (
    TITLE, VIRTUAL_WIDTH, VIRTUAL_HEIGHT, WINDOW_WIDTH,
    WINDOW_HEIGHT, FPS
)
from game.states.state_machine import StateMachine
from game.states.loading_state import LoadingState
from game.states.menu_state import MenuState
from game.states.intro_state import IntroState
from game.states.play_state import PlayState
from game.states.pause_state import PauseState
from game.states.options_state import OptionsState
from game.states.credits_state import CreditsState
from game.states.game_over_state import GameOverState
from game.states.victory_state import VictoryState


def initialize_fonts():
    """Inicializa fuentes pixeladas y del sistema de forma segura."""
    pygame.font.init()
    # Usar fuente predeterminada del sistema garantizada en cualquier plataforma
    fonts = {
        "small": pygame.font.Font(None, 14),
        "medium": pygame.font.Font(None, 18),
        "large": pygame.font.Font(None, 24),
    }
    return fonts


def main():
    """Función principal de inicio del videojuego."""
    # 1. Inicialización de Pygame
    pygame.init()
    pygame.display.set_caption(TITLE)

    # 2. Configuración de ventanas y superficies
    # Ventana visible escalada
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    # Superficie virtual interna de baja resolución para estética pixel art nítida
    virtual_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

    clock = pygame.time.Clock()
    fonts = initialize_fonts()

    # 3. Inicialización de la máquina de estados
    state_machine = StateMachine()

    # Registro de todas las fases y pantallas del juego
    state_machine.register("loading", LoadingState(state_machine, fonts))
    state_machine.register("menu", MenuState(state_machine, fonts))
    state_machine.register("intro", IntroState(state_machine, fonts))
    state_machine.register("play", PlayState(state_machine, fonts))
    state_machine.register("pause", PauseState(state_machine, fonts))
    state_machine.register("options", OptionsState(state_machine, fonts))
    state_machine.register("credits", CreditsState(state_machine, fonts))
    state_machine.register("game_over", GameOverState(state_machine, fonts))
    state_machine.register("victory", VictoryState(state_machine, fonts))

    # Comenzar con la pantalla animada de carga
    state_machine.change_state("loading")

    # 4. Bucle principal de ejecución (Game Loop)
    running = True
    while running:
        # A. Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            state_machine.handle_event(event)

        if not running:
            break

        # B. Actualización de lógica del estado activo
        state_machine.update()

        # C. Renderizado en superficie virtual
        virtual_surface.fill((0, 0, 0))
        state_machine.draw(virtual_surface)

        # D. Escalado nítido a la ventana real
        scaled_surface = pygame.transform.scale(virtual_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
        window.blit(scaled_surface, (0, 0))

        pygame.display.flip()
        clock.tick(FPS)

    # 5. Cierre seguro de subsistemas
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
