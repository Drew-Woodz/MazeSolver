# maze_generators/prims_algorithm.py

import numpy as np
import random
from visualizer.pygame_renderer import PygameRenderer
import time

def generate_maze(width: int, height: int, entry=(0, 0), goal=None, render=None):
    maze_w, maze_h = 2 * width + 1, 2 * height + 1
    maze = np.zeros((maze_h, maze_w), dtype=int)

    sx, sy = entry
    gx, gy = goal if goal else (width - 1, height - 1)
    start_cell = (2 * sy + 1, 2 * sx + 1)
    goal_cell = (2 * gy + 1, 2 * gx + 1)

    if render:
        render.update(maze, entry=start_cell, goal=goal_cell)

    def in_bounds(x, y):
        return 0 <= x < width and 0 <= y < height

    def neighbors(cx, cy):
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = cx + dx, cy + dy
            if in_bounds(nx, ny):
                yield (nx, ny)

    frontier = []
    maze[start_cell] = 1
    visited = {(sx, sy)}

    for nx, ny in neighbors(sx, sy):
        wall = (sx + nx + 1, sy + ny + 1)
        frontier.append(((nx, ny), wall))

    while frontier:
        (cx, cy), (wx, wy) = random.choice(frontier)
        frontier.remove(((cx, cy), (wx, wy)))

        if (cx, cy) in visited:
            continue

        visited.add((cx, cy))
        maze[2 * cy + 1, 2 * cx + 1] = 1
        maze[wy, wx] = 1

        if render and render.running:
            render.update(maze, entry=start_cell, goal=goal_cell)

        for nx, ny in neighbors(cx, cy):
            if (nx, ny) not in visited:
                wall = (cx + nx + 1, cy + ny + 1)
                frontier.append(((nx, ny), wall))

    maze[goal_cell] = 1

    if render:
        render.update(maze, entry=start_cell, goal=goal_cell)
        render.wait_for_exit()

    return maze, start_cell, goal_cell
