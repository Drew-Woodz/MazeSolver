# maze_generators/dfs_backtracker.py

import numpy as np
import random
import time
from visualizer.pygame_renderer import PygameRenderer

def generate_maze(width: int, height: int, entry=(0, 0), goal=None, render=None):
    maze_w, maze_h = 2 * width + 1, 2 * height + 1
    maze = np.zeros((maze_h, maze_w), dtype=int)
    visited = set()

    sx, sy = entry
    gx, gy = goal if goal else (width - 1, height - 1)
    start_cell = (2 * sy + 1, 2 * sx + 1)
    goal_cell = (2 * gy + 1, 2 * gx + 1)

    if render:
        render.draw_maze(maze, entry=start_cell, goal=goal_cell)
        render.update()

    def carve_iterative(sx, sy):
        stack = [(sx, sy)]
        visited.add((sx, sy))
        while stack:
            cx, cy = stack.pop()
            maze[2 * cy + 1, 2 * cx + 1] = 1

            dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            random.shuffle(dirs)
            for dx, dy in dirs:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    wall_x = 2 * cx + 1 + dx
                    wall_y = 2 * cy + 1 + dy
                    maze[wall_y, wall_x] = 1
                    stack.append((nx, ny))

                    if render and render.running:
                        render.draw_maze(maze, entry=start_cell, goal=goal_cell)
                        render.update()

    carve_iterative(sx, sy)
    maze[start_cell] = 1
    maze[goal_cell] = 1

    if render:
        render.draw_maze(maze, entry=start_cell, goal=goal_cell)
        render.update()
        
    return maze, start_cell, goal_cell

