# gui/app.py

import pygame
import sys
import os
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gui.widgets import Button, RadioSelector, Checkbox, TextBox
from gui.gui_renderer import GuiRenderer
from models.maze import Maze

# --- Constants ---
MAZE_WIDTH_PX = 900
MAZE_HEIGHT_PX = 800
UI_WIDTH_PX = 300
FPS = 60

# Mapping algorithm names to internal keys
algo_key_map = {
    "DFS Backtracker": "dfs",
    "Prim's": "prims",
    "Wilson's": "wilsons",
    "Recursive Division": "recdiv",
    "Hunt & Kill": "handk",
    "Kruskal's": "kruskals"
}

# --- Initialize pygame and GUI environment ---
pygame.init()
screen = pygame.display.set_mode((MAZE_WIDTH_PX + UI_WIDTH_PX, MAZE_HEIGHT_PX))
pygame.display.set_caption("MAZESOLVER GUI")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 24)

# --- Renderer Setup ---
def init_renderer(maze_width, maze_height):
    return GuiRenderer(maze_width=maze_width, maze_height=maze_height, surface=screen, UI_WIDTH_PX=UI_WIDTH_PX)

renderer = init_renderer(25, 25)
current_maze = None

# --- UI Elements (Moved outside callback to persist) ---
generate_btn = Button(950, 80, 100, 40, "Generate", callback=lambda: generate_maze_callback())
solve_btn = Button(1050, 80, 100, 40, "Solve")
algo_selector = RadioSelector(x=950, y=150, options=list(algo_key_map.keys()), default_index=0)
animate_checkbox = Checkbox(x=950, y=350, label="Animate Generation")
width_box = TextBox(x=950, y=420, label="Width:")
height_box = TextBox(x=1030, y=420, label="Height:")

class LightweightMaze:
    def __init__(self, grid, start=None, goal=None):
        self.maze = grid
        self.start = start
        self.goal = goal

def animate_generation(renderer, maze, delay=0.01):
    for i, frame in enumerate(maze.history):
        print(f"[DEBUG] Frame {i} type: {type(frame)}, shape: {getattr(frame, 'shape', None)}")
        renderer.draw_maze(LightweightMaze(frame))
        renderer.update(delay)


# --- Generate Maze Logic ---
def generate_maze_callback():
    global generate_btn, solve_btn, algo_selector, animate_checkbox, width_box, height_box, renderer

    selected_algo = algo_selector.get_selected()
    animate = animate_checkbox.is_checked()

    if not (width_box.is_valid() and height_box.is_valid()):
        print("Invalid dimensions! Width and Height must be integers between 10 and 100.")
        return

    width_val = width_box.get_value()
    height_val = height_box.get_value()

    if width_val is None or height_val is None:
        print("Invalid dimensions detected.")
        return

    width = max(10, min(width_val, 100))
    height = max(10, min(height_val, 100))

    print(f"[DEBUG] Maze size requested: {width} x {height}")

    # Resize canvas based on aspect ratio
    min_dim = 600
    max_dim = 1200
    new_width = min(max(min_dim, width * 20), max_dim)  # 20px per cell
    new_height = min(max(min_dim, height * 20), max_dim)
    if width > height:
        new_height = min(max_dim, int(new_width * height / width))
    else:
        new_width = min(max_dim, int(new_height * width / height))

    screen = pygame.display.set_mode((new_width + UI_WIDTH_PX, new_height))
    # Recreate UI elements with adjusted coordinates based on new width
    sidebar_x = screen.get_width() - UI_WIDTH_PX
    generate_btn = Button(sidebar_x + 50, 80, 100, 40, "Generate", callback=lambda: generate_maze_callback())
    solve_btn = Button(sidebar_x + 150, 80, 100, 40, "Solve")
    algo_selector = RadioSelector(x=sidebar_x + 50, y=150, options=list(algo_key_map.keys()), default_index=0)
    animate_checkbox = Checkbox(x=sidebar_x + 50, y=350, label="Animate Generation")
    width_box = TextBox(x=sidebar_x + 50, y=420, label="Width:")
    height_box = TextBox(x=sidebar_x + 130, y=420, label="Height:")

    renderer = GuiRenderer(maze_width=width, maze_height=height, surface=screen, UI_WIDTH_PX=UI_WIDTH_PX)
    renderer._update_dimensions()  # Ensure dimensions are recalculated

    maze = Maze(width, height)
    maze.generate(algo_key_map[selected_algo], animate=animate)
    print(f"[DEBUG] Maze generated, shape: {maze.maze.shape}")
    print(f"[DEBUG] Maze data sample: {maze.maze[0, :10]}")  # Check maze content
    if animate:
        print("[DEBUG] Starting animation with", len(maze.history), "frames")
        animate_generation(renderer, maze)
    else:
        renderer.load_maze(maze)  # Immediate display if not animating

    current_maze = maze
    renderer.load_maze(maze)  # Finalize entry/goal, grid resizing


# --- Draw Static UI Elements ---
def draw_ui():
    sidebar_x = screen.get_width() - UI_WIDTH_PX
    pygame.draw.rect(screen, (30, 30, 30), (sidebar_x, 0, UI_WIDTH_PX, screen.get_height()))

    title = font.render("MAZESOLVER", True, (200, 200, 255))
    screen.blit(title, (sidebar_x + 60, 20))

    generate_btn.draw(screen)
    solve_btn.draw(screen)
    algo_selector.draw(screen)
    animate_checkbox.draw(screen)
    width_box.draw(screen)
    height_box.draw(screen)

# --- Main Loop ---
def run():
    while True:
        screen.fill((0, 0, 0))  # Clear the entire screen to black
        renderer.draw_maze_gui()
        draw_ui()
        pygame.display.update()  # Update entire screen once per frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            generate_btn.handle_event(event)
            solve_btn.handle_event(event)
            algo_selector.handle_event(event)
            animate_checkbox.handle_event(event)
            width_box.handle_event(event)
            height_box.handle_event(event)

        pygame.display.flip()
        clock.tick(FPS)

# --- Entry Point ---
if __name__ == "__main__":
    run()