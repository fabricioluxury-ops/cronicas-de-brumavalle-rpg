"""
game/states/state_machine.py
Máquina de estados con soporte para transiciones y pila de estados superpuestos (como Pausa).
"""
import pygame


class StateMachine:
    """Administra la transición y ejecución de estados del juego."""

    def __init__(self):
        self.states = {}
        self.state_stack = []

    def register(self, name, state_instance):
        """Registra un nuevo estado con una clave única."""
        self.states[name] = state_instance

    def change_state(self, name, **kwargs):
        """Limpia la pila y cambia al estado indicado."""
        if self.state_stack:
            self.state_stack[-1].exit()
            self.state_stack.clear()

        next_state = self.states.get(name)
        if next_state:
            self.state_stack.append(next_state)
            next_state.enter(**kwargs)

    def push_state(self, name, **kwargs):
        """Coloca un estado superpuesto (útil para menús de pausa sobre el juego activo)."""
        next_state = self.states.get(name)
        if next_state:
            self.state_stack.append(next_state)
            next_state.enter(**kwargs)

    def pop_state(self):
        """Retira el estado superior de la pila."""
        if self.state_stack:
            top = self.state_stack.pop()
            top.exit()

    @property
    def current_state(self):
        """Retorna el estado activo actual."""
        return self.state_stack[-1] if self.state_stack else None

    def handle_event(self, event):
        """Envía el evento al estado activo."""
        if self.state_stack:
            self.state_stack[-1].handle_event(event)

    def update(self):
        """Actualiza el estado activo."""
        if self.state_stack:
            self.state_stack[-1].update()

    def draw(self, surface):
        """Dibuja todos los estados en la pila (para que el fondo de pausa sea visible)."""
        for state in self.state_stack:
            state.draw(surface)
