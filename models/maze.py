# models/maze.py
import numpy as np
import random
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
            self._prims_generate(animate)
        elif algorithm == "recdiv":
            self._recdiv_generate(animate)
        elif algorithm == "wilsons":
            self._wilsons_generate(animate)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        return self

    def _dfs_generate(self, animate: bool):
        """DFS generation logic starting at entry point."""
        visited = set()
        # Start at entry cell (converted to cell-space indices)
        start_cx = (self.start[1] - 1) // 2
        start_cy = (self.start[0] - 1) // 2
        stack = [(start_cx, start_cy)]
        visited.add((start_cx, start_cy))
        while stack:
            cx, cy = stack.pop()
            # Convert to grid-space for maze array
            grid_x = 2 * cx + 1
            grid_y = 2 * cy + 1
            self.maze[grid_y, grid_x] = 1
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
                        cell_g = (2 * ny + 1, 2 * nx + 1)  # Grid-space cell
                        self.history.append((cell_g, (wall_y, wall_x)))  # Grid-space wall

    def _handk_generate(self, animate: bool):
        visited = set()
        cx, cy = 0, 0  # start at entry cell

        def visit(x, y):
            gx, gy = 2*y + 1, 2*x + 1
            self.maze[gx, gy] = 1
            visited.add((x, y))
            if animate:
                self.history.append(((gx, gy), (gx, gy)))  # paint cell

        def neigh(x, y):
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x+dx, y+dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    yield nx, ny

        visit(cx, cy)
        while True:
            unvis = [(nx, ny) for nx, ny in neigh(cx, cy) if (nx, ny) not in visited]
            if unvis:
                nx, ny = random.choice(unvis)
                wx, wy = 2*cy+1 + (ny-cy), 2*cx+1 + (nx-cx)  # wall grid
                self.maze[wx, wy] = 1
                visit(nx, ny)
                if animate:
                    self.history.append(((wx, wy), (wx, wy)))
                cx, cy = nx, ny
            else:  # Hunt phase
                hunt_found = False
                for y in range(self.height):
                    for x in range(self.width):
                        if (x, y) not in visited and any((u,v) in visited for u,v in neigh(x, y)):
                            # carve first adjacent visited neighbor wall
                            nx, ny = next((u,v) for u,v in neigh(x,y) if (u,v) in visited)
                            wx, wy = 2*y+1 + (ny-y), 2*x+1 + (nx-x)
                            self.maze[wx, wy] = 1
                            visit(x, y)
                            if animate:
                                self.history.append(((wx, wy), (wx, wy)))
                            cx, cy = x, y
                            hunt_found = True
                            break
                    if hunt_found:
                        break
                if not hunt_found:
                    break

    def _prims_generate(self, animate: bool):
        visited = set()
        frontier = []

        def cell_to_grid(cx, cy):
            return 2*cy+1, 2*cx+1  # grid‑space (gy, gx)

        def add_frontier(cx, cy):
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = cx+dx, cy+dy
                if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in visited:
                    frontier.append((nx, ny, cx, cy))  # neighbour + parent

        # start at entry cell
        cx, cy = (self.start[1]-1)//2, (self.start[0]-1)//2
        visited.add((cx, cy))
        gy, gx = cell_to_grid(cx, cy)
        self.maze[gy, gx] = 1
        add_frontier(cx, cy)

        if animate:
            self.history.append(((gy, gx), (gy, gx)))

        while frontier:
            idx = random.randrange(len(frontier))
            nx, ny, px, py = frontier.pop(idx)
            if (nx, ny) in visited:
                continue
            visited.add((nx, ny))
            # open wall between parent (px,py) and neighbour (nx,ny)
            wy, wx = cell_to_grid(px, py)
            wy += ny - py
            wx += nx - px
            self.maze[wy, wx] = 1
            gy, gx = cell_to_grid(nx, ny)
            self.maze[gy, gx] = 1
            if animate:
                self.history.append(((wy, wx), (gy, gx)))
            add_frontier(nx, ny)

    def _wilsons_generate(self, animate: bool):
        import random                      # local import for clarity

        def cell2grid(cx, cy):             # → (gy, gx)
            return 2 * cy + 1, 2 * cx + 1

        # Seed with the *entry* cell so start is guaranteed connected
        root = ((self.start[1]-1)//2, (self.start[0]-1)//2)
        in_tree = {root}
        ry, rx = cell2grid(*root)
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
                    if (cx, cy) in walk:              # loop‑erasure
                        walk = walk[:walk.index((cx, cy))+1]
            # carve path back to tree (walk reversed for easy linkage)
            prev = (cx, cy)                           # this is in_tree
            for px, py in reversed(walk):
                gy, gx = cell2grid(px, py)
                self.maze[gy, gx] = 1
                py_g, px_g = cell2grid(*prev)
                wy, wx = (gy + py_g)//2, (gx + px_g)//2
                self.maze[wy, wx] = 1                # open wall
                if animate:
                    self.history.append(((wy, wx), (gy, gx)))
                in_tree.add((px, py))
                prev = (px, py)

    def _recdiv_generate(self, animate: bool):
        def pick_odd(start, length):
            """Return list of odd indices between start and start+length-1 (inclusive)."""
            return [i for i in range(start+1, start+length, 2)]

        def divide(x, y, w, h):
            if w < 3 or h < 3:           # need at least one cell and walls around it
                return
            # decide orientation
            horizontal = h > w if w != h else random.choice([True, False])

            if horizontal:               # horizontal wall
                possible_walls = pick_odd(y, h-1)
                if not possible_walls:
                    return
                wy = random.choice(possible_walls)
                passage_x = random.choice(pick_odd(x-1, w+1))  # ensure passage on path grid
                for gx in range(x, x+w):
                    if gx == passage_x:
                        continue
                    self.maze[wy, gx] = 0
                    if animate:
                        self.history.append(((wy, gx), (wy, gx)))
                # recurse: top then bottom
                divide(x, y, w, wy - y)
                divide(x, wy+1, w, y+h-wy-1)
            else:                        # vertical wall
                possible_walls = pick_odd(x, w-1)
                if not possible_walls:
                    return
                wx = random.choice(possible_walls)
                passage_y = random.choice(pick_odd(y-1, h+1))
                for gy in range(y, y+h):
                    if gy == passage_y:
                        continue
                    self.maze[gy, wx] = 0
                    if animate:
                        self.history.append(((gy, wx), (gy, wx)))
                # recurse: left then right
                divide(x, y, wx - x, h)
                divide(wx+1, y, x+w-wx-1, h)

        # Start: all paths inside, walls (0) on border remain
        self.maze[1:-1, 1:-1] = 1
        divide(1, 1, 2*self.width-1, 2*self.height-1)

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