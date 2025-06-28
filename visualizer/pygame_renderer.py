# visualizer/pygame_renderer.py – v2 (blank‑screen fix + correct colours)
from models.maze import Maze
from typing import Optional, Tuple
import os, pygame, time
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

MIN_CELL_SIZE = 1

class PygameRenderer:
    def __init__(self, width: int, height: int):
        pygame.init()
        info = pygame.display.Info()
        self.max_sz = min(900, info.current_w, info.current_h)
        self.mw, self.mh = width, height
        self.cell = max(MIN_CELL_SIZE, min(self.max_sz // self.mw, self.max_sz // self.mh))
        self.w, self.h = self.mw * self.cell, self.mh * self.cell

        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Maze Generation")
        self.clock, self.running, self.maze = pygame.time.Clock(), True, None

        # Start with BLACK walls; we will carve WHITE paths
        self.screen.fill((0, 0, 0))
        pygame.display.flip()
        print(f"Renderer init → {self.w}×{self.h}, cell={self.cell}")

    # ------------------------------------------------------------------- util
    def _rect(self, gx: int, gy: int):
        return pygame.Rect(gx * self.cell, gy * self.cell, self.cell, self.cell)

    # -------------------------------------------------------------- public API
    def set_maze(self, maze: Optional[Maze]):
        self.maze = maze
        if maze:
            print(f"Maze set → shape {maze.maze.shape}")

    def draw_step(self, step: Tuple[Tuple[int, int], Tuple[int, int]]):
        """Replay one carving step — draw white for path (1) and black for wall (0)."""
        if not (self.running and self.maze):
            return

        (gy, gx), (wy, wx) = step            # grid-space coords

        # -- first point --
        color = (255, 255, 255) if self.maze.maze[gy, gx] else (0, 0, 0)
        pygame.draw.rect(self.screen, color, self._rect(gx, gy))

        # -- second point (may be same as first) --
        color = (255, 255, 255) if self.maze.maze[wy, wx] else (0, 0, 0)
        pygame.draw.rect(self.screen, color, self._rect(wx, wy))

        pygame.display.flip()
        time.sleep(0.015)                    # tweak speed to taste

    def draw_maze(self, maze: Optional[Maze] = None):
        maze = maze or self.maze
        if maze is None:
            return
        self.screen.fill((0, 0, 0))  # reset to walls
        grid = maze.maze
        for gy in range(grid.shape[0]):
            for gx in range(grid.shape[1]):
                if grid[gy, gx]:  # path
                    pygame.draw.rect(self.screen, (255, 255, 255), self._rect(gx, gy))
        # Markers
        sx, sy = maze.start[1], maze.start[0]
        gx, gy = maze.goal[1],  maze.goal[0]
        pygame.draw.circle(self.screen, (0, 0, 255), (sx * self.cell + self.cell//2, sy * self.cell + self.cell//2), self.cell//3)
        pygame.draw.circle(self.screen, (0, 255, 0), (gx * self.cell + self.cell//2, gy * self.cell + self.cell//2), self.cell//3)
        pygame.display.flip()

    def mark_cell(self, cell, color=(255, 0, 0)):
        gy, gx = cell
        pygame.draw.circle(self.screen, color, (gx * self.cell + self.cell//2, gy * self.cell + self.cell//2), max(2, self.cell//4))

    def update(self, delay: float = 0.0):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False
        pygame.display.flip()
        self.clock.tick(60)
        if delay:
            time.sleep(delay)

    def wait_for_exit(self):
        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                    self.running = False
        pygame.quit()