# solvers/bidirectional.py
from collections import deque
from typing import Tuple, List, Optional
from models.maze import Maze

def _reconstruct(meet, came_s, came_g):
    # path from start ➜ meet
    path = []
    n = meet
    while n in came_s:
        path.append(n)
        n = came_s[n]
    path.reverse()
    # meet ➜ goal
    n = meet
    while n in came_g:
        n = came_g[n]
        path.append(n)
    return path

def solve(maze: Maze, start: Tuple[int,int], goal: Tuple[int,int],
          render=None, color: Optional[Tuple[int,int,int]]=(0,255,0)) -> List[Tuple[int,int]]:

    grid = maze.maze
    h, w = grid.shape
    inside = lambda p: 0 <= p[0] < h and 0 <= p[1] < w

    qs, qg          = deque([start]), deque([goal])
    came_s, came_g  = {}, {}
    vis_s, vis_g    = {start}, {goal}

    while qs and qg:
        if render and not render.running:
            return []

        # --- expand from start side
        cur = qs.popleft()
        for dy, dx in [(0,1),(0,-1),(1,0),(-1,0)]:
            nb = (cur[0]+dy, cur[1]+dx)
            if inside(nb) and grid[nb]==1 and nb not in vis_s:
                vis_s.add(nb); came_s[nb]=cur; qs.append(nb)
                if render: render.mark_cell(nb,(150,150,255)); render.update()
                if nb in vis_g:            # met the other search
                    path = _reconstruct(nb, came_s, came_g)
                    maze.add_solution(path,"Bidirectional")
                    if render:
                        for p in path: render.mark_cell(p,color); render.update()
                    return path

        # --- expand from goal side
        cur = qg.popleft()
        for dy, dx in [(0,1),(0,-1),(1,0),(-1,0)]:
            nb = (cur[0]+dy, cur[1]+dx)
            if inside(nb) and grid[nb]==1 and nb not in vis_g:
                vis_g.add(nb); came_g[nb]=cur; qg.append(nb)
                if render: render.mark_cell(nb,(200,200,100)); render.update()
                if nb in vis_s:
                    path = _reconstruct(nb, came_s, came_g)
                    maze.add_solution(path,"Bidirectional")
                    if render:
                        for p in path: render.mark_cell(p,color); render.update()
                    return path
    return []

