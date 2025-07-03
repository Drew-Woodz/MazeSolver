import pygame

class GuiRenderer:
    def __init__(self, maze_width, maze_height, surface, UI_WIDTH_PX):
        self.maze_width = maze_width  # Original cell-based width
        self.maze_height = maze_height  # Original cell-based height
        self.surface = surface
        self.UI_WIDTH_PX = UI_WIDTH_PX
        self.maze = None  # Explicitly initialize here
        self.entry = None
        self.goal = None
        self.running = True
        self._update_dimensions()  # Call after maze is potentially set or handle None

    def _update_dimensions(self):
        self.surface_rect = pygame.Rect(0, 0, self.surface.get_width() - self.UI_WIDTH_PX, self.surface.get_height())
        if self.maze and hasattr(self.maze, 'maze'):
            grid_height, grid_width = self.maze.maze.shape
            self.cell_size = min(
                self.surface_rect.width / grid_width,
                self.surface_rect.height / grid_height
            )
        else:
            # Fallback for initial setup before maze is loaded
            grid_width = 2 * self.maze_width + 1
            grid_height = 2 * self.maze_height + 1
            self.cell_size = min(
                self.surface_rect.width / grid_width,
                self.surface_rect.height / grid_height
            )
        print(f"[DEBUG] _update_dimensions - Cell size: {self.cell_size}, Surface rect: {self.surface_rect}, Maze: {self.maze is not None}")

    def set_maze(self, maze_obj):
        self.load_maze(maze_obj)

    def wait_for_exit(self):
        pass

    def clear(self):
        pygame.draw.rect(self.surface, (255, 255, 255), self.surface_rect)

    def load_maze(self, maze_obj):
        self.maze = maze_obj
        self.entry = maze_obj.start
        self.goal = maze_obj.goal
        print(f"[DEBUG] load_maze - Maze set: {self.maze is not None}, Shape: {self.maze.maze.shape if self.maze else 'None'}")
        self._update_dimensions()  # Recalculate after loading maze

    def draw_cell(self, x, y, color):
        if self.maze and hasattr(self.maze, 'maze') and 0 <= x < self.maze.maze.shape[1] and 0 <= y < self.maze.maze.shape[0]:
            cell_x = self.surface_rect.left + x * self.cell_size
            cell_y = self.surface_rect.top + y * self.cell_size
            rect = pygame.Rect(cell_x, cell_y, self.cell_size, self.cell_size)
            if self.surface_rect.colliderect(rect):
                pygame.draw.rect(self.surface, color, rect)

    def draw_maze_gui(self):
        if self.maze is None or not hasattr(self.maze, 'maze'):
            # print("[DEBUG] No maze loaded or maze attribute missing")
            return
        # print("[DEBUG] Drawing maze, shape: ", self.maze.maze.shape)  # Confirm this prints
        grid = self.maze.maze
        for y in range(grid.shape[0]):
            for x in range(grid.shape[1]):
                color = (0, 0, 0) if grid[y, x] == 0 else (255, 255, 255)
                self.draw_cell(x, y, color)
        if self.entry:
            self.draw_cell(self.entry[0], self.entry[1], (0, 255, 0))
        if self.goal:
            self.draw_cell(self.goal[0], self.goal[1], (255, 0, 0))

        # Update the entire canvas once
        pygame.display.update(self.surface_rect)

    def draw_maze(self, maze_obj, entry=None, goal=None):
        if not hasattr(maze_obj, 'maze'):
            return
        grid = maze_obj.maze
        for y in range(grid.shape[0]):
            for x in range(grid.shape[1]):
                color = (0, 0, 0) if grid[y, x] == 0 else (255, 255, 255)
                self.draw_cell(x, y, color)

        if entry:
            self.draw_cell(entry[0], entry[1], (0, 255, 0))
        if goal:
            self.draw_cell(goal[0], goal[1], (255, 0, 0))

    def mark_cell(self, cell, color=(255, 0, 0)):
        y, x = cell
        if self.maze and hasattr(self.maze, 'maze') and 0 <= x < self.maze.maze.shape[1] and 0 <= y < self.maze.maze.shape[0]:
            center = (
                self.surface_rect.left + x * self.cell_size + self.cell_size // 2,
                self.surface_rect.top + y * self.cell_size + self.cell_size // 2
            )
            radius = max(2, self.cell_size // 4)
            pygame.draw.circle(self.surface, color, center, radius)

    def update(self, delay=0.01):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        pygame.display.flip()
        if delay:
            pygame.time.delay(int(delay * 1000))