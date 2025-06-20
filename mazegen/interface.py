# mazegen/interface.py

import numpy as np
from maze_generators import dfs, handk, kruskals, prims, recdiv, wilsons  # Add others as needed

GENERATOR_MAP = {
    "dfs": dfs.generate_maze,
    "prims": prims.generate_maze,
    "wilsons": wilsons.generate_maze,
    "recdiv": recdiv.generate_maze,
    "handk": handk.generate_maze,
    "kruskals": kruskals.generate_maze
}

def generate_maze(algo: str, size: int = 21) -> tuple[np.ndarray, tuple[int, int], tuple[int, int]]:
    if algo not in GENERATOR_MAP:
        raise ValueError(f"Unknown algorithm '{algo}'. Valid options: {list(GENERATOR_MAP.keys())}")
    
    # We assume each generator returns (maze, start, goal)
    return GENERATOR_MAP[algo](width=size, height=size)
