# maze_generators/handk.py
from models.maze import Maze

def generate_maze(width: int, height: int,
                  entry=(0, 0), goal=None,
                  render=None, animate: bool = False):
    """Hunt-and-Kill wrapper that returns a Maze object."""
    maze = Maze(width, height, entry, goal)
    maze.generate("handk", animate=animate)          # <- calls Maze._handk_generate
    if render:
        render.draw_maze(maze, entry=maze.start, goal=maze.goal)
        render.update()
    return maze, maze.start, maze.goal
