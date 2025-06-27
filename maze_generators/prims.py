# maze_generators/prims.py
from models.maze import Maze

def generate_maze(width: int, height: int,
                  entry=(0,0), goal=None,
                  render=None, animate: bool=False):
    maze = Maze(width, height, entry, goal)
    maze.generate("prims", animate=animate)     # calls Maze._prims_generate

    if render:
        render.draw_maze(maze, entry=maze.start, goal=maze.goal)
        render.update()
    return maze, maze.start, maze.goal          # <-- return the Maze instance
