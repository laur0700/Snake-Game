import pygame
import random
import time
from pygame import surface
from pygame.locals import *

BLACK = (0, 0, 0)
SIZE = 40
HEIGHT = 840
WIDTH = 840

class Food:
    def __init__(self, parent_screen):
        self.rows = HEIGHT / SIZE
        self.columns = WIDTH / SIZE

        self.food = pygame.image.load("resources/apple.png").convert()
        self.food = pygame.transform.scale(self.food, (SIZE, SIZE))
        self.x = random.randint(4, self.rows-1) * SIZE
        self.y = random.randint(4, self.columns-1) * SIZE
        self.parent_screen = parent_screen

    def draw(self):
        self.parent_screen.blit(self.food, (self.x, self.y))
        pygame.display.flip()

    def move(self, snake_positions):
        while True:
            self.x = random.randint(0, self.rows-1) * SIZE
            self.y = random.randint(0, self.columns-1) * SIZE

            if (self.x, self.y) not in snake_positions:
                break


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.block = pygame.transform.scale(self.block, (SIZE, SIZE))
        self.x = [0, 0]
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

    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == "up":
            self.y[0] = self.y[0] - SIZE

        if self.direction == "down":
            self.y[0] = self.y[0] + SIZE

        if self.direction == "left":
            self.x[0] = self.x[0] - SIZE

        if self.direction == "right":
            self.x[0] = self.x[0] + SIZE
        
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

        self.snake = Snake(self.surface, 2)
        self.snake.draw(self.surface_color)

        self.food = Food(self.surface)
        self.food.draw()

    def out_of_bounds(self):
        if self.snake.x[0] == 0 - SIZE:
            self.snake.x[0] = WIDTH - SIZE

        if self.snake.x[0] == WIDTH:
           self.snake.x[0] = 0

        if self.snake.y[0] == 0 - SIZE:
            self.snake.y[0] = HEIGHT - SIZE

        if self.snake.y[0] == HEIGHT:
            self.snake.y[0] = 0

    def is_collision(self, x1, y1, x2, y2):
        if x1 == x2 and y1 == y2:
            return True

        return False

    def play(self):
        self.out_of_bounds()
        self.snake.walk()
        self.food.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.food.x, self.food.y):
            self.food.move(self.snake.get_snake_positions())
            self.snake.increase_length()

        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Game over!"

    def display_score(self):
        font = pygame.font.SysFont("arial", 30)
        score = font.render(f"{self.snake.length}", True, (200, 200, 200))
        self.surface.blit(score, (750, 10))

    def show_game_over(self):
        self.surface.fill(BLACK)
        font = pygame.font.SysFont("arial", 30)
        line1 = font.render(f"Game is over! Your score is: {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(line1, (115, 300))
        line2 = font.render(f"To play again press Enter. To exit press Escape!", True, (200, 200, 200))
        self.surface.blit(line2, (115, 350))
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface, 2)
        self.food = Food(self.surface)

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.20-(self.snake.length/1000))


if __name__ == "__main__":
    game = Game(WIDTH, HEIGHT)
    game.run()