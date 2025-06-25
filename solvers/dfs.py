# solvers/dsf.py
from typing import Tuple, List, Optional
import numpy as np

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def solve(maze: np.ndarray,
          start: Tuple[int, int],
          goal: Tuple[int, int],
          render=None,
          color: Optional[Tuple[int, int, int]] = (0, 255, 0)) -> List[Tuple[int, int]]:

    def in_bounds(pos):
        y, x = pos
        return 0 <= y < maze.shape[0] and 0 <= x < maze.shape[1]

    stack = [start]
    came_from = {}
    visited = set()

    while stack:
        if render and not render.running:
            return []

        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            path = reconstruct_path(came_from, current)
            if render and render.running:
                for pos in path:
                    render.mark_cell(pos, color=color)
                    render.update()
            return path

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (current[0] + dy, current[1] + dx)
            if in_bounds(neighbor) and maze[neighbor] == 1 and neighbor not in visited:
                came_from[neighbor] = current
                stack.append(neighbor)

        if render and render.running:
            render.mark_cell(current, color=(200, 200, 100))
            render.update()

    return []
