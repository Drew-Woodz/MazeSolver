# solvers/dijkstra.py – new interface
import heapq
from typing import List, Tuple, Optional
from models.maze import Maze

def reconstruct(par, cur):
    p=[cur]
    while cur in par:
        cur=par[cur]; p.append(cur)
    return p[::-1]

def solve(maze: Maze, start: Tuple[int,int], goal: Tuple[int,int],
          render=None, color: Optional[Tuple[int,int,int]]=(255,255,0)) -> List[Tuple[int,int]]:
    grid = maze.maze
    h,w = grid.shape
    def inside(p): return 0<=p[0]<h and 0<=p[1]<w
    if not (inside(start) and inside(goal)) or grid[start]==0 or grid[goal]==0:
        raise ValueError("Invalid start/goal")

    pq, g, par = [(0,start)], {start:0}, {}
    seen=set()
    while pq:
        if render and not render.running: return []
        d, cur = heapq.heappop(pq)
        if cur in seen: continue
        seen.add(cur)
        if cur==goal:
            path=reconstruct(par,cur)
            maze.add_solution(path,"Dijkstra")
            if render:
                for p in path: render.mark_cell(p,color); render.update()
            return path
        for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
            nb=(cur[0]+dy,cur[1]+dx)
            if inside(nb) and grid[nb]==1 and nb not in seen:
                nd = d+1
                if nd < g.get(nb, 1e9):
                    g[nb]=nd; par[nb]=cur; heapq.heappush(pq,(nd,nb))
        if render: render.mark_cell(cur,(200,200,100)); render.update()
    return []