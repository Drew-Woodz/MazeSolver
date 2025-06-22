import pygame
import numpy as np

class GuiRenderer:
    def __init__(self, maze_width, maze_height):
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.cell_size = min(900 // maze_width, 800 // maze_height)
        self.offset_x = (900 - self.maze_width * self.cell_size) // 2
        self.offset_y = (800 - self.maze_height * self.cell_size) // 2
        self.maze = None
        self.entry = None
        self.goal = None

    def load_maze(self, maze, entry, goal):
        self.maze = maze
        self.entry = entry
        self.goal = goal

    def draw_maze(self, surface):
        pygame.draw.rect(surface, (50, 50, 50), (0, 0, 900, 800))

        if self.maze is None:
            return

        for y in range(self.maze.shape[0]):
            for x in range(self.maze.shape[1]):
                color = (255, 255, 255) if self.maze[y, x] == 1 else (0, 0, 0)
                rect = pygame.Rect(
                    self.offset_x + x * self.cell_size,
                    self.offset_y + y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(surface, color, rect)

        if self.entry:
            ex, ey = self.entry
            pygame.draw.rect(surface, (0, 255, 0), (
                self.offset_x + ex * self.cell_size,
                self.offset_y + ey * self.cell_size,
                self.cell_size,
                self.cell_size))

        if self.goal:
            gx, gy = self.goal
            pygame.draw.rect(surface, (255, 0, 0), (
                self.offset_x + gx * self.cell_size,
                self.offset_y + gy * self.cell_size,
                self.cell_size,
                self.cell_size))
