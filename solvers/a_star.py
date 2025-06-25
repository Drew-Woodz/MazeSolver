# solvers/a_star.py
from models.maze import Maze

import heapq
from typing import Tuple, List, Optional
import numpy as np

def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def solve(maze: 'Maze', start: Tuple[int, int], goal: Tuple[int, int], 
          render=None, color: Optional[Tuple[int, int, int]] = (0, 255, 0)) -> List[Tuple[int, int]]:
    # --- Sanity checks ---
    def in_bounds(pos):
        y, x = pos
        return 0 <= y < maze.maze.shape[0] and 0 <= x < maze.maze.shape[1]

    if not in_bounds(start):
        raise ValueError(f"Start position {start} is out of bounds for maze size {maze.maze.shape}")
    if not in_bounds(goal):
        raise ValueError(f"Goal position {goal} is out of bounds for maze size {maze.maze.shape}")
    if maze.maze[start[0], start[1]] == 0:
        raise ValueError(f"Start position {start} is a wall")
    if maze.maze[goal[0], goal[1]] == 0:
        raise ValueError(f"Goal position {goal} is a wall")
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

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
            maze.add_solution(path, "A* Search")
            return path

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dy, current[1] + dx)
            if (0 <= neighbor[0] < maze.maze.shape[0] and
                0 <= neighbor[1] < maze.maze.shape[1] and
                maze.maze[neighbor[0], neighbor[1]] == 1 and
                neighbor not in visited):

                tentative_g = g_score[current] + 1

                if tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        if render and render.running:
            render.mark_cell(current, color=(100, 100, 255))  # Trail
            render.update()

    return []