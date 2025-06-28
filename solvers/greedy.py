# solvers/greedy.py
import heapq
from typing import Tuple, List, Optional
from models.maze import Maze

def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def _reconstruct(parent, cur):
    path=[cur]
    while cur in parent:
        cur=parent[cur]; path.append(cur)
    return path[::-1]

def solve(maze: Maze, start: Tuple[int,int], goal: Tuple[int,int],
          render=None, color: Optional[Tuple[int,int,int]]=(255,165,0)) -> List[Tuple[int,int]]:
    grid = maze.maze
    h,w = grid.shape
    def inside(p): return 0<=p[0]<h and 0<=p[1]<w
    if not (inside(start) and inside(goal)) or grid[start]==0 or grid[goal]==0:
        raise ValueError("Start/goal invalid")

    pq=[(heuristic(start, goal), start)]
    parent=set(); came={}
    seen=set()
    while pq:
        if render and not render.running: return []
        _, cur = heapq.heappop(pq)
        if cur in seen: continue
        seen.add(cur)
        if cur==goal:
            path=_reconstruct(came,cur)
            maze.add_solution(path,"Greedy BFS")
            if render:
                for p in path: render.mark_cell(p,color); render.update()
            return path
        for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
            nb=(cur[0]+dy, cur[1]+dx)
            if inside(nb) and grid[nb]==1 and nb not in seen:
                came[nb]=cur; heapq.heappush(pq,(heuristic(nb,goal),nb))
        if render: render.mark_cell(cur,(255,200,0)); render.update()
    return []