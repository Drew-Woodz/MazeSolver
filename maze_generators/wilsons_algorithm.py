# maze_generators/wilsons_algorithm.py

import matplotlib.pyplot as plt
import numpy as np
import random

def generate_maze(width: int, height: int, entry=(0, 0), goal=None):
    maze_w, maze_h = 2 * width + 1, 2 * height + 1
    maze = np.zeros((maze_h, maze_w), dtype=int)

    def cell_to_maze_coords(x, y):
        return 2 * y + 1, 2 * x + 1  # returns (row, col)


    all_cells = [(x, y) for x in range(width) for y in range(height)]
    in_tree = set()

    # Start with one random cell in the tree
    start_cell = random.choice(all_cells)
    in_tree.add(start_cell)

    while len(in_tree) < len(all_cells):
        walk_start = random.choice([cell for cell in all_cells if cell not in in_tree])
        path = [walk_start]
        visited_in_walk = {walk_start}
        cx, cy = walk_start

        while (cx, cy) not in in_tree:
            dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            dx, dy = random.choice(dirs)
            nx, ny = cx + dx, cy + dy

            if 0 <= nx < width and 0 <= ny < height:
                next_cell = (nx, ny)

                if next_cell in path:
                    loop_start = path.index(next_cell)
                    path = path[:loop_start + 1]
                else:
                    path.append(next_cell)
                    visited_in_walk.add(next_cell)

                cx, cy = next_cell

        # Add the path to the tree
        for i in range(len(path)):
            px, py = path[i]
            maze_row, maze_col = cell_to_maze_coords(px, py)
            maze[maze_row, maze_col] = 1
            in_tree.add((px, py))

            if i > 0:
                prev_x, prev_y = path[i - 1]
                prev_row, prev_col = cell_to_maze_coords(prev_x, prev_y)
                wall_row = (maze_row + prev_row) // 2
                wall_col = (maze_col + prev_col) // 2
                maze[wall_row, wall_col] = 1



    # Add entry and goal
    sx, sy = entry
    gx, gy = goal if goal else (width - 1, height - 1)
    maze[2 * sy + 1, 2 * sx + 1] = 1
    maze[2 * gy + 1, 2 * gx + 1] = 1

    plt.imshow(maze, cmap="gray")
    plt.title("Debug Maze View")
    plt.show()


    return maze, (2 * sy + 1, 2 * sx + 1), (2 * gy + 1, 2 * gx + 1)
