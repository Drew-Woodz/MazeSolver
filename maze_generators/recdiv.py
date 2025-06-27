# maze_generators/recdiv.py
from models.maze import Maze


def generate_maze(width: int, height: int,
                  entry=(0, 0), goal=None,
                  render=None, animate: bool = False):
    """Recursive Division generator that returns a Maze object."""
    maze = Maze(width, height, entry, goal)
    maze.generate("recdiv", animate=animate)   # calls Maze._recdiv_generate

    if render:
        render.draw_maze(maze, entry=maze.start, goal=maze.goal)
        render.update()
    return maze, maze.start, maze.goal