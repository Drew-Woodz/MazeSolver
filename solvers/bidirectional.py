# solvers/bidirectional.py
"""Bidirectional BFS solver for Maze objects."""
from collections import deque
from typing import Tuple, List, Optional
from models.maze import Maze


def _reconstruct(parent_from_start: dict[Tuple[int, int], Tuple[int, int]],
                 parent_from_goal: dict[Tuple[int, int], Tuple[int, int]],
                 meet: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Return the path that connects *start* and *goal* through *meet*."""
    # path from start to meet (inclusive)
    path: List[Tuple[int, int]] = []
    n = meet
    while n in parent_from_start:
        path.append(n)
        n = parent_from_start[n]
    path.reverse()

    # path from meet to goal (exclusive of meet)
    n = meet
    while n in parent_from_goal:
        n = parent_from_goal[n]
        path.append(n)
    return path


def solve(maze: Maze,
          start: Tuple[int, int],
          goal: Tuple[int, int],
          render=None,
          color: Optional[Tuple[int, int, int]] = (0, 255, 0)
          ) -> List[Tuple[int, int]]:
    """Bidirectional BFS pathfinder.

    Explores simultaneously from *start* and *goal* until the frontiers
    meet, guaranteeing a shortest path. Returns that path or an empty
    list if none exists or the run is cancelled via *render*.
    """
    grid = maze.maze  # 0/1 ndarray
    h, w = grid.shape
    inside = lambda p: 0 <= p[0] < h and 0 <= p[1] < w

    qs, qg = deque([start]), deque([goal])
    came_s: dict[Tuple[int, int], Tuple[int, int]] = {}
    came_g: dict[Tuple[int, int], Tuple[int, int]] = {}
    vis_s: set[Tuple[int, int]] = {start}
    vis_g: set[Tuple[int, int]] = {goal}

    while qs and qg:
        if render and not render.running:
            return []

        # Expand from start side
        cur = qs.popleft()
        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nb = (cur[0] + dy, cur[1] + dx)
            if inside(nb) and grid[nb] == 1 and nb not in vis_s:
                vis_s.add(nb)
                came_s[nb] = cur
                qs.append(nb)
                if render:
                    render.mark_cell(nb, (150, 150, 255))
                    render.update()
                if nb in vis_g:  # met the other search
                    path = _reconstruct(came_s, came_g, nb)
                    maze.add_solution(path, "Bidirectional")
                    if render:
                        for p in path:
                            render.mark_cell(p, color)
                            render.update()
                    return path

        # Expand from goal side
        cur = qg.popleft()
        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nb = (cur[0] + dy, cur[1] + dx)
            if inside(nb) and grid[nb] == 1 and nb not in vis_g:
                vis_g.add(nb)
                came_g[nb] = cur
                qg.append(nb)
                if render:
                    render.mark_cell(nb, (200, 200, 100))
                    render.update()
                if nb in vis_s:
                    path = _reconstruct(came_s, came_g, nb)
                    maze.add_solution(path, "Bidirectional")
                    if render:
                        for p in path:
                            render.mark_cell(p, color)
                            render.update()
                    return path
    return []


