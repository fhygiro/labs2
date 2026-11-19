import pygame
import json
from random import sample
from datetime import datetime
from pathlib import Path

WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)

class Automaton:
    def __init__(self, size):
        self.width = size[0]
        self.height = size[1]
        self.field = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.alive = 0
        self.number_of_step = 0
        self.directions = [
                            (-1, -1), (0, -1), (1, -1),
                            (-1,  0),          (1,  0),
                            (-1,  1), (0,  1), (1,  1)
                        ]

    def random_fill(self, count):
        cells = sample(
            range(self.width * self.height),
            count
        )

        for cell in cells:
            y = cell // self.width
            x = cell % self.width
            self.field[y][x] = 1

        self.alive = count
        self.start_field = [row.copy() for row in self.field]

    def set_field(self, maze):
        if len(maze) == self.height and len(maze[0]) == self.width:
            self.field = maze
            self.count_alive()
            self.number_of_step = 0
            self.start_field = [row.copy() for row in self.field]

    def step(self):
        self.number_of_step+=1
        new_field = [row.copy() for row in self.field]

        for y in range(self.height):
            for x in range(self.width):
                neighbors_cords = [(x + dx, y + dy) 
                                   for dx, dy in self.directions
                                   if 0 <= x + dx < self.width
                                   and 0 <= y + dy < self.height]
                
                neighbors = [self.field[ny][nx] for nx, ny in neighbors_cords]
                alive_neighbors = neighbors.count(1)

                if alive_neighbors < 2:
                    if new_field[y][x] == 1:
                        self.alive -= 1
                    new_field[y][x] = 0

                elif alive_neighbors == 3:
                    if new_field[y][x] == 0:
                        self.alive += 1
                    new_field[y][x] = 1

                elif alive_neighbors >= 4:
                    if new_field[y][x] == 1:
                        self.alive -= 1
                    new_field[y][x] = 0

        self.field = new_field

    def count_alive(self):
        self.alive = sum(row.count(1) for row in self.field)

    def reset(self):
        self.field = [row.copy() for row in self.start_field]
        self.number_of_step = 0
        self.count_alive()

    def terminal_input(self):
        print(f'Итерация {self.number_of_step} - кол-во живых {self.alive}')
        for y in range(self.height):
            print(*self.field[y])
        print()

