# solvers/dijkstra.py
import heapq
from typing import List, Tuple, Optional
from models.maze import Maze


def reconstruct(parent, cur):
    path = [cur]
    while cur in parent:
        cur = parent[cur]
        path.append(cur)
    return path[::-1]


def solve(maze: Maze,
          start: Tuple[int, int],
          goal: Tuple[int, int],
          render=None,
          color: Optional[Tuple[int, int, int]] = (0, 255, 0)  # <-- final path = GREEN
          ) -> List[Tuple[int, int]]:

    grid = maze.maze
    h, w = grid.shape
    inside = lambda p: 0 <= p[0] < h and 0 <= p[1] < w
    if not (inside(start) and inside(goal)) or grid[start] == 0 or grid[goal] == 0:
        raise ValueError("Invalid start / goal")

    pq, g, parent = [(0, start)], {start: 0}, {}
    seen = set()

    frontier_colour = (160, 160, 160)          # soft grey (comment out if you want *no* frontier dots)

    while pq:
        if render and not render.running:
            return []

        d, cur = heapq.heappop(pq)
        if cur in seen:
            continue
        seen.add(cur)

        # -------------------- reached goal --------------------
        if cur == goal:
            path = reconstruct(parent, cur)
            maze.add_solution(path, "Dijkstra")
            if render:
                for p in path:                       # paint only once, in GREEN
                    render.mark_cell(p, color)
                    render.update()
            return path
        # ------------------------------------------------------

        for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nb = (cur[0] + dy, cur[1] + dx)
            if inside(nb) and grid[nb] == 1 and nb not in seen:
                nd = d + 1
                if nd < g.get(nb, 1e9):
                    g[nb] = nd
                    parent[nb] = cur
                    heapq.heappush(pq, (nd, nb))

        if render:                                   # frontier dot (grey, optional)
            render.mark_cell(cur, frontier_colour)
            render.update()

    return []
