# solvers/bfs.py

from collections import deque
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

    if not in_bounds(start):
        raise ValueError(f"Start {start} is out of bounds.")
    if not in_bounds(goal):
        raise ValueError(f"Goal {goal} is out of bounds.")
    if maze[start[0], start[1]] == 0:
        raise ValueError(f"Start {start} is a wall.")
    if maze[goal[0], goal[1]] == 0:
        raise ValueError(f"Goal {goal} is a wall.")

    queue = deque([start])
    came_from = {}
    visited = set([start])

    while queue:
        if render and not render.running:
            return []

        current = queue.popleft()

        if current == goal:
            path = reconstruct_path(came_from, current)
            if render and render.running:
                for pos in path:
                    render.mark_cell(pos, color=color)
                    render.update()
            return path

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dy, current[1] + dx)
            if in_bounds(neighbor) and maze[neighbor[0], neighbor[1]] == 1 and neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)

        if render and render.running:
            render.mark_cell(current, color=(200, 100, 255))  # Soft pink trail
            render.update()

    return []