class Visualizer:
    def __init__(self, automaton, speed, castomiaze):
        self.castomiaze = castomiaze
        self.speed = speed
        self.automaton = automaton
        self.WINDOW_HEIGHT = 1000
        self.WINDOW_WIDTH = 1000
        self.MARGIN = 50
        self.PANEL_WIDTH = 400
        self.FIELD_WIDTH = self.WINDOW_WIDTH - self.MARGIN - self.PANEL_WIDTH
        self.FIELD_HEIGHT = self.WINDOW_HEIGHT - self.MARGIN
        self.running = False
        self.cell_size = min(
            self.FIELD_WIDTH // automaton.width,
            self.FIELD_HEIGHT // automaton.height
        )

        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        self.AUTOMATON_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(self.AUTOMATON_UPDATE, speed)

        self.FONT = pygame.font.Font(None, 40)

    def draw(self):
        self.screen.fill(BLACK)

        step_title = self.FONT.render(f'ИТЕРАЦИЯ: {self.automaton.number_of_step}', True, WHITE)
        alive_title = self.FONT.render(f'ЖИВЫХ: {self.automaton.alive}', True, WHITE)
        speed_title = self.FONT.render(f'СКОРОСТЬ: {1000 / self.speed:.1f} ит/сек', True, WHITE)
        self.screen.blit(step_title, (self.WINDOW_WIDTH - self.PANEL_WIDTH + 20, self.MARGIN))
        self.screen.blit(alive_title, (self.WINDOW_WIDTH - self.PANEL_WIDTH + 20, self.MARGIN + 50))
        self.screen.blit(speed_title, (self.WINDOW_WIDTH - self.PANEL_WIDTH + 20, self.MARGIN + 100))

        for y in range(self.automaton.height):
            for x in range(self.automaton.width):
                rect = pygame.Rect(self.MARGIN + x * self.cell_size, self.MARGIN + y * self.cell_size, self.cell_size, self.cell_size)
                if self.automaton.field[y][x] == 1:
                    pygame.draw.rect(self.screen, WHITE, rect)
                pygame.draw.rect(self.screen, GRAY, rect, 1)
        pygame.display.flip()

    def update(self):
        if self.castomiaze:
            self.automaton.start_field = [row.copy() for row in self.automaton.field]

        self.automaton.step()
        self.castomiaze = False

    def run(self):
        open = True
        clock = pygame.time.Clock()

        while open:
            if self.running:
                pygame.display.set_caption('ПРОЦЕСС ЗАПУЩЕН')
            else:
                pygame.display.set_caption('ПАУЗА')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    open = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.running = not self.running

                    if event.key == pygame.K_r:
                        self.automaton.reset()
                        self.running = False
                        self.castomiaze = True

                    if event.key == pygame.K_n and not self.running:
                        self.automaton.step()

                    if event.key == pygame.K_s:
                        ROOT = Path(__file__).parent
                        filename = ROOT / (datetime.now().strftime('%d-%m-%Y_%H-%M-%S') + '.json')

                        save_automaton(filename, self.automaton)

                    if event.key == pygame.K_RIGHT and self.speed != 100:
                        self.speed-=100
                        pygame.time.set_timer(self.AUTOMATON_UPDATE, self.speed)

                    if event.key == pygame.K_LEFT:
                        self.speed+=100
                        pygame.time.set_timer(self.AUTOMATON_UPDATE, self.speed)

                if event.type == self.AUTOMATON_UPDATE and self.running:
                    self.update()

                if event.type == pygame.MOUSEBUTTONDOWN and self.castomiaze: 
                    mouse_x, mouse_y = event.pos
                    if (self.MARGIN < mouse_x < self.WINDOW_WIDTH - self.MARGIN - self.PANEL_WIDTH and
                        self.MARGIN < mouse_y < self.WINDOW_HEIGHT- self.MARGIN - self.PANEL_WIDTH):
                        
                        x = (mouse_x - self.MARGIN) // self.cell_size
                        y = (mouse_y - self.MARGIN) // self.cell_size
                        
                        if self.automaton.field[y][x] == 0:
                            self.automaton.field[y][x] = 1
                            self.automaton.alive+=1
                        else:
                            self.automaton.field[y][x] = 0
                            self.automaton.alive-=1

            self.draw()
            clock.tick(60)

        pygame.quit()
        
def save_automaton(path, automaton):
    data = {
        'width': automaton.width,
        'height': automaton.height,
        'field': automaton.start_field
    }

    with open(path, 'w') as file:
        json.dump(data, file, indent=4)

def load_automaton(path):
    with open(path, 'r') as file:
        data = json.load(file)
    automaton = Automaton((data['width'], data['height']))
    automaton.set_field(data['field'])
    return automaton

if __name__ == '__main__':
    mode = input('Создать свою конфигурацию (1), загрузить (2), случайно (3): ')

    if mode == '1':
        size = tuple(map(int, input('Размер поля: ').split()))
        automaton = Automaton(size)
        visualizer = Visualizer(automaton, 1000, True)
        visualizer.run()
    elif mode == '2':
        file_conf = input('Путь к файлу конфигурации: ')
        automaton = load_automaton(file_conf)
        visualizer = Visualizer(automaton, 1000, True)
        visualizer.run()
    elif mode == '3':
        size = tuple(map(int, input('Размер поля: ').split()))
        alive = int(input('Кол-во живых: '))
        automaton = Automaton(size)
        automaton.random_fill(alive)
        visualizer = Visualizer(automaton, 1000, True)
        visualizer.run()