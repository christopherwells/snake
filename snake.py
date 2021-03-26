from os import system
from sys import exit
from time import sleep
from random import randint
import pygame
from pygame.locals import *

# constants
# window
WIDTH, HEIGHT = 640, 480
TILE_SIZE = 32
CLOCK = pygame.time.Clock()
MAX_FPS = 30
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
# window title
pygame.display.set_caption("Snake")
# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
# game
SCORE = 0


def main():
    global SCORE
    # init screen
    pygame.init()
    playing = True

    # event loop
    while playing:

        # fps
        print(f"{CLOCK}")

        # key presses
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not snake.dir == 2:
                    snake.dir = 1
                if event.key == pygame.K_DOWN and not snake.dir == 1:
                    snake.dir = 2
                if event.key == pygame.K_LEFT and not snake.dir == 4:
                    snake.dir = 3
                if event.key == pygame.K_RIGHT and not snake.dir == 3:
                    snake.dir = 4

        # snake movement
        if snake.dir == 1:  # up
            snake.body.append([snake.body[0][0], snake.body[0][1]])
            snake.body[0][1] -= TILE_SIZE
            snake.body.pop(1)
        elif snake.dir == 2:  # down
            snake.body.append([snake.body[0][0], snake.body[0][1]])
            snake.body[0][1] += TILE_SIZE
            snake.body.pop(1)
        elif snake.dir == 3:  # left
            snake.body.append([snake.body[0][0], snake.body[0][1]])
            snake.body[0][0] -= TILE_SIZE
            snake.body.pop(1)
        elif snake.dir == 4:  # right
            snake.body.append([snake.body[0][0], snake.body[0][1]])
            snake.body[0][0] += TILE_SIZE
            snake.body.pop(1)
        else:
            pass  # don't move

        # boundary collision
        if snake.body[0][0] < 0 or snake.body[0][1] < 0 or snake.body[0][0] > (WIDTH - TILE_SIZE) or snake.body[0][1] > (HEIGHT - TILE_SIZE):
            exit(f"Boop, boundary collision. Game over, your final score was {SCORE}")

        # hit itself
        for n in range(1, len(snake.body) - 1):
            if snake.body[0][0] == snake.body[n][0] and snake.body[0][1] == snake.body[n][1]:
                print(f"You ate part of yourself. Game over, your final score was {SCORE}")
                exit()

        # nom the food
        if snake.body[0][0] == food.x and snake.body[0][1] == food.y:
            # add old x,y to snake
            snake.length += 1
            SCORE += 10
            snake.body.append([food.x, food.y])
            # find new position
            new_x = randint(1, ((WIDTH - TILE_SIZE) / TILE_SIZE))
            new_y = randint(1, ((HEIGHT - TILE_SIZE) / TILE_SIZE))
            # reset x,y and go to new position
            food.x, food.y = 0, 0
            food.x = new_x * TILE_SIZE
            food.y = new_y * TILE_SIZE

        # fill screen
        SCREEN.fill(BLACK)
        # draw objects
        draw_grid()
        for object in objects:
            object.draw()

        pygame.display.update()
        sleep(0.075)
        CLOCK.tick(MAX_FPS)
        system('clear')


def draw_grid():
    for x in range(0, WIDTH, TILE_SIZE):
        for y in range(0, HEIGHT, TILE_SIZE):
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)


class Snake:
    def __init__(self, x, y, color, dir, length=2):
        self.x = x
        self.y = y
        self.color = color
        self.dir = dir
        self.body = [[self.x, self.y], [self.x - TILE_SIZE, self.y]]
        self.length = length

    def draw(self):
        for part in range(self.length):
            rect = pygame.Rect(
                self.body[part][0], self.body[part][1], TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(SCREEN, self.color, rect)


class Food:
    def __init__(self, x, y, color, value=10):
        self.x = x
        self.y = y
        self.color = color
        self.value = value

    def draw(self):
        rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(SCREEN, self.color, rect)


snake = Snake(128, 128, BLUE, 0)
food = Food(256, 256, RED)
objects = []
objects.append(snake)
objects.append(food)


if __name__ == '__main__':
    main()
