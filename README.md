# Arkanoid Clone (Pygame)

Implementación sencilla de un clon de Arkanoid/Breakout desarrollada en Python utilizando Pygame.

El proyecto incluye:

- Movimiento de pala controlado por teclado.
- Bola con rebote en paredes.
- Sistema de bloques destruibles.
- Puntuación.
- Pantalla de victoria.
- Pantalla de Game Over.
- Detección de colisiones basada en la posición anterior de la bola.
- Rebote de la bola sobre la pala con ángulo variable según el punto de impacto.

---

## Requisitos

- Python 3.10 o superior
- Pygame

Instalación:

```bash
pip install pygame
```

---

## Ejecución

```bash
python arkanoid.py
```

---

## Controles

| Tecla | Acción |
|---------|---------|
| ← | Mover la pala a la izquierda |
| → | Mover la pala a la derecha |
| Cerrar ventana | Salir del juego |

---

## Características

### Escalado de resolución

El juego utiliza dos factores de escala:

```python
scala_x = 3
scala_y = 3
```

Esto permite aumentar el tamaño de todos los elementos del juego manteniendo las proporciones originales.

Resolución resultante:

```text
1440 x 960
```

---

### Sistema de bloques

La disposición de bloques se define mediante:

```python
brick_rows = 3
brick_cols = 5
```

Cada bloque tiene:

```python
{
    "x": posición horizontal,
    "y": posición vertical,
    "status": True,
    "score": 100
}
```

Cuando un bloque es destruido:

- desaparece de pantalla
- suma 100 puntos

---

### Sistema de puntuación

La puntuación se almacena en:

```python
score
```

y se muestra en tiempo real durante la partida.

---

### Detección de colisiones

El proyecto incluye dos enfoques distintos.

#### 1. Detección por penetración mínima

Función:

```python
collision_detection_overlap()
```

Calcula cuánto se solapan la bola y el bloque en cada dirección:

- izquierda
- derecha
- arriba
- abajo

y rebota según la menor penetración.

Actualmente está desactivada.

---

#### 2. Detección mediante posición anterior

Función:

```python
collision_detection_before_position()
```

Es el método utilizado por defecto.

Proceso:

1. Se guarda la posición anterior de la bola.
2. La bola se mueve.
3. Se comprueba si existe solapamiento con un bloque.
4. Se determina desde qué lado llegó la bola comparando la posición anterior con los límites del bloque.

Ventajas:

- comportamiento más estable
- menos rebotes erróneos en esquinas
- implementación sencilla
- adecuada para velocidades moderadas

---

### Rebote sobre la pala

La función:

```python
collision_detection_paddle()
```

implementa un rebote dependiente del punto de impacto.

Si la bola golpea:

- el centro → rebote casi vertical
- la izquierda → rebote hacia la izquierda
- la derecha → rebote hacia la derecha

El ángulo se calcula mediante:

```python
angle = (hit_pos - 0.5) * math.radians(120)
```

donde:

```python
hit_pos
```

representa la posición relativa del impacto dentro de la pala.

Esto produce un comportamiento similar al de los juegos Arkanoid y Breakout clásicos.

---

## Condiciones de victoria y derrota

### Victoria

El jugador gana cuando todos los bloques han sido destruidos.

Se muestra:

```text
YOU WIN
```

### Derrota

El jugador pierde cuando la bola atraviesa la zona inferior sin tocar la pala.

Se muestra:

```text
GAME OVER
```

---

## Estructura principal

```text
arkanoid.py
│
├── Inicialización de Pygame
├── Configuración de pantalla
├── Creación de bloques
├── Detección de colisiones
├── Movimiento de la bola
├── Movimiento de la pala
├── Sistema de puntuación
├── Renderizado
└── Bucle principal del juego
```

---

## Posibles mejoras

- Sistema de vidas.
- Múltiples niveles.
- Bloques con resistencia variable.
- Efectos de sonido.
- Música de fondo.
- Aumento progresivo de velocidad.
- Power-ups.
- Persistencia de puntuaciones máximas.
- Menú principal.
- Pausa.
- Soporte para mando.

---

## Tecnologías utilizadas

- Python
- Pygame

---

## Licencia

Proyecto educativo desarrollado para aprender:

- bucles de juego
- renderizado 2D
- detección de colisiones
- gestión de eventos
- física básica para videojuegos arcade