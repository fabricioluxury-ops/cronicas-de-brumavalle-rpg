"""
game/entities/npc.py
Comportamiento y diálogos de los personajes no jugables (NPCs):
- Guardiana Valeria: Defensora de las puertas de Brumavalle.
- Torin el Herrero: Maestro forjador del pueblo.
- Elira la Sabia: Anciana del claro del bosque y guardiana del conocimiento antiguo.
"""
import pygame
from game.settings import TILE_SIZE, COLOR_TEXT_GOLD, COLOR_WHITE, COLOR_UI_BG


class NPC:
    """Clase base para personajes con diálogo, retrato e indicador de interacción."""

    def __init__(self, npc_id, name, title, x, y, sprite_key, portrait_key, dialogues):
        self.id = npc_id
        self.name = name
        self.title = title
        self.x = float(x)
        self.y = float(y)
        self.rect = pygame.Rect(int(self.x), int(self.y), TILE_SIZE, TILE_SIZE)
        self.sprite_key = sprite_key
        self.portrait_key = portrait_key
        self.dialogues = dialogues  # Diccionario indexado por fase de misión: {0: [...], 1: [...], ...}

    def get_dialogue_for_quest_stage(self, quest_stage, has_relic=False):
        """Devuelve la lista de frases adecuada según el avance de la misión."""
        if self.id == "valeria" and has_relic:
            return self.dialogues.get("victory", ["¡Has traído la reliquia sagrada! ¡El reino está a salvo!"])

        # Retornar diálogo para la etapa actual o la más cercana
        if quest_stage in self.dialogues:
            return self.dialogues[quest_stage]
        elif "default" in self.dialogues:
            return self.dialogues["default"]
        return [f"{self.name}: 'Saludos, viajero.'"]

    def is_player_nearby(self, player_rect, distance=24):
        """Comprueba si el jugador está lo suficientemente cerca para interactuar."""
        center_self = self.rect.center
        center_player = player_rect.center
        dist = ((center_self[0] - center_player[0]) ** 2 + (center_self[1] - center_player[1]) ** 2) ** 0.5
        return dist <= distance

    def draw(self, surface, camera, asset_loader):
        """Dibuja el sprite del NPC."""
        screen_pos = camera.apply_pos(self.rect.x, self.rect.y)
        sprite = asset_loader.sprites.get(self.sprite_key)
        if sprite:
            surface.blit(sprite, screen_pos)

    def draw_prompt(self, surface, camera, font):
        """Dibuja la viñeta flotante [E] Hablar sobre la cabeza del NPC."""
        screen_pos = camera.apply_pos(self.rect.x, self.rect.y)
        prompt_text = "[E] Hablar"
        text_surf = font.render(prompt_text, True, COLOR_TEXT_GOLD)

        # Fondo pequeño para legibilidad
        bg_rect = pygame.Rect(
            screen_pos[0] - 6,
            screen_pos[1] - 14,
            text_surf.get_width() + 4,
            text_surf.get_height() + 2
        )
        pygame.draw.rect(surface, (20, 24, 30, 200), bg_rect, border_radius=3)
        pygame.draw.rect(surface, COLOR_TEXT_GOLD, bg_rect, 1, border_radius=3)
        surface.blit(text_surf, (bg_rect.x + 2, bg_rect.y + 1))


