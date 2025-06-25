# visualizer/pygame_renderer.py
from models.maze import Maze
import numpy as np
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import time

MAX_WINDOW_SIZE = 900
MIN_CELL_SIZE = 3

class PygameRenderer:
    def __init__(self, maze: 'Maze'):
        self.maze_w = maze.maze.shape[1]
        self.maze_h = maze.maze.shape[0]
        cell_size_w = MAX_WINDOW_SIZE // self.maze_w
        cell_size_h = MAX_WINDOW_SIZE // self.maze_h
        self.cell_size = max(MIN_CELL_SIZE, min(cell_size_w, cell_size_h))
        self.width = self.maze_w * self.cell_size
        self.height = self.maze_h * self.cell_size
        self.running = True

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Maze Generation")
        self.clock = pygame.time.Clock()

    def draw_maze(self, maze=None, entry=None, goal=None):
        self.screen.fill((0, 0, 0))
        maze_to_draw = maze.maze if maze is not None else np.zeros((self.maze_h, self.maze_w), dtype=np.int8)
        for y in range(self.maze_h):
            for x in range(self.maze_w):
                if maze_to_draw[y, x] == 1:
                    rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                    pygame.draw.rect(self.screen, (255, 255, 255), rect)

        entry_pos = entry if entry is not None else (maze.start if maze is not None else None)
        goal_pos = goal if goal is not None else (maze.goal if maze is not None else None)
        if entry_pos:
            ex, ey = entry_pos
            pygame.draw.circle(self.screen, (0, 0, 255), ((ex + 0.5) * self.cell_size, (ey + 0.5) * self.cell_size), self.cell_size // 3)
        if goal_pos:
            gx, gy = goal_pos
            pygame.draw.circle(self.screen, (0, 255, 0), ((gx + 0.5) * self.cell_size, (gy + 0.5) * self.cell_size), self.cell_size // 3)

        pygame.display.flip()
    
    def mark_cell(self, cell, color=(255, 0, 0)):
        if not self.running:
            return
        y, x = cell
        center = (x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2)
        radius = max(2, self.cell_size // 4)
        pygame.draw.circle(self.screen, color, center, radius)

    def update(self, delay=0.01):
        if not self.running:
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        pygame.display.flip()
        self.clock.tick(60)
        if delay:
            time.sleep(delay)

    def wait_for_exit(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    waiting = False
        pygame.quit()

    def close(self):
        pygame.quit()