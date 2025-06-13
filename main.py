# main.py

import argparse
from visualizer.pygame_renderer import PygameRenderer

# Import all algorithms
import maze_generators.dfs_backtracker as dfs_backtracker
import maze_generators.prims_algorithm as prims_algorithm
import maze_generators.wilsons_algorithm as wilsons_algorithm
import maze_generators.recursive_division as recursive_division
import maze_generators.hunt_and_kill as hunt_and_kill
import maze_generators.kruskals_algorithm as kruskals_algorithm


algorithms = {
    1: dfs_backtracker.generate_maze,
    2: prims_algorithm.generate_maze,
    3: wilsons_algorithm.generate_maze,
    4: recursive_division.generate_maze,
    5: hunt_and_kill.generate_maze,
    6: kruskals_algorithm.generate_maze
}

algo_names = {
    1: "DFS Backtracker",
    2: "Prim's Algorithm",
    3: "Wilson's Algorithm",
    4: "Recursive Division",
    5: "Hunt and Kill",
    6: "Kruskal's Algorithm"
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Maze Generator Visualizer")
    parser.add_argument('--algo', type=int, choices=range(1, 7), default=1,
                        help="Choose maze generation algorithm (1–6)")
    parser.add_argument('--size', type=int, default=50,
                        help="Maze width and height (in cells)")

    args = parser.parse_args()
    algo_fn = algorithms[args.algo]
    algo_name = algo_names[args.algo]

    print(f"Generating maze using {algo_name} (size {args.size}x{args.size})...")

    renderer = PygameRenderer(args.size, args.size)
    algo_fn(args.size, args.size, render=renderer)
