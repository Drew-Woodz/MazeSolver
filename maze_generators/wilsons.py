# maze_generators/wilsons.py
from models.maze import Maze

def generate_maze(width, height, entry=(0,0), goal=None,
                  render=None, animate=False):
    """Return a Maze filled with Wilson’s algorithm paths."""
    maze = Maze(width, height, entry, goal)
    maze.generate("wilsons", animate=animate)
    if render:
        render.draw_maze(maze, entry=maze.start, goal=maze.goal)
        render.update()
    return maze, maze.start, maze.goal