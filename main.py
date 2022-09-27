import pygame
import os

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("for nahal<3")
bg_color = (140, 171, 168)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

FPS = 60  # speed:frames per second
SPACESHIP_WITDH, SPACESHIP_HEIGHT = 50, 40
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


YELLOW_PLAYER_image = pygame.image.load(os.path.join("pics", "spaceship_yellow.png"))
YELLOW_PLAYER = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_PLAYER_image, (SPACESHIP_WITDH, SPACESHIP_HEIGHT)),
    270,
)

RED_PLAYER_image = pygame.image.load(os.path.join("pics", "spaceship_red.png"))
RED_PLAYER = pygame.transform.rotate(
    pygame.transform.scale(RED_PLAYER_image, (SPACESHIP_WITDH, SPACESHIP_HEIGHT)), 90
)

red_bullets = []
yellow_bullets = []


def draw(red, yellow, red_bullets, yellow_bullets):
    WIN.fill(bg_color)
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(YELLOW_PLAYER, (yellow.x, yellow.y))
    WIN.blit(RED_PLAYER, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # left
        yellow.x -= VEL
    elif keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # up
        yellow.y -= VEL
    elif (
        keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width - 10 < BORDER.x
    ):  # right
        yellow.x += VEL
    elif (
        keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height + 10 < HEIGHT
    ):  # down
        yellow.y += VEL


def red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL - 10 > BORDER.x:  # left
        red.x -= VEL
    elif keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # up
        red.y -= VEL
    elif keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width - 12 < WIDTH:  # right
        red.x += VEL
    elif keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height + 10 < HEIGHT:  # down
        red.y += VEL


def bullets_strikes(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)


def main():
    red = pygame.Rect(
        700, 300, SPACESHIP_WITDH, SPACESHIP_HEIGHT
    )  # represent red player on the screen
    yellow = pygame.Rect(
        100, 300, SPACESHIP_WITDH, SPACESHIP_HEIGHT
    )  # represent yellow player on the screen

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

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

        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed, yellow)
        red_movement(keys_pressed, red)

        bullets_strikes(yellow_bullets, red_bullets, yellow, red)

        draw(red, yellow, red_bullets, yellow_bullets)

    pygame.quit()


if __name__ == "__main__":
    main()
