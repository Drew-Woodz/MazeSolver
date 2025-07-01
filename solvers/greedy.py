# solvers/greedy.py
"""Greedy Best‑First Search (GBFS) solver for Maze objects."""
import heapq
from typing import Tuple, List, Optional
from models.maze import Maze


def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    """Manhattan distance between *a* and *b* (4‑connected grid)."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _reconstruct(parent: dict[Tuple[int, int], Tuple[int, int]],
                 cur: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Rebuild path from *start* to *cur* using the *parent* map."""
    path = [cur]
    while cur in parent:
        cur = parent[cur]
        path.append(cur)
    return path[::-1]


def solve(maze: Maze,
          start: Tuple[int, int],
          goal: Tuple[int, int],
          render=None,
          color: Optional[Tuple[int, int, int]] = (255, 165, 0)
          ) -> List[Tuple[int, int]]:
    """Greedy Best‑First Search pathfinder.

    Explores the neighbour with the smallest heuristic (Manhattan)
    distance to the *goal*. Fast but not optimal—may return a longer path
    than BFS or A*. Returns the discovered path or an empty list if none
    exists or the run is cancelled via *render*.
    """
    grid = maze.maze  # 0/1 ndarray
    h, w = grid.shape

    def inside(p: Tuple[int, int]) -> bool:
        return 0 <= p[0] < h and 0 <= p[1] < w

    if not (inside(start) and inside(goal)) or grid[start] == 0 or grid[goal] == 0:
        raise ValueError("Start/goal invalid")

    pq: list[tuple[int, Tuple[int, int]]] = [(heuristic(start, goal), start)]
    came: dict[Tuple[int, int], Tuple[int, int]] = {}
    seen: set[Tuple[int, int]] = set()

    while pq:
        if render and not render.running:
            return []
        _, cur = heapq.heappop(pq)
        if cur in seen:
            continue
        seen.add(cur)
        if cur == goal:
            path = _reconstruct(came, cur)
            maze.add_solution(path, "Greedy BFS")
            if render:
                for p in path:
                    render.mark_cell(p, color)
                    render.update()
            return path
        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nb = (cur[0] + dy, cur[1] + dx)
            if inside(nb) and grid[nb] == 1 and nb not in seen:
                came[nb] = cur
                heapq.heappush(pq, (heuristic(nb, goal), nb))
        if render:
            render.mark_cell(cur, (255, 200, 0))
            render.update()
    return []
