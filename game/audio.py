"""
game/audio.py
Manejador de audio y generador procedural de efectos de sonido (retro chiptune).
Garantiza que el juego funcione sin errores incluso si el dispositivo de audio no está disponible.
"""
import math
import struct
import pygame


class AudioManager:
    """Administrador central de efectos de sonido y música procedural."""

    def __init__(self):
        self.enabled = True
        self.volume = 0.7
        self.initialized = False
        self.sounds = {}
        self._init_mixer()
        if self.initialized:
            self._generate_procedural_sounds()

    def _init_mixer(self):
        """Inicializa el subsistema de audio con manejo seguro de excepciones."""
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
            self.initialized = True
        except Exception as e:
            print(f"[Audio] Dispositivo de audio no disponible ({e}). El juego continuará en modo silencioso.")
            self.initialized = False

    def _create_raw_sound(self, samples, sample_rate=22050):
        """Convierte una lista de muestras flotantes (-1.0 a 1.0) en un Sound de Pygame."""
        if not self.initialized:
            return None
        try:
            raw_bytes = bytearray()
            for s in samples:
                val = max(-1.0, min(1.0, s))
                int_val = int(val * 32767)
                raw_bytes.extend(struct.pack("<h", int_val))
            return pygame.mixer.Sound(buffer=bytes(raw_bytes))
        except Exception as e:
            print(f"[Audio] Error al sintetizar sonido: {e}")
            return None

    def _generate_procedural_sounds(self):
        """Genera efectos de sonido retro mediante síntesis de ondas directa."""
        sample_rate = 22050

        # 1. Sonido de seleccionar menú / interfaz (bip corto agradable)
        def make_select():
            duration = 0.08
            n_samples = int(sample_rate * duration)
            samples = []
            for i in range(n_samples):
                t = i / sample_rate
                freq = 520.0 + 300.0 * (t / duration)
                env = 1.0 - (t / duration)
                samples.append(math.sin(2 * math.pi * freq * t) * env * 0.4)
            return self._create_raw_sound(samples, sample_rate)

        # 2. Sonido de diálogo (tecleo retro)
        def make_talk():
            duration = 0.04
            n_samples = int(sample_rate * duration)
            samples = []
            for i in range(n_samples):
                t = i / sample_rate
                freq = 380.0
                env = 1.0 - (t / duration)
                # Onda cuadrada suave
                val = 0.25 if math.sin(2 * math.pi * freq * t) > 0 else -0.25
                samples.append(val * env)
            return self._create_raw_sound(samples, sample_rate)

        # 3. Sonido de ataque con espada (golpe de viento)
        def make_attack():
            duration = 0.14
            n_samples = int(sample_rate * duration)
            samples = []
            import random
            for i in range(n_samples):
                t = i / sample_rate
                freq = 400.0 * (1.0 - (t / duration) ** 1.5) + 80.0
                env = (1.0 - (t / duration)) ** 1.2
                noise = (random.random() * 2.0 - 1.0) * 0.35
                sine = math.sin(2 * math.pi * freq * t) * 0.4
                samples.append((sine + noise) * env)
            return self._create_raw_sound(samples, sample_rate)

        # 4. Sonido de impacto / golpe a enemigo o jugador
        def make_hit():
            duration = 0.16
            n_samples = int(sample_rate * duration)
            samples = []
            import random
            for i in range(n_samples):
                t = i / sample_rate
                freq = 150.0 * (1.0 - (t / duration)) + 50.0
                env = (1.0 - (t / duration)) ** 2
                noise = (random.random() * 2.0 - 1.0) * 0.5
                sine = math.sin(2 * math.pi * freq * t) * 0.5
                samples.append((sine + noise) * env * 0.7)
            return self._create_raw_sound(samples, sample_rate)

        # 5. Sonido de poción curativa (arpegio mágico ascendente)
        def make_potion():
            duration = 0.28
            n_samples = int(sample_rate * duration)
            samples = []
            notes = [523.25, 659.25, 783.99, 1046.50]  # C, E, G, C alta
            note_len = duration / len(notes)
            for i in range(n_samples):
                t = i / sample_rate
                note_idx = min(int(t / note_len), len(notes) - 1)
                freq = notes[note_idx]
                note_t = t - (note_idx * note_len)
                env = 1.0 - (note_t / note_len)
                samples.append(math.sin(2 * math.pi * freq * t) * env * 0.35)
            return self._create_raw_sound(samples, sample_rate)

        # 6. Sonido de logro / misión completada (arpegio triunfal)
        def make_quest():
            duration = 0.55
            n_samples = int(sample_rate * duration)
            samples = []
            notes = [440.0, 554.37, 659.25, 880.0]  # A, C#, E, A alta
            note_len = duration / len(notes)
            for i in range(n_samples):
                t = i / sample_rate
                note_idx = min(int(t / note_len), len(notes) - 1)
                freq = notes[note_idx]
                note_t = t - (note_idx * note_len)
                env = 1.0 - (note_t / note_len) * 0.7
                samples.append(math.sin(2 * math.pi * freq * t) * env * 0.4)
            return self._create_raw_sound(samples, sample_rate)

        # 7. Sonido de derrota (Game Over)
        def make_defeat():
            duration = 0.6
            n_samples = int(sample_rate * duration)
            samples = []
            notes = [440.0, 392.0, 349.23, 261.63]  # A, G, F, C
            note_len = duration / len(notes)
            for i in range(n_samples):
                t = i / sample_rate
                note_idx = min(int(t / note_len), len(notes) - 1)
                freq = notes[note_idx]
                env = 1.0 - (t / duration)
                samples.append(math.sin(2 * math.pi * freq * t) * env * 0.4)
            return self._create_raw_sound(samples, sample_rate)

        self.sounds = {
            "select": make_select(),
            "talk": make_talk(),
            "attack": make_attack(),
            "hit": make_hit(),
            "potion": make_potion(),
            "quest": make_quest(),
            "defeat": make_defeat(),
        }

    def play(self, name):
        """Reproduce un sonido por su nombre con el volumen configurado."""
        if not self.enabled or not self.initialized:
            return
        snd = self.sounds.get(name)
        if snd:
            try:
                snd.set_volume(self.volume)
                snd.play()
            except Exception:
                pass

    def toggle(self):
        """Alterna el sonido activado/desactivado."""
        self.enabled = not self.enabled
        return self.enabled

    def set_volume(self, val):
        """Ajusta el volumen entre 0.0 y 1.0."""
        self.volume = max(0.0, min(1.0, val))


# Instancia global accesible en todo el juego
audio = AudioManager()
