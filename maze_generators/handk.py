# maze_generators/handk.py
import numpy as np
import random
from visualizer.pygame_renderer import PygameRenderer

def generate_maze(width: int, height: int, entry=(0, 0), goal=None, render=None):
    maze_w, maze_h = 2 * width + 1, 2 * height + 1
    maze = np.zeros((maze_h, maze_w), dtype=int)  # Start with walls

    sx, sy = entry
    gx, gy = goal if goal else (width - 1, height - 1)
    start_cell = (2 * sy + 1, 2 * sx + 1)
    goal_cell = (2 * gy + 1, 2 * gx + 1)

    visited = set()
    cx, cy = sx, sy

    def visit(x, y):
        maze[2 * y + 1, 2 * x + 1] = 1
        visited.add((x, y))

    def neighbors(x, y):
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                yield nx, ny

    visit(cx, cy)

    while True:
        unvisited = [(nx, ny) for nx, ny in neighbors(cx, cy) if (nx, ny) not in visited]
        if unvisited:
            nx, ny = random.choice(unvisited)
            wall_x = 2 * (cx + nx) // 2 + 1
            wall_y = 2 * (cy + ny) // 2 + 1
            maze[wall_y, wall_x] = 1
            visit(nx, ny)
            cx, cy = nx, ny
        else:
            # Hunt phase: find any unvisited cell next to a visited one
            found = False
            for y in range(height):
                for x in range(width):
                    if (x, y) not in visited:
                        for nx, ny in neighbors(x, y):
                            if (nx, ny) in visited:
                                visit(x, y)
                                wall_x = 2 * (x + nx) // 2 + 1
                                wall_y = 2 * (y + ny) // 2 + 1
                                maze[wall_y, wall_x] = 1
                                cx, cy = x, y
                                found = True
                                break
                    if found:
                        break
                if found:
                    break
            if not found:
                break

        if render and render.running:
            render.draw_maze(maze, entry=start_cell, goal=goal_cell)
            render.update()


    maze[start_cell] = 1
    maze[goal_cell] = 1

    if render:
        render.draw_maze(maze, entry=start_cell, goal=goal_cell)
        render.update()

    return maze, start_cell, goal_cell
