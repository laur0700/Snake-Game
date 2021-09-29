import pygame
import random
import sys
import os
from pygame.constants import K_DOWN, K_ESCAPE, K_LEFT, K_RETURN, K_RIGHT, K_UP, KEYDOWN, QUIT, K_p

BLACK = (0, 0, 0)
SIZE = 30
HEIGHT = 750
WIDTH = 750
MAX_LENGTH = (HEIGHT*WIDTH) // (SIZE*SIZE)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Food:
    def __init__(self, play_surface):
        self.rows = HEIGHT // SIZE - 2
        self.columns = WIDTH // SIZE - 1

        self.food = pygame.image.load(resource_path("resources/apple.png")).convert()
        self.food = pygame.transform.scale(self.food, (SIZE, SIZE))
        self.x = random.randint(6, self.columns) * SIZE
        self.y = random.randint(6, self.rows) * SIZE
        self.play_surface = play_surface

    def draw(self):
        self.play_surface.blit(self.food, (self.x, self.y))

    def move(self, snake_positions):
        while True:
            self.x = random.randint(0, self.columns) * SIZE
            self.y = random.randint(0, self.rows) * SIZE

            if (self.x, self.y) not in snake_positions:
                break


class Snake:
    def __init__(self, play_surface):
        self.length = 2
        self.block = pygame.image.load(resource_path("resources/block.jpg")).convert()
        self.block = pygame.transform.scale(self.block, (SIZE, SIZE))
        self.x = [SIZE*4, SIZE*4]
        self.y = [SIZE*5, SIZE*4]
        self.direction = "down"
        self.play_surface = play_surface

    def draw(self):
        for i in range(self.length):
            self.play_surface.blit(self.block, (self.x[i], self.y[i]))

    def get_snake_positions(self):
        snake_positions = []
        for i in range(self.length):
            snake_positions.append((self.x[i], self.y[i]))

        return snake_positions

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
            self.y[0] = HEIGHT - SIZE*2
            teleporting = "up"

        if self.y[0] == HEIGHT - SIZE and teleporting != "up":
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
        self.draw()
        
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
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Snake")

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font = pygame.font.Font(resource_path("resources/arial.ttf"), SIZE)

        self.score_surface = pygame.Surface([WIDTH, SIZE])
        self.score_surface.fill((200, 200, 200))

        self.play_surface = pygame.Surface([WIDTH, HEIGHT - SIZE])
        self.play_surface.fill(BLACK)

        self.snake = Snake(self.play_surface)
        self.snake.draw()

        self.food = Food(self.play_surface)
        self.food.draw()

        self.display_score()

        self.screen.blit(self.score_surface, (0, 0))
        self.screen.blit(self.play_surface, (0, SIZE))
        pygame.display.flip()

        self.game_over = False
        self.reset = False

        self.run()

    def is_collision(self, x1, y1, x2, y2):
        if x1 == x2 and y1 == y2:
            return True

        return False

    def play(self):
        self.play_surface.fill(BLACK)
        self.snake.walk()
        
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.food.x, self.food.y):
            self.snake.increase_length()
            self.food.move(self.snake.get_snake_positions())
            self.food.draw()
            self.display_score()
        else:
            self.food.draw()
            self.display_score()

        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.show_game_over()


    def display_score(self):
        self.score_surface.fill((200, 200, 200))
        score = self.font.render(f"{self.snake.length - 2}", True, (0, 0, 0))
        self.score_surface.blit(score, (7, 0))
        self.screen.blit(self.score_surface, (0, 0))

    def show_game_over(self):
        self.play_surface.fill(BLACK)
        line1 = self.font.render(f"Game is over! Your score is: {self.snake.length - 2}", True, (220, 220, 220))
        self.play_surface.blit(line1, (50, HEIGHT//2 - SIZE*3))
        line2 = self.font.render(f"To play again press Enter. To exit press Escape!", True, (220, 220, 220))
        self.play_surface.blit(line2, (50, HEIGHT//2 - SIZE))
        self.game_over = True

    def pause(self):
        self.display_score()
        font = pygame.font.Font(resource_path("resources/arial.ttf"), 25)
        pause = font.render(f"Game Paused", True, (0, 0, 0))
        self.score_surface.blit(pause, (295, 0))
        self.screen.blit(self.score_surface, (0, 0))

    def reset_game(self):
        self.score_surface.fill((200, 200, 200))
        self.play_surface.fill(BLACK)

        self.snake = Snake(self.play_surface)
        self.snake.draw()

        self.food = Food(self.play_surface)
        self.food.draw()

        self.display_score()

        self.screen.blit(self.score_surface, (0, 0))
        self.screen.blit(self.play_surface, (0, SIZE))
        pygame.display.flip()

        self.reset = False
        self.game_over = False

    def run(self):
        running = True
        pause = False
        
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if not pause:
                        if event.key == K_RETURN:
                            self.reset = True

                        if not self.game_over:
                            if event.key == K_p:
                                pause = True

                            if event.key == K_UP:
                                self.snake.move_up()
                                break

                            elif event.key == K_DOWN:
                                self.snake.move_down()
                                break

                            elif event.key == K_LEFT:
                                self.snake.move_left()
                                break

                            elif event.key == K_RIGHT:
                                self.snake.move_right()
                                break

                    else:
                        if event.key == K_p:
                                pause = False

                elif event.type == QUIT:
                    running = False

            if not self.game_over:
                if not pause:
                    self.play()
                elif pause:
                    self.pause()
            elif not self.reset:
                self.show_game_over()
            else:
                self.reset_game()
                

            self.screen.blit(self.play_surface, (0, SIZE))
            pygame.display.flip()
            self.clock.tick(round(6.7 + ((self.snake.length - MAX_LENGTH) / 1000)*3, 4))
            

def main():
    game = Game()


if __name__ == "__main__":
    main()
