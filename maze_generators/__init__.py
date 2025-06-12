# maze_generators/__init__.py
from maze_generators.dfs_backtracker import generate_maze as dfs_backtracker
from maze_generators.prims_algorithm import generate_maze as prims

generators = {
    "DFS Backtracker": dfs_backtracker,
    "Prim's Algorithm": prims,
    # "Wilson's Algorithm": wilsons,
    # etc.
}
