# solvers/dfs.py
"""Depth‑First Search (DFS) solver for Maze objects."""
from typing import Tuple, List, Optional
from models.maze import Maze


def _reconstruct(parent: dict[Tuple[int, int], Tuple[int, int]],
                 cur: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Build path by walking backwards through *parent* until the start."""
    path = [cur]
    while cur in parent:
        cur = parent[cur]
        path.append(cur)
    return path[::-1]


def solve(maze: Maze,
          start: Tuple[int, int],
          goal: Tuple[int, int],
          render=None,
          color: Optional[Tuple[int, int, int]] = (0, 255, 0)
          ) -> List[Tuple[int, int]]:
    """Depth‑First Search pathfinder.

    Explores as deep as possible before backtracking. Returns the first
    path found from *start* to *goal*, or an empty list if none exists or
    the run is cancelled via *render*.
    """
    grid = maze.maze  # 0/1 ndarray
    h, w = grid.shape
    inside = lambda p: 0 <= p[0] < h and 0 <= p[1] < w
    if not (inside(start) and inside(goal)) or grid[start] == 0 or grid[goal] == 0:
        raise ValueError("Start/goal invalid")

    stack: List[Tuple[int, int]] = [start]
    parent: dict[Tuple[int, int], Tuple[int, int]] = {}
    visited: set[Tuple[int, int]] = {start}
    frontier_cl = (160, 160, 160)  # grey exploration dots

    while stack:
        if render and not render.running:
            return []

        cur = stack.pop()
        if cur == goal:
            path = _reconstruct(parent, cur)
            maze.add_solution(path, "DFS")
            if render:
                for p in path:
                    render.mark_cell(p, color)
                    render.update()
            return path

        if render:
            render.mark_cell(cur, frontier_cl)  # comment out for silent DFS
            render.update()

        for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nb = (cur[0] + dy, cur[1] + dx)
            if inside(nb) and grid[nb] == 1 and nb not in visited:
                visited.add(nb)
                parent[nb] = cur
                stack.append(nb)

    return []
