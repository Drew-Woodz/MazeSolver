# maze_generators/__init__.py
from maze_generators.dfs_backtracker import generate_maze as dfs_backtracker
from maze_generators.prims_algorithm import generate_maze as prims
from maze_generators.wilsons_algorithm import generate_maze as wilsons
from maze_generators.recursive_division import generate_maze as recursive_division

generators = {
    "DFS Backtracker": dfs_backtracker,
    "Prim's Algorithm": prims,
    "Wilson's Algorithm": wilsons,
    "Recursive Division": recursive_division,
    # etc.
}
