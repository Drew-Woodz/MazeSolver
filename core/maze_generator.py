import numpy as np
import random

def generate_maze(width, height, entry=(0,0), goal=None):
    maze_w, maze_h = 2*width+1, 2*height+1
    maze = np.zeros((maze_h, maze_w), dtype=int)
    visited = set()

    def carve_iterative(sx, sy):
        stack = [(sx, sy)]
        visited.add((sx, sy))  # mark on push
        while stack:
            cx, cy = stack.pop()
            maze[2*cy+1, 2*cx+1] = 1
            dirs = [(1,0), (-1,0), (0,1), (0,-1)]
            random.shuffle(dirs)
            for dx, dy in dirs:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited:
                    visited.add((nx, ny))  # mark on push
                    wall_x = 2*cx+1 + dx
                    wall_y = 2*cy+1 + dy
                    maze[wall_y, wall_x] = 1
                    stack.append((nx, ny))

    sx, sy = entry
    carve_iterative(sx, sy)

    # Define exit if not provided
    gx, gy = goal if goal else (width-1, height-1)
    maze[2*sy+1, 2*sx+1] = 1
    maze[2*gy+1, 2*gx+1] = 1

    print(np.sum(maze))  # sanity check: should be > 0
    print("Unique values:", np.unique(maze))
    print("Top-left cell (should be wall):", maze[0, 0])
    print("Path cell (1,1):", maze[1, 1])
    print("Visited cells:", len(visited))
    print("Maze size (walkable grid cells):", width * height)

    return maze, (2*sy+1, 2*sx+1), (2*gy+1, 2*gx+1)
