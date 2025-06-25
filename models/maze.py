# models/maze.py
import numpy as np
import random as random
from typing import List, Tuple, Optional

class Maze:
    def __init__(self, width: int, height: int, entry: Tuple[int, int] = (0, 0), 
                 goal: Optional[Tuple[int, int]] = None):
        """Initialize maze with empty grid and coordinates."""
        self.width = width
        self.height = height
        self.maze = np.zeros((2 * height + 1, 2 * width + 1), dtype=np.int8)
        self.start = (2 * entry[1] + 1, 2 * entry[0] + 1)  # Convert to maze coords
        self.goal = (2 * (goal[1] if goal else width - 1) + 1, 
                     2 * (goal[0] if goal else height - 1) + 1)
        self.solutions = []  # List of (path: List[Tuple[int, int]], solver_name: str)
        self.history = []    # Animation steps, populated only if animate=True
        self.maze[self.start] = 1
        self.maze[self.goal] = 1

    def generate(self, algorithm: str, animate: bool = False) -> 'Maze':
        """Generate maze using specified algorithm, optionally storing animation steps."""
        self.history.clear()  # Reset history
        if algorithm == "dfs":
            self._dfs_generate(animate)
        elif algorithm == "handk":
            self._handk_generate(animate)
        elif algorithm == "kruskals":
            raise ValueError(f"TODO: kruskals_generate: {algorithm}")
            # self._kruskals_generate(animate)         
        elif algorithm == "prims":
            raise ValueError(f"TODO: prims_generate: {algorithm}")
            # self._prims_generate(animate)
        elif algorithm == "recdiv":
            raise ValueError(f"TODO: recdiv_generate: {algorithm}")
            # self._recdiv_generate(animate)
        elif algorithm == "wilsons":
            raise ValueError(f"TODO: wilsons_generate: {algorithm}")
            # self._wilsons_generate(animate)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        return self

    def _dfs_generate(self, animate: bool):
        """DFS generation logic (to be moved from dfs.py)."""
        visited = set()
        stack = [(self.width // 2, self.height // 2)]  # Start near center
        visited.add(stack[0])
        while stack:
            cx, cy = stack.pop()
            self.maze[2 * cy + 1, 2 * cx + 1] = 1
            dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            random.shuffle(dirs)
            for dx, dy in dirs:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    wall_x = 2 * cx + 1 + dx
                    wall_y = 2 * cy + 1 + dy
                    self.maze[wall_y, wall_x] = 1
                    stack.append((nx, ny))
                    if animate:
                        self.history.append(((nx, ny), (wall_x, wall_y)))

    # Add _handk_generate, _kruskals_generate, etc., similarly (pseudocode for now)
    def _handk_generate(self, animate: bool):
        # Implement Hunt-and-Kill logic, store steps if animate
        pass

    def add_solution(self, path: List[Tuple[int, int]], solver_name: str):
        """Add a solution path with its solver name."""
        self.solutions.append((path, solver_name))

    def to_json(self) -> dict:
        """Serialize maze data for saving."""
        return {
            "maze": self.maze.tolist(),
            "start": self.start,
            "goal": self.goal,
            "solutions": self.solutions
        }

    def get_animation_steps(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Return history for animation (empty if not generated with animate=True)."""
        return self.history

    # Future methods (pseudocode/notes)
    def save_to_png(self, filename: str):
        # Use Pygame or PIL to render maze to PNG
        # Future: Integrate with gui_renderer or pygame_renderer
        pass

    def print_setup(self):
        # Initiate local print dialog for maze image
        # Future: Use OS-specific print API
        pass

    def clear_history(self):
        # Clear animation steps to save memory
        self.history = []