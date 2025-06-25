# maze_generators/dfs.py
from models.maze import Maze

def generate_maze(width: int, height: int, entry=(0, 0), goal=None, render=None):
    maze = Maze(width, height, entry, goal)
    maze.generate("dfs", animate=render is not None)
    if render:
        render.draw_maze(maze, entry=maze.start, goal=maze.goal)
        render.update()
        if maze.history:  # Animate if steps exist
            for cell, wall in maze.get_animation_steps():
                render.draw_maze(maze, entry=maze.start, goal=maze.goal)
                render.update(delay=0.1)  # Add delay for visibility
    return maze, maze.start, maze.goal