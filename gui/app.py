# gui/app.py
import pygame
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gui.widgets import Button, RadioSelector, Checkbox, TextBox
from gui.gui_renderer import GuiRenderer
from maze_generators import dfs, prims, wilsons, recdiv, handk, kruskals
from visualizer.pygame_renderer import PygameRenderer  # Optional
from gui.helpers import convert_maze_for_gui, convert_coords_for_gui

# Mapping algorithm names to generator functions
algorithm_map = {
    "DFS Backtracker": dfs.generate_maze,
    "Prim's": prims.generate_maze,
    "Wilson's": wilsons.generate_maze,
    "Recursive Division": recdiv.generate_maze,
    "Hunt & Kill": handk.generate_maze,
    "Kruskal's": kruskals.generate_maze,
}

# --- Initialize pygame and GUI environment ---
pygame.init()
WIDTH, HEIGHT = 1200, 800
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MAZESOLVER GUI")

clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 24)

# --- Renderer Setup ---
def init_renderer(maze_width, maze_height):
    return GuiRenderer(maze_width=maze_width, maze_height=maze_height, surface=screen)

renderer = init_renderer(25, 25)

# --- UI Elements ---
generate_btn = Button(950, 80, 100, 40, "Generate", callback=lambda: generate_maze_callback())
solve_btn = Button(1050, 80, 100, 40, "Solve")

algo_selector = RadioSelector(
    x=950, y=150,
    options=[
        "DFS Backtracker", "Prim's", "Wilson's",
        "Recursive Division", "Hunt & Kill", "Kruskal's"
    ],
    default_index=0
)

animate_checkbox = Checkbox(x=950, y=350, label="Animate Generation")
width_box = TextBox(x=950, y=420, label="Width:")
height_box = TextBox(x=1030, y=420, label="Height:")

# --- Generate Maze Logic ---
def generate_maze_callback():
    global renderer

    selected_algo = algo_selector.get_selected()
    algo_fn = algorithm_map.get(selected_algo)
    if not algo_fn:
        print("No algorithm selected!")
        return

    animate = animate_checkbox.is_checked()

    width = width_box.get_value()
    height = height_box.get_value()
    if width is None or height is None:
        print("Invalid maze dimensions")
        return

    # Recalculate display size and reinitialize renderer
    canvas_width = width * 20  # rough estimate of cell size before calculation
    canvas_height = height * 20
    global screen
    screen = pygame.display.set_mode((canvas_width + 300, max(canvas_height, 800)))
    renderer = GuiRenderer(maze_width=width, maze_height=height, surface=screen)

    render = renderer if animate else None

    if "render" in algo_fn.__code__.co_varnames:
        maze, entry, goal = algo_fn(width, height, render=render)
        if render:
            render.wait_for_exit()
    else:
        maze, entry, goal = algo_fn(width, height)

    maze = convert_maze_for_gui(maze)
    entry = convert_coords_for_gui(entry)
    goal = convert_coords_for_gui(goal)

    renderer.load_maze(maze, entry, goal)

# --- Draw Static UI Elements ---
def draw_ui():
    sidebar_x = screen.get_width() - 300
    pygame.draw.rect(screen, (30, 30, 30), (sidebar_x, 0, 300, screen.get_height()))

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
        screen.fill((0, 0, 0))
        renderer.draw_maze_gui()
        draw_ui()

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
