# solvers/a_star.py
"""A* (A‑star) solver for Maze objects."""
from models.maze import Maze

import heapq
from typing import Tuple, List, Optional, Dict

# NumPy is only needed for type annotations, not imported here

def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    """Manhattan distance between *a* and *b*."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def reconstruct_path(came_from: Dict[Tuple[int, int], Tuple[int, int]],
                     current: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Return the path from the start node to *current*."""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def solve(maze: Maze,
          start: Tuple[int, int],
          goal: Tuple[int, int],
          render=None,
          color: Optional[Tuple[int, int, int]] = (0, 255, 0)
          ) -> List[Tuple[int, int]]:
    """A* shortest‑path solver.

    Combines Dijkstra's algorithm with a heuristic (Manhattan distance)
    to find an optimal path efficiently. Returns the path or an empty
    list if none exists or the run is cancelled via *render*.
    """
    # --- Sanity checks --------------------------------------------------
    rows, cols = maze.maze.shape

    def in_bounds(pos: Tuple[int, int]) -> bool:
        y, x = pos
        return 0 <= y < rows and 0 <= x < cols

    if not in_bounds(start):
        raise ValueError(f"Start position {start} is out of bounds for maze size {maze.maze.shape}")
    if not in_bounds(goal):
        raise ValueError(f"Goal position {goal} is out of bounds for maze size {maze.maze.shape}")
    if maze.maze[start] == 0:
        raise ValueError(f"Start position {start} is a wall")
    if maze.maze[goal] == 0:
        raise ValueError(f"Goal position {goal} is a wall")

    # Priority queue holds (f_score, cell)
    open_set: List[Tuple[int, Tuple[int, int]]] = []
    heapq.heappush(open_set, (0, start))

    came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
    g_score: Dict[Tuple[int, int], int] = {start: 0}
    f_score: Dict[Tuple[int, int], int] = {start: heuristic(start, goal)}

    visited: set[Tuple[int, int]] = set()

    while open_set:
        if render and not render.running:
            return []

        _, current = heapq.heappop(open_set)
        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            path = reconstruct_path(came_from, current)
            maze.add_solution(path, "A* Search")
            if render and render.running:
                for pos in path:
                    render.mark_cell(pos, color=color)
                    render.update()
            return path

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dy, current[1] + dx)
            if (in_bounds(neighbor)
                    and maze.maze[neighbor] == 1
                    and neighbor not in visited):

                tentative_g = g_score[current] + 1
                if tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + heuristic(neighbor, goal)
                    f_score[neighbor] = f
                    heapq.heappush(open_set, (f, neighbor))

        if render and render.running:
            render.mark_cell(current, color=(100, 100, 255))  # Trail
            render.update()

    return []
