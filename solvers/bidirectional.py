from collections import deque
from typing import Tuple, List, Optional
import numpy as np

def reconstruct_bidirectional_path(meet, came_from_start, came_from_goal):
    path_start = []
    node = meet
    while node in came_from_start:
        path_start.append(node)
        node = came_from_start[node]
    path_start.reverse()

    path_goal = []
    node = meet
    while node in came_from_goal:
        node = came_from_goal[node]
        path_goal.append(node)

    return path_start + [meet] + path_goal

def solve(maze: np.ndarray,
          start: Tuple[int, int],
          goal: Tuple[int, int],
          render=None,
          color: Optional[Tuple[int, int, int]] = (0, 255, 0)) -> List[Tuple[int, int]]:

    def in_bounds(pos):
        y, x = pos
        return 0 <= y < maze.shape[0] and 0 <= x < maze.shape[1]

    frontier_start = deque([start])
    frontier_goal = deque([goal])

    came_from_start = {}
    came_from_goal = {}
    visited_start = set([start])
    visited_goal = set([goal])

    while frontier_start and frontier_goal:
        if render and not render.running:
            return []

        def expand(frontier, visited, came_from, other_visited):
            current = frontier.popleft()
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                neighbor = (current[0] + dy, current[1] + dx)
                if in_bounds(neighbor) and maze[neighbor] == 1 and neighbor not in visited:
                    came_from[neighbor] = current
                    visited.add(neighbor)
                    frontier.append(neighbor)
                    if render and render.running:
                        render.mark_cell(neighbor, color=(200, 200, 100))
                        render.update()
                    if neighbor in other_visited:
                        return neighbor
            return None

        meet = expand(frontier_start, visited_start, came_from_start, visited_goal)
        if meet:
            path = reconstruct_bidirectional_path(meet, came_from_start, came_from_goal)
            if render and render.running:
                for pos in path:
                    render.mark_cell(pos, color=color)
                    render.update()
            return path

        meet = expand(frontier_goal, visited_goal, came_from_goal, visited_start)
        if meet:
            path = reconstruct_bidirectional_path(meet, came_from_start, came_from_goal)
            if render and render.running:
                for pos in path:
                    render.mark_cell(pos, color=color)
                    render.update()
            return path

    return []
