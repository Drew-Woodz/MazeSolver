# visualizer/pygame_renderer.py

import pygame
import time

CELL_SIZE = 20  # pixels

class PygameRenderer:
    def __init__(self, maze_width, maze_height):
        self.maze_w = 2 * maze_width + 1
        self.maze_h = 2 * maze_height + 1
        self.cell_size = CELL_SIZE
        self.width = self.maze_w * self.cell_size
        self.height = self.maze_h * self.cell_size
        self.running = True

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Maze Generation")
        self.clock = pygame.time.Clock()

    def draw_maze(self, maze, entry=None, goal=None):
        self.screen.fill((0, 0, 0))
        for y in range(self.maze_h):
            for x in range(self.maze_w):
                if maze[y, x] == 1:
                    rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                    pygame.draw.rect(self.screen, (255, 255, 255), rect)

        if entry:
            ex, ey = entry
            pygame.draw.circle(self.screen, (0, 0, 255), ((ex + 0.5) * self.cell_size, (ey + 0.5) * self.cell_size), self.cell_size // 3)

        if goal:
            gx, gy = goal
            pygame.draw.circle(self.screen, (0, 255, 0), ((gx + 0.5) * self.cell_size, (gy + 0.5) * self.cell_size), self.cell_size // 3)

        pygame.display.flip()


    def update(self, maze, entry=None, goal=None):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        self.draw_maze(maze, entry, goal)
        self.clock.tick(60)
        time.sleep(0.01)


    def wait_for_exit(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
        pygame.quit()

    def close(self):
        pygame.quit()
