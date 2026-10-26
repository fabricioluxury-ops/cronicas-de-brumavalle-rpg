"""
game/save_manager.py
Gestión de partidas guardadas en JSON y máquina de estados de la misión principal.
Incluye validación robusta y manejo de errores ante archivos ausentes o corruptos.
"""
import os
import json
from game.settings import DATA_DIR, SAVE_FILE_PATH, AUTHOR


class QuestManager:
    """Controla los pasos, objetivos e historial de la misión principal."""

    STAGES = {
        0: {
            "title": "La Niebla Sobre Brumavalle",
            "desc": "La Guardiana Valeria te ha pedido que consultes a la Sabia Elira en el claro del Bosque Susurrante.",
            "target": "Habla con la Sabia Elira en el bosque."
        },
        1: {
            "title": "El Despertar de las Sombras",
            "desc": "Elira reveló que la Llama Antigua está en las Ruinas de Kal-Drakor. Debes derrotar al Guardián de las Sombras.",
            "target": "Cruza al este y derrota al Guardián en las Ruinas de Kal-Drakor."
        },
        2: {
            "title": "El Altar del Fuego Sagrado",
            "desc": "El Guardián Sombrío ha caído. Ahora acércate al altar en el fondo de las ruinas y recoge la reliquia.",
            "target": "Recupera la Reliquia de la Llama Antigua del altar [E]."
        },
        3: {
            "title": "El Retorno de la Luz",
            "desc": "Tienes la Reliquia de la Llama Antigua. Regresa con la Guardiana Valeria a la entrada de Brumavalle.",
            "target": "Entrega la reliquia a la Guardiana Valeria en Brumavalle [E]."
        },
        4: {
            "title": "¡Salvador de Brumavalle!",
            "desc": "Has devuelto la Llama Antigua a la plaza del reino. Las sombras retrocedieron y la paz fue restaurada.",
            "target": "¡Misión completada con honores!"
        }
    }

    def __init__(self, current_stage=0):
        self.stage = current_stage

    def advance_to(self, new_stage):
        """Avanza la misión si la nueva etapa es superior."""
        if new_stage > self.stage:
            self.stage = new_stage

    def get_current_info(self):
        """Devuelve el título, descripción y objetivo actual."""
        return self.STAGES.get(self.stage, {
            "title": "Aventura en curso",
            "desc": "Explora el reino de Brumavalle.",
            "target": "Explora el mapa."
        })

    def is_completed(self):
        """Indica si la misión principal ha finalizado."""
        return self.stage >= 4


class SaveManager:
    """Guarda y carga el estado completo del juego en formato JSON."""

    @staticmethod
    def save_exists():
        """Comprueba si existe un archivo de partida guardada."""
        return os.path.exists(SAVE_FILE_PATH)

    @staticmethod
    def save_game(player, quest_manager, world_map, enemies):
        """Serializa la posición, salud, inventario, misión y enemigos derrotados."""
        try:
            os.makedirs(DATA_DIR, exist_ok=True)
            data = {
                "version": "1.0.0",
                "author": AUTHOR,
                "player": {
                    "name": player.name,
                    "x": player.x,
                    "y": player.y,
                    "hp": player.hp,
                    "max_hp": player.max_hp,
                    "direction": player.direction,
                    "inventory": player.inventory,
                },
                "quest": {
                    "stage": quest_manager.stage
                },
                "world": {
                    "chest_opened": world_map.chest_opened,
                    "relic_taken": world_map.relic_taken,
                },
                "enemies": {
                    e.id: {"is_alive": e.is_alive, "hp": e.hp}
                    for e in enemies
                }
            }
            # Escritura atómica mediante archivo temporal para evitar corrupción
            temp_path = SAVE_FILE_PATH + ".tmp"
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            os.replace(temp_path, SAVE_FILE_PATH)
            return True, "¡Partida guardada exitosamente en data/savegame.json!"
        except Exception as e:
            return False, f"Error al guardar la partida: {e}"

    @staticmethod
    def load_game():
        """Carga y valida los datos de la partida guardada con manejo seguro de fallos."""
        if not os.path.exists(SAVE_FILE_PATH):
            return None, "No se encontró ningún archivo de guardado previo."

        try:
            with open(SAVE_FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Validación básica de estructura requerida
            if not isinstance(data, dict) or "player" not in data or "quest" not in data:
                return None, "El archivo de partida guardada tiene un formato inválido o está incompleto."

            return data, "Partida cargada exitosamente."
        except json.JSONDecodeError:
            return None, "El archivo de guardado está corrupto. Comienza una Nueva Partida."
        except Exception as e:
            return None, f"Error inesperado al cargar la partida: {e}"
