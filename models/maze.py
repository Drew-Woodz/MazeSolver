import numpy as np
import random
from typing import List, Tuple, Optional

class Maze:
    def __init__(self, width: int, height: int, entry: Tuple[int, int] = (0, 0), 
                 goal: Optional[Tuple[int, int]] = None, max_history_size: int = 10000):
        """Initialize maze with empty grid and coordinates.
        
        Args:
            width (int): Width of the maze in cells (10-100, doubled internally for grid).
            height (int): Height of the maze in cells (10-100, doubled internally for grid).
            entry (Tuple[int, int]): Starting position in cell-space (default: (0, 0)).
            goal (Tuple[int, int], optional): Goal position in cell-space (default: bottom-right).
            max_history_size (int): Maximum number of animation steps to retain (default: 10000).
        
        Note: Grid size is 2 * width + 1 x 2 * height + 1 to accommodate walls.
        Raises:
            ValueError: If dimensions or coordinates are invalid.
        """
        # Validate dimensions
        if not isinstance(width, int) or not isinstance(height, int):
            raise ValueError("Width and height must be integers.")
        if not (10 <= width <= 100 and 10 <= height <= 100):
            raise ValueError("Width and height must be between 10 and 100.")
        
        self.width = width
        self.height = height
        self.maze = np.zeros((2 * height + 1, 2 * width + 1), dtype=np.int8)
        
        # Validate and convert entry to grid-space
        if not isinstance(entry, tuple) or len(entry) != 2:
            raise ValueError("Entry must be a tuple of (x, y).")
        entry_x, entry_y = entry
        if not (0 <= entry_x < width and 0 <= entry_y < height):
            raise ValueError("Entry coordinates must be within maze bounds (0 to width-1, 0 to height-1).")
        self.start = (2 * entry_y + 1, 2 * entry_x + 1)  # Convert to grid-space
        
        # Validate and convert goal to grid-space
        if goal is not None:
            if not isinstance(goal, tuple) or len(goal) != 2:
                raise ValueError("Goal must be a tuple of (x, y).")
            goal_x, goal_y = goal
            if not (0 <= goal_x < width and 0 <= goal_y < height):
                raise ValueError("Goal coordinates must be within maze bounds (0 to width-1, 0 to height-1).")
            self.goal = (2 * goal_y + 1, 2 * goal_x + 1)
        else:
            self.goal = (2 * (height - 1) + 1, 2 * (width - 1) + 1)  # Default to bottom-right
        
        self.solutions = []  # List of (path: List[Tuple[int, int]], solver_name: str)
        self.history = []    # Animation steps, populated only if animate=True
        self.max_history_size = max_history_size  # Cap for memory management
        self.maze[self.start] = 1
        self.maze[self.goal] = 1

    def to_grid_space(self, cx: int, cy: int) -> Tuple[int, int]:
        """Convert cell-space (cx, cy) to grid-space (gy, gx)."""
        return 2 * cy + 1, 2 * cx + 1

    def to_cell_space(self, gy: int, gx: int) -> Tuple[int, int]:
        """Convert grid-space (gy, gx) to cell-space (cy, cx)."""
        return (gy - 1) // 2, (gx - 1) // 2

    def generate(self, algorithm: str, animate: bool = False) -> 'Maze':
        """Generate maze using specified algorithm, optionally storing animation steps."""
        self.history.clear()  # Reset history
        if algorithm == "dfs":
            self._dfs_generate(animate)
        elif algorithm == "handk":
            self._handk_generate(animate)
        elif algorithm == "kruskals":
            self._kruskals_generate(animate)         
        elif algorithm == "prims":
            self._prims_generate(animate)
        elif algorithm == "recdiv":
            self._recdiv_generate(animate)
        elif algorithm == "wilsons":
            self._wilsons_generate(animate)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        if len(self.history) > self.max_history_size:
            self.history = self.history[-self.max_history_size:]  # Trim to max size
        return self

    def _dfs_generate(self, animate: bool):
        """DFS generation: carve paths from start using cell-space, store in grid-space."""
        visited = set()
        # Convert start to cell-space
        start_cy, start_cx = self.to_cell_space(*self.start)
        stack = [(start_cx, start_cy)]
        visited.add((start_cx, start_cy))
        while stack:
            cx, cy = stack.pop()
            # Convert to grid-space for maze array
            grid_y, grid_x = self.to_grid_space(cx, cy)
            self.maze[grid_y, grid_x] = 1
            dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            random.shuffle(dirs)
            for dx, dy in dirs:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    # Wall between (cx, cy) and (nx, ny) in grid-space
                    wall_x = grid_x + dx
                    wall_y = grid_y + dy
                    self.maze[wall_y, wall_x] = 1
                    stack.append((nx, ny))
                    if animate:
                        cell_g = self.to_grid_space(nx, ny)
                        self.history.append((cell_g, (wall_y, wall_x)))

    def _handk_generate(self, animate: bool):
        """Hunt-and-Kill: carve paths in cell-space, update grid-space maze."""
        visited = set()
        # Start at entry cell in cell-space
        cx, cy = self.to_cell_space(*self.start)
        
        def visit(x: int, y: int):
            gy, gx = self.to_grid_space(x, y)
            self.maze[gy, gx] = 1
            visited.add((x, y))
            if animate:
                self.history.append(((gy, gx), (gy, gx)))

        def neigh(x: int, y: int):
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    yield nx, ny

        visit(cx, cy)

        while True:
            unvis = [nb for nb in neigh(cx, cy) if nb not in visited]
            if unvis:  # Kill phase
                nx, ny = random.choice(unvis)
                # Wall between (cx, cy) and (nx, ny) in grid-space using cell-space difference
                cy_g, cx_g = self.to_grid_space(cx, cy)
                wy = cy_g + (ny - cy)  # Scale cell difference to grid
                wx = cx_g + (nx - cx)
                self.maze[wy, wx] = 1
                visit(nx, ny)
                if animate:
                    self.history.append(((wy, wx), (wy, wx)))
                cx, cy = nx, ny
            else:  # Hunt phase
                found = False
                for y in range(self.height):
                    for x in range(self.width):
                        if (x, y) in visited:
                            continue
                        if any(nb in visited for nb in neigh(x, y)):
                            # Carve wall to the first visited neighbor
                            nx, ny = next(nb for nb in neigh(x, y) if nb in visited)
                            y_g, x_g = self.to_grid_space(x, y)
                            wy = y_g + (ny - y)  # Scale cell difference to grid
                            wx = x_g + (nx - x)
                            self.maze[wy, wx] = 1
                            visit(x, y)
                            if animate:
                                self.history.append(((wy, wx), (wy, wx)))
                            cx, cy = x, y
                            found = True
                            break
                    if found:
                        break
                if not found:
                    break

    def _prims_generate(self, animate: bool):
        """Prim's: grow maze from start in cell-space, carve paths in grid-space."""
        visited = set()
        frontier = []

        # Start at entry cell in cell-space
        cx, cy = self.to_cell_space(*self.start)
        visited.add((cx, cy))
        gy, gx = self.to_grid_space(cx, cy)
        self.maze[gy, gx] = 1

        def add_frontier(cx, cy):
            """Add unvisited neighbors in cell-space to frontier with their parent."""
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in visited:
                    frontier.append((nx, ny, cx, cy))  # neighbor + parent

        add_frontier(cx, cy)
        if animate:
            self.history.append(((gy, gx), (gy, gx)))

        while frontier:
            idx = random.randrange(len(frontier))
            nx, ny, px, py = frontier.pop(idx)  # neighbor and parent in cell-space
            if (nx, ny) in visited:
                continue
            visited.add((nx, ny))
            # Carve wall and cell in grid-space
            py_g, px_g = self.to_grid_space(px, py)
            ny_g, nx_g = self.to_grid_space(nx, ny)
            # Wall is between parent (px,py) and neighbor (nx,ny)
            wy = py_g + (ny - py)  # Adjust based on cell-space difference
            wx = px_g + (nx - px)
            self.maze[wy, wx] = 1
            gy, gx = ny_g, nx_g
            self.maze[gy, gx] = 1
            if animate:
                self.history.append(((wy, wx), (gy, gx)))
            add_frontier(nx, ny)

    def _wilsons_generate(self, animate: bool):
        """Wilson's: random walks in cell-space, carve paths in grid-space."""
        # Convert start to cell-space
        root = self.to_cell_space(*self.start)
        in_tree = {root}
        ry, rx = self.to_grid_space(*root)
        self.maze[ry, rx] = 1
        if animate:
            self.history.append(((ry, rx), (ry, rx)))

        all_cells = [(x, y) for x in range(self.width) for y in range(self.height)]
        while len(in_tree) < len(all_cells):
            walk = []
            cx, cy = random.choice([c for c in all_cells if c not in in_tree])
            while (cx, cy) not in in_tree:
                walk.append((cx, cy))
                dx, dy = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    cx, cy = nx, ny
                    if (cx, cy) in walk:
                        walk = walk[:walk.index((cx, cy))+1]
            prev = (cx, cy)
            for px, py in reversed(walk):
                gy, gx = self.to_grid_space(px, py)
                self.maze[gy, gx] = 1
                py_g, px_g = self.to_grid_space(*prev)
                # Wall is midpoint between current and previous cell in grid-space
                wy, wx = (gy + py_g) // 2, (gx + px_g) // 2
                self.maze[wy, wx] = 1
                if animate:
                    self.history.append(((wy, wx), (gy, gx)))
                in_tree.add((px, py))
                prev = (px, py)

    def _recdiv_generate(self, animate: bool):
        """Recursive Division: divide grid-space, create walls with passages."""
        def pick_odd(start, length):
            """Return all odd indices in [start + 1 … start + length - 1]."""
            return [i for i in range(start + 1, start + length, 2)]

        def divide(x, y, w, h, border_steps, step_idx):
            """Recursively divide space, interleave with border animation."""
            if w < 3 or h < 3:
                return step_idx
            horizontal = h > w if w != h else random.choice([True, False])

            if horizontal:
                wy = random.choice(pick_odd(y, h - 1))
                passage_x = random.choice(pick_odd(x - 1, w + 1))
                for gx in range(x, x + w):
                    if gx == passage_x:
                        continue
                    self.maze[wy, gx] = 0
                    if animate:
                        self.history.append(((wy, gx), (wy, gx)))  # Record wall square
                step_idx = divide(x, y, w, wy - y, border_steps, step_idx)
                step_idx = divide(x, wy + 1, w, y + h - wy - 1, border_steps, step_idx)
            else:
                wx = random.choice(pick_odd(x, w - 1))
                passage_y = random.choice(pick_odd(y - 1, h + 1))
                for gy in range(y, y + h):
                    if gy == passage_y:
                        continue
                    self.maze[gy, wx] = 0
                    if animate:
                        self.history.append(((gy, wx), (gy, wx)))  # Record wall square
                step_idx = divide(x, y, wx - x, h, border_steps, step_idx)
                step_idx = divide(wx + 1, y, x + w - wx - 1, h, border_steps, step_idx)
            return step_idx

        # Initialize grid as all paths (1), unlike other algorithms starting with walls
        self.maze[1:-1, 1:-1] = 1
        if animate:
            w, h = self.maze.shape[1], self.maze.shape[0]
            border_steps = [
                ((0, gx), (0, gx)) for gx in range(w)  # Top
            ] + [
                ((h-1, gx), (h-1, gx)) for gx in range(w)  # Bottom
            ] + [
                ((gy, 0), (gy, 0)) for gy in range(1, h-1)  # Left
            ] + [
                ((gy, w-1), (gy, w-1)) for gy in range(1, h-1)  # Right
            ]
            step_idx = 0
            total_steps = len(border_steps)
            # Interleave border and maze steps
            divide(1, 1, 2 * self.width - 1, 2 * self.height - 1, border_steps, 0)
            while step_idx < total_steps:
                if step_idx < total_steps:
                    self.history.append(border_steps[step_idx])
                    self.maze[border_steps[step_idx][0][0], border_steps[step_idx][0][1]] = 0
                    step_idx += 1

    def _kruskals_generate(self, animate: bool):
        """Kruskal's: connect cells in cell-space, carve paths in grid-space."""
        class DisjointSet:
            def __init__(self):   self.p = {}
            def find(self, x):
                if self.p[x] != x: self.p[x] = self.find(self.p[x])
                return self.p[x]
            def union(self, a, b):
                ra, rb = self.find(a), self.find(b)
                if ra != rb:
                    self.p[rb] = ra
                    return True
                return False

        ds = DisjointSet()
        cells = [(x, y) for x in range(self.width) for y in range(self.height)]
        for c in cells: ds.p[c] = c

        # Every interior cell becomes a white square first (paths)
        for cx, cy in cells:
            gy, gx = self.to_grid_space(cx, cy)
            self.maze[gy, gx] = 1
            if animate:
                self.history.append(((gy, gx), (gy, gx)))  # Record carved cell

        # Candidate edges = walls between neighbouring cells
        edges = []
        for x, y in cells:
            if x < self.width-1: edges.append(((x, y), (x+1, y)))  # East wall
            if y < self.height-1: edges.append(((x, y), (x, y+1)))  # South wall
        random.shuffle(edges)

        for (ax, ay), (bx, by) in edges:
            if ds.union((ax, ay), (bx, by)):  # Wall can be removed
                ay_g, ax_g = self.to_grid_space(ax, ay)
                by_g, bx_g = self.to_grid_space(bx, by)
                # Wall is between cells, use the grid-space wall position
                wy = (ay_g + by_g) // 2 if ay != by else ay_g
                wx = (ax_g + bx_g) // 2 if ax != bx else ax_g
                self.maze[wy, wx] = 1  # Remove wall to create path
                if animate:
                    self.history.append(((wy, wx), (wy, wx)))

    def add_solution(self, path: List[Tuple[int, int]], solver_name: str):
        """Add a solution path with its solver name."""
        self.solutions.append((path, solver_name))

    def to_json(self) -> dict:
        """Serialize maze data for saving."""
        return {
            "maze": self.maze.tolist(),
            "start": self.start,
            "goal": self.goal,
            "solutions": self.solutions,
            "history": self.history  # Include history for animation replay
        }

    def save_to_png(self, filename: str):
        """Save maze to PNG using Pygame (placeholder implementation)."""
        import pygame
        pygame.init()
        size = self.maze.shape
        surface = pygame.Surface(size)
        for y in range(size[0]):
            for x in range(size[1]):
                color = (255, 255, 255) if self.maze[y, x] else (0, 0, 0)
                surface.set_at((x, y), color)
        pygame.image.save(surface, filename)
        pygame.quit()

    def print_setup(self):
        pass

    def clear_history(self):
        """Manually clear animation history to free memory when no longer needed."""
        self.history.clear()

    def clear_solutions(self):
        """Manually clear solution paths to free memory when no longer needed."""
        self.solutions.clear()

    def get_animation_steps(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Return history for animation (empty if not generated with animate=True)."""
        return self.history