def create_all_npcs():
    """Instancia los 3 NPCs requeridos con sus diálogos ramificados."""
    # 1. Guardiana Valeria (Pueblo, cerca de la salida este en x=19, y=10)
    valeria_dialogues = {
        0: [
            "Valeria: '¡Alto ahí, joven Eric! La niebla oscura avanza desde el bosque hacia nuestro pueblo.'",
            "Valeria: 'La Llama Antigua de Kal-Drakor se ha extinguido y monstruos sombríos amenazan las puertas.'",
            "Valeria: 'Antes de aventurarte, busca a la sabia Elira en el claro del Bosque Susurrante. Ella conoce los ritos del fuego.'"
        ],
        1: [
            "Valeria: '¿Ya hablaste con Elira? Ve a las Ruinas de Kal-Drakor y recupera la reliquia sagrada.'",
            "Valeria: 'Ten mucho cuidado con el Guardián de las Sombras; no permitas que te acorrale.'"
        ],
        2: [
            "Valeria: 'Has vencido a la sombra, pero aún debes recoger la reliquia del pedestal en las ruinas.'",
            "Valeria: '¡Apresúrate antes de que las sombras se regeneren!'"
        ],
        3: [
            "Valeria: '¡Por todos los cielos! ¡Esa es la legendaria Llama Antigua!'",
            "Valeria: 'Tu valentía ha salvado a Brumavalle de una noche eterna. ¡Eres el héroe de nuestro reino!'"
        ],
        "victory": [
            "Valeria: '¡Esa es la Llama Antigua! ¡Brumavalle está a salvo gracias a ti, Eric!'",
            "Valeria: 'Las leyendas cantarán tu nombre por generaciones.'"
        ],
        "default": [
            "Valeria: 'Mantén la guardia alta en todo momento. La paz de Brumavalle depende de nosotros.'"
        ]
    }

    valeria = NPC(
        npc_id="valeria",
        name="Guardiana Valeria",
        title="Capitana de la Guardia de Brumavalle",
        x=19 * TILE_SIZE,
        y=10 * TILE_SIZE,
        sprite_key="npc_valeria",
        portrait_key="valeria",
        dialogues=valeria_dialogues
    )

    # 2. Herrero Torin (Pueblo, al sur cerca de su forja en x=8, y=18)
    torin_dialogues = {
        0: [
            "Torin: '¡Saludos, Eric! He afilado esa espada de acero que llevas al cinto.'",
            "Torin: 'Recuerda: pulsa ESPACIO para atacar. Un buen golpe mantiene a raya a las bestias.'",
            "Torin: 'Si te hieren, usa una poción desde tu inventario pulsando [I]. ¡No te confíes allá afuera!'"
        ],
        1: [
            "Torin: 'Las bestias del bosque son rápidas, pero tu espada es firme. ¡Confía en tu entrenamiento!'"
        ],
        2: [
            "Torin: 'Escuché el estruendo desde las ruinas... ¡Esa criatura sombría ha caído!'",
            "Torin: 'Recoge la reliquia del altar y regresa con Valeria.'"
        ],
        3: [
            "Torin: '¡Increíble forja de la llama! Es un honor haber hecho la espada del salvador de Brumavalle.'"
        ],
        "default": [
            "Torin: 'El buen acero y un corazón valiente son todo lo que necesita un guerrero de honor.'"
        ]
    }

    torin = NPC(
        npc_id="torin",
        name="Herrero Torin",
        title="Maestro Forjador de Brumavalle",
        x=8 * TILE_SIZE,
        y=18 * TILE_SIZE,
        sprite_key="npc_torin",
        portrait_key="torin",
        dialogues=torin_dialogues
    )

    # 3. Anciana Elira (Bosque Susurrante, santuario en x=36, y=10)
    elira_dialogues = {
        0: [
            "Elira: 'Te estaba esperando, Eric... Los susurros del viento me anunciaron tu llegada.'",
            "Elira: 'La Llama Antigua que protegía nuestro reino fue robada y encerrada en las Ruinas de Kal-Drakor.'",
            "Elira: 'Un Guardián Sombrío la vigila día y noche. Debes derrotarlo y devolver la reliquia a la guardia.'",
            "Elira: 'Toma la bendición del bosque. Ve hacia el este, cruza los muros de piedra y purifica las sombras.'"
        ],
        1: [
            "Elira: 'El camino hacia Kal-Drakor está al este. Empuña tu espada contra las sombras y libera la Llama.'"
        ],
        2: [
            "Elira: 'Siento cómo el manto oscuro se desvanece... ¡Toma la reliquia del altar y llévasela a Valeria en el pueblo!'"
        ],
        3: [
            "Elira: 'La llama arde nuevamente. Que la luz guíe siempre tus pasos, noble Eric.'"
        ],
        "default": [
            "Elira: 'La luz siempre encuentra un camino a través de la noche más oscura.'"
        ]
    }

    elira = NPC(
        npc_id="elira",
        name="Sabia Elira",
        title="Custodia del Bosque Susurrante",
        x=36 * TILE_SIZE,
        y=10 * TILE_SIZE,
        sprite_key="npc_elira",
        portrait_key="elira",
        dialogues=elira_dialogues
    )

    return [valeria, torin, elira]
