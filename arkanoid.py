import pygame
import sys
import math
import time

pygame.init()

# Ventana
scala_x = 3
scala_y = 3
WIDTH = 480 * scala_x
HEIGHT = 320 * scala_y

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arkanoid Clone")

clock = pygame.time.Clock()

# Bola
x = (WIDTH / 2)
y = (HEIGHT - 30)
dx = 2
dy = -2
ball_radius = 10 * (scala_x + scala_y) / 2 / 1.3

# Pala
paddle_height = 10 * scala_x
paddle_width = 75 * scala_y
paddle_x = ((WIDTH - paddle_width) / 2)
paddle_speed = 7 * scala_x

# Bloques
brick_rows = 3
brick_cols = 5
brick_width = 75 * scala_x
brick_height = 20 * scala_y
brick_padding = 10 * (scala_x + scala_y) / 2
brick_offset_top = 30 * scala_y
brick_offset_left = 30 * scala_x

bricks = []

for c in range(brick_cols):
    column = []
    for r in range(brick_rows):
        brick_x = c * (brick_width + brick_padding) + brick_offset_left
        brick_y = r * (brick_height + brick_padding) + brick_offset_top

        column.append({
            "x": brick_x,
            "y": brick_y,
            "status": True,
            "score": 100
        })

    bricks.append(column)

# Fuente
font = pygame.font.Font(None, int(20 * (scala_x + scala_y) / 2))

# Puntuacion
score = 0

def collision_detection_overlap():
    global x, y, dx, dy, score

    for c in range(brick_cols):
        for r in range(brick_rows):
            brick = bricks[c][r]

            if brick["status"]:
                ball_left = x - ball_radius
                ball_right = x + ball_radius
                ball_top = y - ball_radius
                ball_bottom = y + ball_radius

                brick_left = brick["x"]
                brick_right = brick["x"] + brick_width
                brick_top = brick["y"]
                brick_bottom = brick["y"] + brick_height

                if (ball_right >= brick_left and
                        ball_left <= brick_right and
                        ball_bottom >= brick_top and
                        ball_top <= brick_bottom):

                    overlap_left = ball_right - brick_left
                    overlap_right = brick_right - ball_left
                    overlap_top = ball_bottom - brick_top
                    overlap_bottom = brick_bottom - ball_top

                    min_overlap = min(
                        overlap_left,
                        overlap_right,
                        overlap_top,
                        overlap_bottom
                    )

                    if min_overlap == overlap_left:
                        dx = -abs(dx)
                        x -= overlap_left

                    elif min_overlap == overlap_right:
                        dx = abs(dx)
                        x += overlap_right

                    elif min_overlap == overlap_top:
                        dy = -abs(dy)
                        y -= overlap_top

                    else:
                        dy = abs(dy)
                        y += overlap_bottom

                    brick["status"] = False
                    score += brick["score"]


def collision_detection_before_position(old_x_pos, old_y_pos):
    global dx, dy, score

    for c in range(brick_cols):
        for r in range(brick_rows):

            brick = bricks[c][r]

            if not brick["status"]:
                continue

            ball_left = x - ball_radius
            ball_right = x + ball_radius
            ball_top = y - ball_radius
            ball_bottom = y + ball_radius

            brick_left = brick["x"]
            brick_right = brick["x"] + brick_width
            brick_top = brick["y"]
            brick_bottom = brick["y"] + brick_height

            if (ball_right >= brick_left and
                    ball_left <= brick_right and
                    ball_bottom >= brick_top and
                    ball_top <= brick_bottom):

                old_ball_left = old_x_pos - ball_radius
                old_ball_right = old_x_pos + ball_radius
                old_ball_top = old_y_pos - ball_radius
                old_ball_bottom = old_y_pos + ball_radius

                if old_ball_bottom <= brick_top:
                    dy = -abs(dy)

                elif old_ball_top >= brick_bottom:
                    dy = abs(dy)

                elif old_ball_right <= brick_left:
                    dx = -abs(dx)

                elif old_ball_left >= brick_right:
                    dx = abs(dx)

                brick["status"] = False
                score += brick["score"]
                return


running = True
win = False


def collision_detection_paddle():
    global x, y, dx, dy

    ball_left = x - ball_radius
    ball_right = x + ball_radius
    ball_top = y - ball_radius
    ball_bottom = y + ball_radius

    paddle_top = HEIGHT - paddle_height
    paddle_bottom = HEIGHT
    paddle_left = paddle_x
    paddle_right = paddle_x + paddle_width

    if (ball_right >= paddle_left and
            ball_left <= paddle_right and
            ball_bottom >= paddle_top and
            ball_top <= paddle_bottom):
        # corregir posición para evitar “pegado”
        y = paddle_top - ball_radius

        # rebote con ángulo según impacto
        hit_pos = (x - paddle_x) / paddle_width
        hit_pos = max(0.0, min(1.0, hit_pos))

        angle = (hit_pos - 0.5) * math.radians(120)
        speed = math.sqrt(dx * dx + dy * dy)

        dx = speed * math.sin(angle)
        dy = -abs(speed * math.cos(angle))

        return True

    return False


def paint_score():
    text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(text, (10*scala_x, 10*scala_y))

def paint_game_over():
    text = font.render("G A M E    O V E R", True, (255, 255, 255))
    screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))

def paint_game_win():
    text = font.render("Y O U    W I N", True, (255, 255, 255))
    screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))

while running or not win:

    clock.tick(100)  # Aproximadamente equivalente a setInterval(draw, 10)

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Teclado
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        paddle_x += paddle_speed

    if keys[pygame.K_LEFT]:
        paddle_x -= paddle_speed

    paddle_x = max(0, min(WIDTH - paddle_width, paddle_x))

    # Colisiones con paredes
    if x + dx > WIDTH - ball_radius or x + dx < ball_radius:
        dx = -dx

    if y + dy < ball_radius:
        dy = -dy

    elif y + dy > HEIGHT - ball_radius:

        # Colisión con la pala
        if not collision_detection_paddle():
            # print("GAME OVER")
            running = False

    # collision_detection_overlap()

    old_x = x
    old_y = y

    # Movimiento
    x += dx * scala_x
    y += dy * scala_y

    collision_detection_before_position(old_x, old_y)

    # Dibujado
    screen.fill((34, 34, 34))

    # Bloques
    win = True
    for c in range(brick_cols):
        for r in range(brick_rows):

            brick = bricks[c][r]

            if brick["status"]:
                pygame.draw.rect(
                    screen,
                    (76, 175, 80),
                    (
                        brick["x"],
                        brick["y"],
                        brick_width,
                        brick_height
                    )
                )
                win = False

    # Bola
    pygame.draw.circle(
        screen,
        (255, 87, 51),
        (int(x), int(y)),
        ball_radius
    )

    # Pala
    pygame.draw.rect(
        screen,
        (0, 149, 221),
        (
            paddle_x,
            HEIGHT - paddle_height,
            paddle_width,
            paddle_height
        )
    )

    paint_score()

    if not running:
        paint_game_over()

    if win:
        paint_game_win()
        running = False

    pygame.display.flip()

time.sleep(3)

pygame.quit()
sys.exit()
