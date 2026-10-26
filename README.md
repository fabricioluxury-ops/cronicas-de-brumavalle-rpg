# ⚔️ Crónicas de Brumavalle: La Llama Antigua 🛡️

**Un videojuego RPG medieval clásico en 2D con estética Pixel Art de 16-bit**  
*Desarrollado en Python 3 y Pygame*

---

## 📜 Historia y Ambientación

Durante generaciones, la sagrada **Llama Antigua de Kal-Drakor** ardió en lo alto del pedestal del templo, irradiando una bendición protectora sobre los valles de **Brumavalle**. Gracias a su luz celestial, la aldea prosperó entre frondosos robles, arroyos cristalinos y fértiles tierras de labranza.

Sin embargo, una noche de luna menguante, las sombras ancestrales despertaron en las profundidades de las ruinas. Una criatura tenebrosa conocida como el **Guardián de las Sombras** descendió sobre el santuario, robando la reliquia y extinguiendo el fuego sagrado. Una densa bruma fría cubrió de inmediato los senderos del **Bosque Susurrante**, y temibles slimes sombríos comenzaron a asediar las empalizadas de Brumavalle.

La capitana **Guardiana Valeria** ha convocado a los defensores, pero la tradición dice que solo un corazón valiente guiado por la sabiduría de la anciana **Sabia Elira** y armado con el acero forjado por el maestro **Herrero Torin** podrá abrirse paso a través de las ruinas, purificar las tinieblas y devolver la Llama Antigua a su pedestal.

**Tu leyenda como el héroe Eric comienza en las puertas de Brumavalle.**

---

## ✨ Características Implementadas

1. **Pantalla de Carga Animada:**
   - Barra de progreso fluida con mensajes inmersivos (*"Preparando el reino...", "Cargando personajes...", "Encendiendo las antorchas...", "Despertando a los guardianes antiguos..."*).
2. **Menú Principal Completo:**
   - Opciones interactivas con teclado: *Nueva Partida*, *Continuar* (con validación de guardado previo), *Opciones*, *Créditos* y *Salir*.
3. **Prólogo Narrativo (Intro):**
   - Introducción a la historia y contexto del reino antes de comenzar la partida.
4. **Mundo Abierto Explorable Top-Down:**
   - Mapa de 60x40 casillas (960x640 píxeles) dividido en 3 zonas conectadas:
     - **Pueblo de Brumavalle:** Cabañas con tejados y ventanas, caminos de adoquines, vallas, antorchas, flores y la herrería.
     - **Bosque Susurrante:** Senderos de tierra, arboledas densas, un río navegable con puente de madera, cofre secreto y el santuario místico.
     - **Ruinas de Kal-Drakor:** Salón de piedra oscura con columnas milenarias, antorchas místicas y el altar sagrado de la reliquia.
5. **Cámara Suave y Dinámica (Smooth Follow):**
   - Sigue al héroe suavemente mediante interpolación y se bloquea con precisión en los límites exteriores del mapa.
6. **Sistema Físico y de Colisiones por Eje:**
   - Detección precisa de obstáculos (árboles, muros, edificios, vallas, agua y columnas) que impide que el jugador o los enemigos atraviesen objetos sólidos.
7. **Personaje Principal Original:**
   - Héroe ("Eric") con túnica de aventurero y armadura de acero, animación de 4 direcciones (abajo, arriba, izquierda, derecha) con 3 fotogramas de caminata y fotograma de reposo.
8. **3 Personajes NPCs Originales con Diálogos Ramificados:**
   - **Guardiana Valeria:** Capitana defensora del pueblo con armadura de plata y capa escarlata.
   - **Herrero Torin:** Forjador maestro con delantal de cuero, barba tupida y consejos de combate.
   - **Sabia Elira:** Anciana custodia del bosque con túnica púrpura, báculo místico y amuleto rúnico.
9. **Sistema de Interacción con Indicadores Visuales:**
   - Al acercarse a un NPC u objeto interactuable, aparece la viñeta flotante `[E] Hablar` o `[E] Abrir`.
   - Cuadro de diálogo clásico con marco dorado, retrato detallado de 32x32 píxeles, nombre del personaje y avance mediante `E` o `ENTER`.
