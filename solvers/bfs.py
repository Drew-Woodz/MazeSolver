# solvers/bfs.py

from collections import deque
from typing import Tuple, List, Optional
from models.maze import Maze


def _reconstruct(parent, cur):
    path = [cur]
    while cur in parent:
        cur = parent[cur]
        path.append(cur)
    return path[::-1]


def solve(maze: Maze, start: Tuple[int, int], goal: Tuple[int, int],
          render=None, color: Optional[Tuple[int, int, int]] = (0, 255, 0)) -> List[Tuple[int, int]]:
    """Breadth‑First Search that works with the new Maze class."""
    grid = maze.maze  # 0/1 ndarray
    h, w = grid.shape

    def inside(p):
        return 0 <= p[0] < h and 0 <= p[1] < w

    if not (inside(start) and inside(goal)) or grid[start] == 0 or grid[goal] == 0:
        raise ValueError("Start/goal invalid or in wall")

    q = deque([start])
    parent = {}
    visited = {start}

    while q:
        if render and not render.running:
            return []
        cur = q.popleft()
        if cur == goal:
            path = _reconstruct(parent, cur)
            maze.add_solution(path, "BFS")
            if render:
                for pos in path:
                    render.mark_cell(pos, color)
                    render.update()
            return path
        for dy, dx in [(0,1), (0,-1), (1,0), (-1,0)]:
            nb = (cur[0] + dy, cur[1] + dx)
            if inside(nb) and grid[nb] == 1 and nb not in visited:
                visited.add(nb)
                parent[nb] = cur
                q.append(nb)
                if render:
                    render.mark_cell(nb, (150, 150, 255))
                    render.update()
    return []