# maze_generators/prims_algorithm.py

import numpy as np
import random

def generate_maze(width: int, height: int, entry=(0, 0), goal=None):
    maze_w, maze_h = 2 * width + 1, 2 * height + 1
    maze = np.zeros((maze_h, maze_w), dtype=int)

    def in_bounds(x, y):
        return 0 <= x < width and 0 <= y < height

    def neighbors(cx, cy):
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = cx + dx, cy + dy
            if in_bounds(nx, ny):
                yield (nx, ny)

    # Cell and wall coordinates live in maze grid space
    frontier = []
    start_x, start_y = entry
    maze[2*start_y+1, 2*start_x+1] = 1

    for nx, ny in neighbors(start_x, start_y):
        wall = (start_x + nx + 1, start_y + ny + 1)
        frontier.append(((nx, ny), wall))

    visited = {(start_x, start_y)}

    while frontier:
        (cx, cy), (wx, wy) = random.choice(frontier)
        frontier.remove(((cx, cy), (wx, wy)))

        if (cx, cy) in visited:
            continue

        visited.add((cx, cy))
        maze[2*cy+1, 2*cx+1] = 1
        maze[wy, wx] = 1

        for nx, ny in neighbors(cx, cy):
            if (nx, ny) not in visited:
                wall = (cx + nx + 1, cy + ny + 1)
                frontier.append(((nx, ny), wall))

    gx, gy = goal if goal else (width-1, height-1)
    maze[2*start_y+1, 2*start_x+1] = 1
    maze[2*gy+1, 2*gx+1] = 1

    return maze, (2*start_y+1, 2*start_x+1), (2*gy+1, 2*gx+1)
