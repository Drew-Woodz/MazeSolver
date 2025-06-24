import pygame
import numpy as np

class GuiRenderer:
    def __init__(self, maze_width, maze_height):
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.maze = None
        self.entry = None
        self.goal = None
        self.cell_size = min(900 // maze_width, 800 // maze_height)

    def wait_for_exit(self):
        pass


    def draw_cell(self, surface, x, y, color):
        pygame.draw.rect(surface, color, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
        pygame.display.update()

    def clear(self, surface,):
        pygame.draw.rect(surface, (255, 255, 255), (0, 0, 900, 800))

    def load_maze(self, maze, entry, goal):
        self.maze = maze
        self.entry = entry
        self.goal = goal

    def draw_maze(self, surface):
        if self.maze is None:
            return
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                color = (0, 0, 0) if cell == 0 else (255, 255, 255)
                pygame.draw.rect(surface, color, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
        if self.entry:
            pygame.draw.rect(surface, (0, 255, 0), (self.entry[0] * self.cell_size, self.entry[1] * self.cell_size, self.cell_size, self.cell_size))
        if self.goal:
            pygame.draw.rect(surface, (255, 0, 0), (self.goal[0] * self.cell_size, self.goal[1] * self.cell_size, self.cell_size, self.cell_size))

