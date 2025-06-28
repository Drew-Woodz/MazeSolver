# maze_generators/kruskals.py
from models.maze import Maze

def generate_maze(width:int, height:int,
                  entry=(0,0), goal=None,
                  render=None, animate:bool=False):
    m = Maze(width, height, entry, goal)
    m.generate("kruskals", animate=animate)
    if render:
        render.draw_maze(m, entry=m.start, goal=m.goal)
        render.update()
    return m, m.start, m.goal

