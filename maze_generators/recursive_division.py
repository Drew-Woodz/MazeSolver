# maze_generators/recursive_division.py

import numpy as np
import random
from visualizer.pygame_renderer import PygameRenderer

def generate_maze(width: int, height: int, entry=(0, 0), goal=None, render=None):
    maze_w, maze_h = 2 * width + 1, 2 * height + 1
    maze = np.zeros((maze_h, maze_w), dtype=int)  # Start with all walls

    sx, sy = entry
    gx, gy = goal if goal else (width - 1, height - 1)
    start_cell = (2 * sy + 1, 2 * sx + 1)
    goal_cell = (2 * gy + 1, 2 * gx + 1)

    def divide(x, y, w, h, orientation):
        if w <= 1 or h <= 1:
            return

        horizontal = orientation == 'H'

        if horizontal:
            wy = y + random.randrange(0, h // 2) * 2 + 1
            px = x + random.randrange(0, w // 2) * 2
            for dx in range(0, w):
                wx = x + dx
                if wx == px:
                    continue
                maze[wy, wx] = 0  # wall
                if render and render.running:
                    render.draw_maze(maze, entry=start_cell, goal=goal_cell)
                    render.update()

        else:
            wx = x + random.randrange(0, w // 2) * 2 + 1
            py = y + random.randrange(0, h // 2) * 2
            for dy in range(0, h):
                wy = y + dy
                if wy == py:
                    continue
                maze[wy, wx] = 0  # wall
                if render and render.running:
                    render.draw_maze(maze, entry=start_cell, goal=goal_cell)
                    render.update()


        if horizontal:
            divide(x, y, w, wy - y, choose_orientation(w, wy - y))
            divide(x, wy + 1, w, y + h - wy - 1, choose_orientation(w, y + h - wy - 1))
        else:
            divide(x, y, wx - x, h, choose_orientation(wx - x, h))
            divide(wx + 1, y, x + w - wx - 1, h, choose_orientation(x + w - wx - 1, h))

    def choose_orientation(w, h):
        if w < h:
            return 'H'
        elif h < w:
            return 'V'
        else:
            return random.choice(['H', 'V'])

    # Set all interior cells to path
    maze[1:-1, 1:-1] = 1

    divide(1, 1, maze_w - 2, maze_h - 2, choose_orientation(maze_w - 2, maze_h - 2))

    # Ensure entry and goal are clear paths
    maze[start_cell] = 1
    maze[goal_cell] = 1

    if render:
        render.draw_maze(maze, entry=start_cell, goal=goal_cell)
        render.update()

    return maze, start_cell, goal_cell
