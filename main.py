#!../env/bin/activate
import pygame
import random
import time
from pygame import surface
from pygame.event import pump
from pygame.locals import *

BLACK = (0, 0, 0)
SIZE = 35
HEIGHT = 840
WIDTH = 840
SCORE_POSITION = WIDTH - SIZE*2

class Food:
    def __init__(self, parent_screen):
        self.rows = HEIGHT / SIZE
        self.columns = WIDTH / SIZE

        self.food = pygame.image.load("linux/src/resources/apple.png").convert()
        self.food = pygame.transform.scale(self.food, (SIZE, SIZE))
        self.x = random.randint(4, self.rows-2) * SIZE
        self.y = random.randint(4, self.columns-2) * SIZE
        self.parent_screen = parent_screen

    def draw(self):
        self.parent_screen.blit(self.food, (self.x, self.y))
        pygame.display.flip()

    def move(self, snake_positions):
        while True:
            self.x = random.randint(1, self.rows-2) * SIZE
            self.y = random.randint(1, self.columns-2) * SIZE

            if (self.x, self.y) not in snake_positions:
                break


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.block = pygame.image.load("linux/src/resources/block.jpg").convert()
        self.block = pygame.transform.scale(self.block, (SIZE, SIZE))
        self.x = [SIZE, SIZE]
        self.y = [SIZE*3, SIZE*2]
        self.direction = "down"
        self.parent_screen = parent_screen

    def get_snake_positions(self):
        positions = []
        for i in range(self.length):
            positions.append((self.x[i], self.y[i]))

        return positions

    def draw(self, surface_color):
        self.parent_screen.fill(surface_color)
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length = self.length + 1
        self.x.append(-1)
        self.y.append(-1)

    def out_of_bounds(self):
        teleporting = ""

        if self.x[0] == 0 - SIZE and teleporting != "left":
            self.x[0] = WIDTH - SIZE
            teleporting = "right"

        if self.x[0] == WIDTH and teleporting != "right":
           self.x[0] = 0
           teleporting = "left"

        if self.y[0] == 0 - SIZE and teleporting != "down":
            self.y[0] = HEIGHT - SIZE
            teleporting = "up"

        if self.y[0] == HEIGHT and teleporting != "up":
            self.y[0] = 0
            teleporting = "down"

    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == "up":
            self.y[0] = self.y[0] - SIZE

        elif self.direction == "down":
            self.y[0] = self.y[0] + SIZE

        elif self.direction == "left":
            self.x[0] = self.x[0] - SIZE

        elif self.direction == "right":
            self.x[0] = self.x[0] + SIZE

        self.out_of_bounds()
        self.draw(BLACK)
        
    def move_up(self):
        if self.direction != "up" and self.direction != "down":
            self.direction = "up"

    def move_down(self):
        if self.direction != "up" and self.direction != "down":
            self.direction = "down"

    def move_left(self):
        if self.direction != "left" and self.direction != "right":
            self.direction = "left"

    def move_right(self):
        if self.direction != "right" and self.direction != "left":
            self.direction = "right"


class Game:
    def __init__(self, width, height, surface_color=BLACK):
        pygame.init()

        self.surface_color = surface_color
        self.surface = pygame.display.set_mode((width, height))
        self.surface.fill(self.surface_color)
        
        pygame.display.set_caption("Snake")
        self.icon = pygame.image.load("linux/src/resources/icon.png").convert()
        self.icon = pygame.transform.scale(self.icon, (32, 32))
        pygame.display.set_icon(self.icon)

        self.snake = Snake(self.surface, 2)
        self.snake.draw(self.surface_color)

        self.food = Food(self.surface)
        self.food.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 == x2 and y1 == y2:
            return True

        return False

    def play(self):
        self.snake.walk()
        
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.food.x, self.food.y):
            self.food.move(self.snake.get_snake_positions())
            self.food.draw()
            self.display_score()
            self.snake.increase_length()
        else:
            self.food.draw()
            self.display_score()

        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Game over!"


    def display_score(self):
        font = pygame.font.SysFont("arial", 30)
        score = font.render(f"{self.snake.length}", True, (200, 200, 200))
        self.surface.blit(score, (SCORE_POSITION, 5))
        pygame.display.flip()

    def show_game_over(self):
        self.surface.fill(BLACK)
        font = pygame.font.SysFont("arial", 30)
        line1 = font.render(f"Game is over! Your score is: {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(line1, (110, 320))
        line2 = font.render(f"To play again press Enter. To exit press Escape!", True, (200, 200, 200))
        self.surface.blit(line2, (110, 370))
        pygame.display.flip()

    def pause(self):
        font = pygame.font.SysFont("arial", 70)
        pause = font.render(f"Game Paused", True, (200, 200, 200))
        self.surface.blit(pause, (185, 350))
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface, 2)
        self.food = Food(self.surface)

    def run(self):
        clock = pygame.time.Clock()
        running = True
        pause = False
        game_over = False
        
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if not pause:
                        if event.key == K_RETURN:
                            game_over = False

                        if not game_over:
                            if event.key == K_p:
                                pause = True

                            if event.key == K_UP:
                                self.snake.move_up()

                            elif event.key == K_DOWN:
                                self.snake.move_down()

                            elif event.key == K_LEFT:
                                self.snake.move_left()

                            elif event.key == K_RIGHT:
                                self.snake.move_right()

                    else:
                        if event.key == K_p:
                                pause = False

                elif event.type == QUIT:
                    running = False

            try:
                if not pause and not game_over:
                    self.play()
                elif pause:
                    self.pause()
            except Exception as e:
                self.show_game_over()
                game_over = True
                self.reset()

            time.sleep(round(0.20-(self.snake.length/1200), 4))
            


if __name__ == "__main__":
    game = Game(WIDTH, HEIGHT)
    game.run()