10. **Misión Principal Estructurada y Registro (Diario de Misiones):**
    - Paso 1: Consultar a la Sabia Elira en el claro del bosque.
    - Paso 2: Cruzar al este y derrotar al Guardián de las Sombras en las ruinas.
    - Paso 3: Reclamar la Reliquia de la Llama Antigua en el altar.
    - Paso 4: Regresar a Brumavalle y entregar la reliquia a la Guardiana Valeria para salvar el reino.
    - Tecla `J` para abrir/cerrar el diario con casillas de verificación de estado.
11. **Combate en Tiempo Real con Espada:**
    - Ataque con `ESPACIO`: anima un tajo curvo de acero brillante frente al jugador con efecto de sonido de corte.
    - Área de daño (hitbox) que calcula impacto y retroceso físico (knockback) sobre los enemigos.
    - Slimes Sombríos errantes y patrullando el bosque.
    - Miniboss: **Guardián de las Sombras** custodiando el altar de las ruinas con alta vida y ataque potente.
    - Mini barras de vida flotantes sobre los enemigos heridos y efecto visual de parpadeo de daño.
12. **Sistema de Salud e Inventario:**
    - Barra de vida en el HUD con indicador numérico `PV: 100/100`.
    - Tecla `I` para abrir el inventario retro: visualización de espada equipada, pociones y objetos clave.
    - Uso de Pociones de Vida (teclas `U` o `ENTER`) que restauran +40 PV con sonido de arpegio mágico y límite máximo de salud.
13. **Sistema de Guardado y Carga Local (JSON):**
    - Almacenado en `data/savegame.json`.
    - Guarda posición exacta del jugador, salud, inventario, progreso de misión, cofre abierto y enemigos derrotados.
    - Escritura atómica para evitar corrupción de archivos y manejo seguro con mensajes amigables si el archivo está ausente o corrupto.
14. **Menú de Pausa (ESC):**
    - Continuar, Guardar Partida (con confirmación en pantalla), Opciones, Volver al Menú y Salir.
15. **Pantallas de Victoria y Game Over:**
    - Game Over al caer en combate con opción de reintentar desde el último punto de guardado o regresar al menú.
    - Victoria conmemorativa al entregar la reliquia, con celebración y créditos.
16. **Efectos de Sonido Retro Procedurales (Chiptune):**
    - Síntesis de sonido propia sin librerías externas mediante ondas senoidales, armónicos y ruido (bip de menú, tecleo de texto, tajo de espada, impacto, arpegio de curación, fanfarria de misión y derrota).
    - Manejo seguro ante ausencia de hardware de audio (modo silencioso automático).
17. **Cierre Limpio:**
    - Cierre correcto de ventanas y procesos Pygame desde cualquier menú o pantalla.

---

## 🎮 Controles del Juego

| Tecla | Acción |
| :--- | :--- |
| **W, A, S, D** o **Flechas** | Mover al personaje en 4 direcciones |
| **ESPACIO** | Atacar con la espada de acero |
| **E** o **ENTER** | Hablar con NPCs, abrir cofres, interactuar y avanzar diálogos |
| **I** | Abrir / Cerrar el Inventario |
| **U** o **ENTER** (en inventario) | Beber Poción de Vida seleccionada |
| **J** | Abrir / Cerrar el Diario de Misiones |
| **ESC** | Pausar el juego / Volver atrás en menús |

---

## 📁 Estructura del Proyecto

