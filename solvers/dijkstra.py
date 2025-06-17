# solvers/dijkstra.py
import heapq
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
          color: Optional[Tuple[int, int, int]] = (255, 255, 0)) -> List[Tuple[int, int]]:

    def in_bounds(pos):
        y, x = pos
        return 0 <= y < maze.shape[0] and 0 <= x < maze.shape[1]

    if not in_bounds(start):
        raise ValueError(f"Start {start} out of bounds.")
    if not in_bounds(goal):
        raise ValueError(f"Goal {goal} out of bounds.")
    if maze[start[0], start[1]] == 0:
        raise ValueError(f"Start {start} is a wall.")
    if maze[goal[0], goal[1]] == 0:
        raise ValueError(f"Goal {goal} is a wall.")

    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {start: 0}
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
                    render.mark_cell(pos, color=(0, 255, 0))  # Bright green final path
                    render.update()
            return path

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (current[0] + dy, current[1] + dx)
            if in_bounds(neighbor) and maze[neighbor[0], neighbor[1]] == 1 and neighbor not in visited:
                tentative_g = g_score[current] + 1
                if tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    heapq.heappush(open_set, (tentative_g, neighbor))

        if render and render.running:
            render.mark_cell(current, color=(200, 200, 100))
            render.update()

    return []
