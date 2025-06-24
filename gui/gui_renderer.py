# gui/gui_renderer.py
import pygame
import numpy as np

class GuiRenderer:
    def __init__(self, maze_width, maze_height, surface):
        """
        Initialize the GUI renderer with the desired maze dimensions and the drawing surface (e.g., screen from app.py).

        This renderer is intended to be compatible with the same interface used by PygameRenderer,
        so it can be passed into maze generators or solvers expecting `draw_maze(maze, entry, goal)` and `update()`.
        """
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.surface = surface  # Reference to the shared pygame display surface

        self.maze = None
        self.entry = None
        self.goal = None

        # Ensure the maze fits inside a fixed-size visual area (900x800)
        self.cell_size = min(900 // maze_width, 800 // maze_height)
        self.running = True  # To match the PygameRenderer API

    def wait_for_exit(self):
        """
        Placeholder for compatibility with PygameRenderer.
        In the GUI context, we do not block for window exit since the app loop handles it.
        """
        pass

    def draw_cell(self, x, y, color):
        """
        Draw a single cell at maze-space coordinate (x, y) using the given color.
        """
        rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(self.surface, color, rect)
        pygame.display.update(rect)

    def clear(self):
        """
        Clear the maze area (left 900px x 800px) to white.
        """
        pygame.draw.rect(self.surface, (255, 255, 255), (0, 0, 900, 800))

    def load_maze(self, maze, entry, goal):
        """
        Store the final generated maze and key coordinates to be drawn during GUI updates.
        """
        self.maze = maze
        self.entry = entry
        self.goal = goal

    def draw_maze_gui(self):
        """
        Draw the stored maze (as loaded by `load_maze()`) to the GUI surface.
        """
        if self.maze is None:
            return

        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                color = (0, 0, 0) if cell == 0 else (255, 255, 255)
                self.draw_cell(x, y, color)

        if self.entry:
            self.draw_cell(self.entry[0], self.entry[1], (0, 255, 0))

        if self.goal:
            self.draw_cell(self.goal[0], self.goal[1], (255, 0, 0))

    def draw_maze(self, maze, entry=None, goal=None):
        """
        Draw a maze directly (used by generators expecting PygameRenderer API).
        This does NOT store the maze internally.
        """
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                color = (0, 0, 0) if cell == 0 else (255, 255, 255)
                self.draw_cell(x, y, color)

        if entry:
            self.draw_cell(entry[0], entry[1], (0, 255, 0))

        if goal:
            self.draw_cell(goal[0], goal[1], (255, 0, 0))

    def mark_cell(self, cell, color=(255, 0, 0)):
        """
        Optional API to match PygameRenderer — allows solvers to highlight a cell.
        """
        y, x = cell
        center = (x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2)
        radius = max(2, self.cell_size // 4)
        pygame.draw.circle(self.surface, color, center, radius)

    def update(self, delay=0.01):
        """
        Process any pending GUI events and flip the display.
        This is a no-op for now since app.py handles event loop, but keeps API compatible.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        pygame.display.flip()
        if delay:
            pygame.time.delay(int(delay * 1000))
