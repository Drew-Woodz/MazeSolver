# main.py

from visualizer.pygame_renderer import PygameRenderer
from maze_generators.dfs_backtracker import generate_maze

if __name__ == "__main__":
    renderer = PygameRenderer(25, 25)
    generate_maze(25, 25, render=renderer)
    