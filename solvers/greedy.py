# solvers/greedy.py

import heapq
import numpy as np
from typing import Tuple, List, Optional

def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

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
        raise ValueError(f"Start {start} out of bounds.")
    if not in_bounds(goal):
        raise ValueError(f"Goal {goal} out of bounds.")
    if maze[start[0], start[1]] == 0 or maze[goal[0], goal[1]] == 0:
        raise ValueError("Start or goal is a wall.")

    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), start))
    came_from = {}
    visited = set()

    while open_set:
        if render and not render.running:
            return []

        _, current = heapq.heappop(open_set)
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

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dy, current[1] + dx)
            if in_bounds(neighbor) and maze[neighbor[0], neighbor[1]] == 1 and neighbor not in visited:
                came_from[neighbor] = current
                heapq.heappush(open_set, (heuristic(neighbor, goal), neighbor))

        if render and render.running:
            render.mark_cell(current, color=(255, 200, 0))  # warm yellow-orange
            render.update()

    return []