```text
cronicas-de-brumavalle-rpg/
├── .gitignore               # Exclusión de temporales, cachés y partidas guardadas locales
├── LICENSE                  # Licencia de código abierto MIT (Eric Fabricio García García)
├── README.md                # Documentación exhaustiva del proyecto
├── main.py                  # Punto de entrada principal y bucle del motor Pygame
├── requirements.txt         # Dependencias del proyecto (pygame / pygame-ce)
├── run_game.bat             # Lanzador rápido de un clic para Windows
├── test_game.py             # Batería de pruebas automatizadas y comprobación headless
├── assets/
│   ├── images/              # Sprites pixel art 16x16 y 32x32 generados y exportados
│   │   ├── icon_*.png       # Iconos de espada, poción y reliquia
│   │   ├── portrait_*.png   # Retratos de Valeria, Torin, Elira y Eric
│   │   ├── sprite_*.png     # Sprites de caminata, NPCs y enemigos
│   │   └── tile_*.png       # Tiles de terreno, edificios, agua y ruinas
│   └── sounds/              # Directorio de recursos de audio
├── data/
│   └── savegame.json        # Partida guardada local (generada al guardar partida)
└── game/
    ├── __init__.py          # Inicializador del paquete
    ├── settings.py          # Constantes globales, dimensiones, paletas y controles
    ├── audio.py             # Motor y sintetizador procedural de efectos retro
    ├── asset_loader.py      # Generador y cargador de recursos pixel art originales
    ├── camera.py            # Cámara 2D con seguimiento suave y confinamiento al mapa
    ├── map_data.py          # Definición de tiles, colisiones, cofres y altar del mundo
    ├── save_manager.py      # Gestor de persistencia JSON y etapas de la misión
    ├── entities/
    │   ├── __init__.py
    │   ├── player.py        # Héroe jugable, física, combate, vida e inventario
    │   ├── npc.py           # NPCs (Valeria, Torin, Elira), diálogos e indicadores
    │   └── enemy.py         # Slimes y Guardián de las Sombras con IA de persecución
    ├── ui/
    │   ├── __init__.py
    │   ├── hud.py           # Tarjeta de vida, objetivo actual y barra de controles
    │   ├── dialogue_box.py  # Ventana clásica de diálogo con marco y retrato
    │   ├── inventory_view.py# Ventana modal de inventario y consumo de pociones
    │   └── quest_log_view.py# Diario de registro de pasos de la misión
    └── states/
        ├── __init__.py
        ├── base_state.py    # Clase abstracta base para pantallas
        ├── state_machine.py # Máquina de estados con transiciones y capas superpuestas
        ├── loading_state.py # Pantalla inicial de carga con barra animada
        ├── menu_state.py    # Menú principal con opciones funcionales
        ├── intro_state.py   # Pantalla de prólogo e historia
        ├── play_state.py    # Núcleo del juego activo y coordinación de sistemas
        ├── pause_state.py   # Menú modal de pausa y guardado rápido
        ├── options_state.py # Ajustes de volumen, sonido y mapa de controles
        ├── credits_state.py # Pantalla de créditos del autor y nota educativa
        ├── game_over_state.py # Pantalla de derrota con reintento
        └── victory_state.py # Pantalla triunfal de misión cumplida
```

---

## 🛠️ Requisitos e Instalación

### Requisitos del Sistema
- **Python 3.10 o superior** (probado en Python 3.10, 3.11, 3.12, 3.13 y 3.14).
- Sistema Operativo: Windows 10/11, macOS o Linux.
- Biblioteca **Pygame** o **Pygame-CE** (Community Edition).

### Instalación de Dependencias

1. Abre una terminal o consola de comandos en la carpeta del proyecto.
2. Instala la biblioteca requerida:

```bash
pip install -r requirements.txt
```

> **Nota para Python 3.14+:** En Python 3.14 se recomienda utilizar `pygame-ce` ya que incluye binarios precompilados compatibles con SDL2.

---

## 🚀 Cómo Ejecutar el Juego

### En Windows
Puedes hacer doble clic directamente en el archivo:
```text
run_game.bat
```
O desde la consola (PowerShell o CMD):
```bash
python main.py
```

### En macOS / Linux
Desde la terminal:
```bash
python3 main.py
```

---

## 🧭 Guía de Juego: Cómo Completar la Aventura

1. **Inicio en Brumavalle:**
   - Apareces en la plaza central de Brumavalle. A tu izquierda se encuentra la cabaña de guardia y al sur la herrería de **Torin**.
   - Habla con **Torin** para repasar los controles de combate.
