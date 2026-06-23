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

# Vidas
lives = 3


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
                    sound_brick.play()
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
                sound_brick.play()
                score += brick["score"]
                return


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

        sound_paddle.play()

        return True

    return False


def paint_score():
    text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(text, (10 * scala_x, 10 * scala_y))


def paint_lives():
    text = font.render("Lives: " + str(lives), True, (255, 255, 255))
    screen.blit(text, (200 * scala_x, 10 * scala_y))


def paint_game_over():
    text = font.render("G A M E    O V E R", True, (255, 255, 255))
    screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))


def paint_game_win():
    text = font.render("Y O U    W I N", True, (255, 255, 255))
    screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))


running = True
win = None
player_dies = None

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
sound_wall = pygame.mixer.Sound("sounds/wall.wav")
sound_paddle = pygame.mixer.Sound("sounds/paddle.wav")
sound_brick = pygame.mixer.Sound("sounds/brick.wav")
sound_bg = pygame.mixer.Sound("sounds/bg.wav")
sound_wall.set_volume(0.5)
sound_paddle.set_volume(0.5)
sound_brick.set_volume(0.5)
sound_bg.set_volume(0.3)

sound_bg.play(-1)  # fade_ms=1000)

start_time = time.time()
start_ticks = pygame.time.get_ticks()
final_time = None


def get_time_text(elapsed):
    if final_time is not None:
        elapsed = final_time
    else:
        elapsed = pygame.time.get_ticks() - start_ticks

    seconds = elapsed // 1000
    minutes = seconds // 60
    seconds = seconds % 60

    return f"{minutes:02d}:{seconds:02d}"


def paint_time(elapsed):
    minutes = elapsed // 60
    seconds = elapsed % 60
    time_text = f"{minutes:02d}:{seconds:02d}"
    text_surface = font.render(get_time_text(elapsed), True, (255, 255, 255))
    if running:
        screen.blit(
            text_surface,
            (WIDTH - text_surface.get_width() - 10, 10)
        )


while running and win is None:

    clock.tick(100)  # Aproximadamente equivalente a setInterval(draw, 10)

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sound_bg.stop()
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
        sound_wall.play()

    if y + dy < ball_radius:
        dy = -dy
        sound_wall.play()

    elif y + dy > HEIGHT - ball_radius:

        # Colisión con la pala
        if not collision_detection_paddle():
            player_dies = True
            lives = lives - 1
            if lives == 0:
                win = False
            final_time = pygame.time.get_ticks() - start_ticks

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
    bricks_remaining = 0
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
                bricks_remaining += 1
    if bricks_remaining == 0:
        win = True

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

    paint_time(int(time.time() - start_time))
    paint_lives()
    paint_score()

    if player_dies:
        pygame.mixer.music.load("sounds/player_dies.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
        if lives > 0:
            player_dies = False
            x = (WIDTH / 2)
            y = (HEIGHT - 30)
            dx = 2
            dy = -2
            paddle_x = ((WIDTH - paddle_width) / 2)

    if win is True:
        paint_game_win()
        sound_bg.stop()
        final_time = pygame.time.get_ticks() - start_ticks
        pygame.mixer.music.load("sounds/win.mp3")
        pygame.mixer.music.play()
    elif win is False:
        paint_game_over()
        sound_bg.stop()
        pygame.mixer.music.load("sounds/lose.mp3")
        pygame.mixer.music.play()

    pygame.display.flip()

while pygame.mixer.music.get_busy():
    pygame.time.wait(100)

time.sleep(1.5)

pygame.quit()
sys.exit()
