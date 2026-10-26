"""
game/states/base_state.py
Clase base para todos los estados del juego.
"""


class BaseState:
    """Interfaz estándar que deben implementar todos los estados del juego."""

    def __init__(self, state_machine):
        self.state_machine = state_machine

    def enter(self, **kwargs):
        """Se ejecuta al entrar al estado."""
        pass

    def exit(self):
        """Se ejecuta al salir del estado."""
        pass

    def handle_event(self, event):
        """Procesa eventos de teclado, ratón o ventana."""
        pass

    def update(self):
        """Actualiza la lógica interna del estado."""
        pass

    def draw(self, surface):
        """Dibuja el estado sobre la superficie virtual."""
        pass
