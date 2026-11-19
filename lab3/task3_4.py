import pygame, sys
from random import randrange
from pygame.math import Vector2

CELL_SIZE = 25
COUNT_CELL = 30
OFFSET = 75

RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

pygame.init()

FONT = pygame.font.Font(None, 60)

screen = pygame.display.set_mode((2*OFFSET + CELL_SIZE*COUNT_CELL, 2*OFFSET + CELL_SIZE*COUNT_CELL))
pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()

class Food:
    def __init__(self, snake_body):
        self.position = self.generate_rand_pos(snake_body)

    def draw(self):
        rect = pygame.Rect(OFFSET + self.position.x * CELL_SIZE, OFFSET + self.position.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, RED, rect, 0, 8)

    def create_new(self, snake_body):
        self.position = self.generate_rand_pos(snake_body)

    def generate_rand_pos(self, snake_body):
        position = Vector2(randrange(0, COUNT_CELL), randrange(0, COUNT_CELL))
        while position in snake_body:
            position = Vector2(randrange(0, COUNT_CELL), randrange(0, COUNT_CELL))
        return position

class Snake:
    def __init__(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)
        self.add_segment = False

    def draw(self):
        for segment in self.body:
            rect = pygame.Rect(OFFSET + segment.x * CELL_SIZE, OFFSET + segment.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GREEN, rect, 0, 5)

    def update(self):
        if self.add_segment:
            self.add_segment = False
        else:
            self.body = self.body[:-1]
        self.body.insert(0, self.body[0] + self.direction)

    def reset(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.running = True
        self.score = 0

    def draw(self):
        self.snake.draw()
        self.food.draw()
        self.score_title = FONT.render(f'Счет: {self.score}', True, WHITE)
        screen.blit(self.score_title, (OFFSET-5, 20))

        if not self.running:
            lose_title = FONT.render('Игра окончена', True, WHITE)
            screen.blit(lose_title, (350, 20))

    def update(self):
        if self.running:
            self.check_col_wall()
            if self.running: 
                self.snake.update()
                self.check_col_food()
                self.check_col_tail()

    def check_col_food(self):
        if self.snake.body[0] == self.food.position:
            self.food.create_new(self.snake.body)
            self.snake.add_segment = True
            self.score+=1

    def game_over(self):
        self.running = False

    def reset(self):
        self.running = True
        self.score = 0
        self.snake.reset()
        self.food.create_new(self.snake.body)

    def check_col_wall(self):
        next_pos = self.snake.body[0] + self.snake.direction

        if (next_pos.x < 0 or next_pos.y < 0 or
            next_pos.x >= COUNT_CELL or next_pos.y >= COUNT_CELL):
            self.game_over()

    def check_col_tail(self):
        headless = self.snake.body[1:]
        if self.snake.body[0] in headless:
            self.game_over()

SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 200)

game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SNAKE_UPDATE:
            game.update()

        if event.type == pygame.KEYDOWN:
            if not game.running:
                game.reset()

            if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
                game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
                game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
                game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
                game.snake.direction = Vector2(-1, 0)


    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, WHITE, (OFFSET-5, OFFSET-5, CELL_SIZE*COUNT_CELL+10, CELL_SIZE*COUNT_CELL+10), 5)
    game.draw()

    pygame.display.update()
    clock.tick(60)