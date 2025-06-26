# visualizer/pygame_renderer.py
from models.maze import Maze
from typing import Optional, Tuple
import numpy as np
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import time

MAX_WINDOW_SIZE = 900
MIN_CELL_SIZE = 3

class PygameRenderer:
    def __init__(self, width: int, height: int):
        self.maze_w = width
        self.maze_h = height
        cell_size_w = MAX_WINDOW_SIZE // self.maze_w
        cell_size_h = MAX_WINDOW_SIZE // self.maze_h
        self.cell_size = max(MIN_CELL_SIZE, min(cell_size_w, cell_size_h))
        self.width = self.maze_w * self.cell_size
        self.height = self.maze_h * self.cell_size
        self.running = True
        self.maze = None  # Set later if needed

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Maze Generation")
        self.clock = pygame.time.Clock()
        self.screen.fill((255, 255, 255))  # White canvas
        pygame.display.flip()
        print(f"Renderer initialized: size={self.width}x{self.height}, cell_size={self.cell_size}")

    def set_maze(self, maze: Optional[Maze]):
        """Set the maze object after initialization."""
        self.maze = maze
        if maze:
            print(f"Maze set: shape={maze.maze.shape}")

    def draw_maze(self, maze=None, entry=None, goal=None):
        if maze is None and self.maze is None:
            self.screen.fill((255, 255, 255))  # Keep white if no maze
            print("Drawing empty white maze")
        else:
            maze_to_draw = maze.maze if maze is not None else (self.maze.maze if self.maze is not None else np.zeros((self.maze_h, self.maze_w), dtype=np.int8))
            self.screen.fill((0, 0, 0))  # Clear to black for final draw
            print(f"Drawing maze: shape={maze_to_draw.shape}, first cell={maze_to_draw[0, 0]}")
            for y in range(maze_to_draw.shape[0]):
                for x in range(maze_to_draw.shape[1]):
                    if maze_to_draw[y, x] == 1:
                        rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                        pygame.draw.rect(self.screen, (255, 255, 255), rect)

            entry_pos = entry if entry is not None else (self.maze.start if self.maze else None)
            goal_pos = goal if goal is not None else (self.maze.goal if self.maze else None)
            if entry_pos:
                ex, ey = entry_pos
                pygame.draw.circle(self.screen, (0, 0, 255), ((ex + 0.5) * self.cell_size, (ey + 0.5) * self.cell_size), self.cell_size // 3)
            if goal_pos:
                gx, gy = goal_pos
                pygame.draw.circle(self.screen, (0, 255, 0), ((gx + 0.5) * self.cell_size, (gy + 0.5) * self.cell_size), self.cell_size // 3)

        pygame.display.flip()
    
    def draw_step(self, cell: Tuple[int, int], wall: Tuple[int, int]):
        """Draw a single step (cell and wall) on the white canvas."""
        if self.maze:
            cx, cy = cell  # Cell center (e.g., 12, 11)
            wx, wy = wall  # Wall position (e.g., 25, 24)
            # Map wall to nearest cell edge: adjust for 51x51 grid (walls at odd indices)
            wall_x = (wx - 1) // 2 if wx % 2 else wx // 2 - 1 if wx > 0 else 0  # Edge adjustment
            wall_y = (wy - 1) // 2 if wy % 2 else wy // 2 - 1 if wy > 0 else 0
            print(f"Drawing step: cell=({cx}, {cy}), wall=({wx}, {wy}) -> adjusted=({wall_x}, {wall_y})")
            rect_cell = pygame.Rect(cx * self.cell_size, cy * self.cell_size, self.cell_size, self.cell_size)
            rect_wall = pygame.Rect(wall_x * self.cell_size, wall_y * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, (0, 0, 0), rect_cell)  # Black cell
            pygame.draw.rect(self.screen, (0, 0, 0), rect_wall)  # Black wall
            pygame.display.flip()
            time.sleep(0.1)  # Increased delay

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
        while waiting and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    waiting = False
        pygame.quit()

    def close(self):
        pygame.quit()