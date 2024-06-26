from turtle import width
from pygame.locals import *

import pygame, sys
import os


# Initialize pygame and font
pygame.init()
pygame.font.init()

# Define colors
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BG_COLOR = (140, 171, 168)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Define game constants
BORDER_WIDTH = 10
FPS = 60
SPACESHIP_WIDTH = 50
SPACESHIP_HEIGHT = 40
PLAYER_VELOCITY = 5
BULLET_VELOCITY = 7
MAX_BULLETS = 3

# Custom events for handling player hits
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Load assets
YELLOW_PLAYER_IMAGE_PATH = os.path.join("pics", "spaceship_yellow.png")
RED_PLAYER_IMAGE_PATH = os.path.join("pics", "spaceship_red.png")
YELLOW_PLAYER = pygame.transform.rotate(
    pygame.transform.scale(
        pygame.image.load(YELLOW_PLAYER_IMAGE_PATH), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    ),
    270,
)
RED_PLAYER = pygame.transform.rotate(
    pygame.transform.scale(
        pygame.image.load(RED_PLAYER_IMAGE_PATH), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    ),
    90,
)
HEALTH_FONT = pygame.font.SysFont("comicsans", 40)

# Define player objects
red_player = pygame.Rect(
    WIDTH - SPACESHIP_WIDTH - 10,
    HEIGHT // 2 - SPACESHIP_HEIGHT // 2,
    SPACESHIP_WIDTH,
    SPACESHIP_HEIGHT,
)
yellow_player = pygame.Rect(
    10, HEIGHT // 2 - SPACESHIP_HEIGHT // 2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT
)

# define border object:
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

# Define lists for bullets
red_bullets = []
yellow_bullets = []

# Define player lives
red_lives = 10
yellow_lives = 10


def draw_game_window(red, yellow, red_bullets, yellow_bullets, red_lives, yellow_lives):
    WIN.fill(BG_COLOR)
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_lives_text = HEALTH_FONT.render("Lives: " + str(red_lives), 1, WHITE)
    yellow_lives_text = HEALTH_FONT.render("Lives: " + str(yellow_lives), 1, WHITE)
    WIN.blit(red_lives_text, (WIDTH - red_lives_text.get_width() - 10, 10))
    WIN.blit(yellow_lives_text, (10, 10))

    WIN.blit(YELLOW_PLAYER, (yellow.x, yellow.y))
    WIN.blit(RED_PLAYER, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def handle_yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - PLAYER_VELOCITY > 0:  # left
        yellow.x -= PLAYER_VELOCITY
    elif keys_pressed[pygame.K_w] and yellow.y - PLAYER_VELOCITY > 0:  # up
        yellow.y -= PLAYER_VELOCITY
    elif (
        keys_pressed[pygame.K_d]
        and yellow.x + PLAYER_VELOCITY + yellow.width - 10 < BORDER.x
    ):  # right
        yellow.x += PLAYER_VELOCITY
    elif (
        keys_pressed[pygame.K_s]
        and yellow.y + PLAYER_VELOCITY + yellow.height + 10 < HEIGHT
    ):  # down
        yellow.y += PLAYER_VELOCITY


def handle_red_movement(keys_pressed, red):
    if (
        keys_pressed[pygame.K_LEFT] and red.x - PLAYER_VELOCITY - 10 > BORDER_WIDTH
    ):  # left
        red.x -= PLAYER_VELOCITY
    elif keys_pressed[pygame.K_UP] and red.y - PLAYER_VELOCITY > 0:  # up
        red.y -= PLAYER_VELOCITY
    elif (
        keys_pressed[pygame.K_RIGHT]
        and red.x + PLAYER_VELOCITY + red.width - 12 < WIDTH
    ):  # right
        red.x += PLAYER_VELOCITY
    elif (
        keys_pressed[pygame.K_DOWN]
        and red.y + PLAYER_VELOCITY + red.height + 10 < HEIGHT
    ):  # down
        red.y += PLAYER_VELOCITY


def handle_bullets_controll(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = HEALTH_FONT.render(text, 1, WHITE)
    WIN.blit(
        draw_text,
        (
            WIDTH // 2 - draw_text.get_width() // 2,
            HEIGHT // 2 - draw_text.get_height() // 2,
        ),
    )
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    global red_lives, yellow_lives
    red = pygame.Rect(
        700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT
    )  # represent red player on the screen
    yellow = pygame.Rect(
        100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT
    )  # represent yellow player on the screen

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
                # pygame.display.update()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)

                if event.key == pygame.K_z and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width,
                        yellow.y + yellow.height // 2 - 2,
                        10,
                        5,
                    )
                    yellow_bullets.append(bullet)

            if event.type == RED_HIT:
                red_lives -= 1

            if event.type == YELLOW_HIT:
                yellow_lives -= 1

        winner_text = ""
        if red_lives <= 0:
            winner_text = "yellow wins!"
        if yellow_lives <= 0:
            winner_text = "red wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        handle_yellow_movement(keys_pressed, yellow)
        handle_red_movement(keys_pressed, red)

        handle_bullets_controll(yellow_bullets, red_bullets, yellow, red)

        draw_game_window(
            red, yellow, red_bullets, yellow_bullets, red_lives, yellow_lives
        )

    main()


if __name__ == "__main__":
    main()
