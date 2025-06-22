# gui/app.py
import pygame
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gui.widgets import Button, RadioSelector, Checkbox
from gui.gui_renderer import GuiRenderer
from maze_generators import dfs, prims, wilsons, recdiv, handk, kruskals
from visualizer.pygame_renderer import PygameRenderer
from gui.helpers import convert_maze_for_gui, convert_coords_for_gui

algorithm_map = {
    "DFS Backtracker": dfs.generate_maze,
    "Prim's": prims.generate_maze,
    "Wilson's": wilsons.generate_maze,
    "Recursive Division": recdiv.generate_maze,
    "Hunt & Kill": handk.generate_maze,
    "Kruskal's": kruskals.generate_maze,
}

renderer = None
pygame.init()

WIDTH, HEIGHT = 1200, 800
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MAZESOLVER GUI")

clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 24)

# UI Elements
# --- UI Elements ---

animate_checkbox = Checkbox(x=950, y=350, label="Animate Generation")
animate = animate_checkbox.is_checked()

def generate_maze_callback():
    selected_algo = algo_selector.get_selected()
    algo_fn = algorithm_map.get(selected_algo)
    if not algo_fn:
        print("No algorithm selected!")
        return

    animate = animate_checkbox.is_checked()
    width, height = 25, 25

    render = PygameRenderer(width, height) if animate else None

    if "render" in algo_fn.__code__.co_varnames:
        maze, entry, goal = algo_fn(width, height, render=render)
    else:
        maze, entry, goal = algo_fn(width, height)

    if render:
        render.wait_for_exit()

    # Convert for GUI display
    maze = convert_maze_for_gui(maze)
    entry = convert_coords_for_gui(entry)
    goal = convert_coords_for_gui(goal)

    renderer.load_maze(maze, entry, goal)


generate_btn = Button(950, 80, 100, 40, "Generate", callback=generate_maze_callback)
solve_btn = Button(1050, 80, 100, 40, "Solve")

algo_selector = RadioSelector(
    x=950, y=150, options=[
        "DFS Backtracker", "Prim's", "Wilson's",
        "Recursive Division", "Hunt & Kill", "Kruskal's"
    ],
    default_index=0
)


def draw_ui():
    pygame.draw.rect(screen, (30, 30, 30), (900, 0, 300, HEIGHT))  # UI Panel
    title = font.render("MAZESOLVER", True, (200, 200, 255))
    screen.blit(title, (960, 20))
    generate_btn.draw(screen)
    solve_btn.draw(screen)
    algo_selector.draw(screen)
    animate_checkbox.draw(screen)


# Main loop
def run():
    global renderer
    renderer = GuiRenderer(maze_width=25, maze_height=25)

    # Now that renderer exists, define the callback:
    def generate_maze_callback():
        selected_algo = algo_selector.get_selected()
        algo_fn = algorithm_map.get(selected_algo)
        if not algo_fn:
            print("No algorithm selected!")
            return

        animate = animate_checkbox.is_checked()
        width, height = 25, 25

        render = PygameRenderer(width, height) if animate else None

        if "render" in algo_fn.__code__.co_varnames:
            maze, entry, goal = algo_fn(width, height, render=render)
        else:
            maze, entry, goal = algo_fn(width, height)

        if render:
            render.wait_for_exit()

        # Convert for GUI display
        maze = convert_maze_for_gui(maze)
        entry = convert_coords_for_gui(entry)
        goal = convert_coords_for_gui(goal)

        renderer.load_maze(maze, entry, goal)

    # UI Buttons now that callback exists
    generate_btn.callback = generate_maze_callback

    while True:
        screen.fill((0, 0, 0))
        renderer.draw_maze(screen)
        draw_ui()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            generate_btn.handle_event(event)
            solve_btn.handle_event(event)
            algo_selector.handle_event(event)
            animate_checkbox.handle_event(event)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    run()