2. **Hablar con Valeria:**
   - Camina hacia el este de la aldea y habla con la **Guardiana Valeria** usando la tecla `E`. Te informará sobre la oscuridad que acecha y te pedirá que encuentres a la sabia.
3. **El Bosque Susurrante y la Sabia Elira:**
   - Cruza hacia el este al Bosque Susurrante. Cruza el puente de madera sobre el río.
   - Encontrarás un claro místico con columnas rúnicas donde habita la **Sabia Elira**. Habla con ella con `E` para recibir la bendición y desbloquear el acceso a las ruinas.
   - *Consejo:* Al norte del puente hay un cofre de madera entre los árboles; acércate y pulsa `E` para obtener pociones curativas extra.
4. **Combate en las Ruinas de Kal-Drakor:**
   - Continúa hacia el este para adentrarte en las ruinas de piedra oscura.
   - Elimina los Slimes Sombríos atacando con `ESPACIO`.
   - En la antecámara del altar te enfrentarás al **Guardián de las Sombras**. Mantén la distancia, asesta tajos precisos y vigila tu barra de vida. Si tu salud baja, pulsa `I` y consume una poción con `ENTER` o `U`.
5. **Reclamar la Llama Antigua:**
   - Una vez derrotado el Guardián, acércate al pedestal del altar al fondo de las ruinas (x=55, y=11) y presiona `E` para tomar la **Reliquia de la Llama Antigua**.
6. **Regreso Triunfal a Brumavalle:**
   - Emprende el camino de regreso hacia el pueblo y habla nuevamente con la **Guardiana Valeria** para entregarle la reliquia.
   - ¡Se activará la pantalla de victoria conmemorando tu hazaña!

---

## 💾 Sistema de Guardado y Carga

- El juego permite guardar la partida en cualquier momento durante la exploración abriendo el menú de pausa con `ESC` y seleccionando **"Guardar Partida"**.
- El progreso se guarda en el archivo local:
  ```text
  data/savegame.json
  ```
- Al abrir el juego, el botón **"Continuar"** en el Menú Principal se activará automáticamente para retomar la aventura exactamente donde la dejaste.
- Si el archivo no existe o se encuentra dañado, el juego lo notifica cordialmente sin cerrarse de forma inesperada.

---

## 🧪 Pruebas Automatizadas (Test Suite)

El proyecto incluye una suite de pruebas automatizadas que verifican la integridad de los generadores gráficos, la lógica de daño, las etapas de misiones y la persistencia JSON sin necesidad de abrir una ventana gráfica:

Para ejecutar los tests:
```bash
python test_game.py
```

Resultado verificado:
```text
......
----------------------------------------------------------------------
Ran 6 tests in 0.722s

OK
```

---

## 🔧 Solución de Problemas Comunes

- **Error al importar `pygame`:**
  Ejecuta `pip install pygame-ce` o `pip install pygame` para reinstalar la biblioteca gráfica.
- **La ventana se abre pero no hay sonido:**
  El juego cuenta con un controlador de audio seguro que detecta si el equipo no posee tarjeta de sonido activa o controladores de audio y continúa funcionando en modo silencioso sin fallos.
- **Rendimiento bajo o tirones:**
  El juego está optimizado para ejecutarse a 60 FPS estables gracias a la técnica de renderizado en resolución virtual nativa (480x270) escalada por hardware.

---

## 👤 Créditos y Autoría

- **Desarrollador y Creador:** **Eric Fabricio García García**
- **Proyecto:** Proyecto Escolar y Educativo de Videojuegos 2D con Python y Pygame.
- **Nota de Originalidad:** Todos los personajes (Valeria, Torin, Elira, Eric, Guardián de las Sombras), el guion, el diseño del mapa, los diálogos y los recursos gráficos pixel art fueron concebidos originalmente para este proyecto o sintetizados mediante algoritmos en código fuente, garantizando el cumplimiento total de los derechos de autor y originalidad académica.

---
*¡Que la Llama Antigua ilumine siempre tu camino!*
