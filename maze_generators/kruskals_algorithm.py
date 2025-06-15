# maze_generators/kruskals_algorithm.py

import numpy as np
import random
from visualizer.pygame_renderer import PygameRenderer

class DisjointSet:
    def __init__(self):
        self.parent = {}

    def find(self, cell):
        if self.parent[cell] != cell:
            self.parent[cell] = self.find(self.parent[cell])
        return self.parent[cell]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra
            return True
        return False

def generate_maze(width: int, height: int, entry=(0, 0), goal=None, render=None):
    maze_w, maze_h = 2 * width + 1, 2 * height + 1
    maze = np.zeros((maze_h, maze_w), dtype=int)  # Start with all walls

    sx, sy = entry
    gx, gy = goal if goal else (width - 1, height - 1)
    start_cell = (2 * sy + 1, 2 * sx + 1)
    goal_cell = (2 * gy + 1, 2 * gx + 1)

    ds = DisjointSet()
    cells = [(x, y) for x in range(width) for y in range(height)]
    for cell in cells:
        ds.parent[cell] = cell

    edges = []
    for x in range(width):
        for y in range(height):
            if x < width - 1:
                edges.append(((x, y), (x + 1, y)))
            if y < height - 1:
                edges.append(((x, y), (x, y + 1)))

    random.shuffle(edges)

    for x, y in cells:
        maze[2 * y + 1, 2 * x + 1] = 1  # Carve out cell

    for a, b in edges:
        if ds.union(a, b):
            ax, ay = a
            bx, by = b
            wall_x = ax + bx + 1
            wall_y = ay + by + 1
            maze[wall_y, wall_x] = 1

            if render and render.running:
                render.draw_maze(maze, entry=start_cell, goal=goal_cell)
                render.update()


    maze[start_cell] = 1
    maze[goal_cell] = 1

    if render:
        render.draw_maze(maze, entry=start_cell, goal=goal_cell)
        render.update()

    return maze, start_cell, goal_cell
