# maze_generators/dfs.py
from models.maze import Maze

def generate_maze(width: int, height: int, entry=(0, 0), goal=None, render=None, animate=False):
    maze = Maze(width, height, entry, goal)
    maze.generate("dfs", animate=animate)  # Use the animate parameter
    if render:
        render.draw_maze(maze, entry=maze.start, goal=maze.goal)
        render.update()
        if maze.history:
            print(f"Generated with {len(maze.history)} steps")  # Debug
    return maze, maze.start, maze.goal