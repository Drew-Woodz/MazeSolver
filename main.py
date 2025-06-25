# main.py
import argparse
from visualizer.pygame_renderer import PygameRenderer
from models.maze import Maze

# Import all algorithms
import maze_generators.dfs as dfs
import maze_generators.prims as prims
import maze_generators.wilsons as wilsons
import maze_generators.recdiv as recdiv
import maze_generators.handk as handk
import maze_generators.kruskals as kruskals
# Solver imports
from solvers.a_star import solve as a_star_solver
from solvers.dijkstra import solve as dijkstra_solver
from solvers.bfs import solve as bfs_solver
from solvers.greedy import solve as greedy_solver
from solvers.dfs import solve as dfs_solver
from solvers.bidirectional import solve as bidirectional_solver

algorithms = {
    1: dfs.generate_maze,
    2: prims.generate_maze,
    3: wilsons.generate_maze,
    4: recdiv.generate_maze,
    5: handk.generate_maze,
    6: kruskals.generate_maze
}

algo_names = {
    1: "DFS Backtracker",
    2: "Prim's Algorithm",
    3: "Wilson's Algorithm",
    4: "Recursive Division",
    5: "Hunt and Kill",
    6: "Kruskal's Algorithm"
}

solvers = {
    1: a_star_solver,
    2: dijkstra_solver,
    3: bfs_solver,
    4: greedy_solver,
    5: dfs_solver,
    6: bidirectional_solver,
}

solver_names = {
    1: "A* Search",
    2: "Dijkstra's Algorithm",
    3: "Breadth-First Search",
    4: "Greedy Best-First Search",
    5: "Depth-First Search",
    6: "Bidirectional_solver",
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Maze Generator Visualizer")
    parser.add_argument('--algo', type=int, choices=range(1, 7), default=1,
                        help="Choose maze generation algorithm (1=DFS Backtracker, 2=Prim's, 3=Wilson's, 4=Recursive Division, 5=Hunt & Kill, 6=Kruskal's)")
    parser.add_argument('--size', type=int, default=50,
                        help="Maze width and height (in cells)")
    parser.add_argument('--solve', type=int, choices=range(1, 7), default=0,
                        help="Choose maze solving algorithm (1=A*, 2=Dijkstra, 3=BFS, 4=Greedy, 5=DFS, 6=Bidirectional)")
    parser.add_argument('--animate', action='store_true',
                        help="Enable animation for maze generation")
    parser.add_argument('--animate-solve', action='store_true',
                        help="Enable animation for solver")

    args = parser.parse_args()

    algo_fn = algorithms[args.algo]
    algo_name = algo_names[args.algo]

    print(f"Generating maze using {algo_name} (size {args.size}x{args.size})...")
    renderer = PygameRenderer(Maze(args.size, args.size))
    maze, start, goal = algo_fn(args.size, args.size, render=renderer if args.animate else None)

    if args.solve:
        solver_fn = solvers[args.solve]
        solver_name = solver_names[args.solve]
        print(f"Solving maze with {solver_name}...")
        if args.animate_solve:
            path = solver_fn(maze, start, goal, render=renderer)
            for pos in path:
                renderer.mark_cell(pos, color=(0, 255, 0))
                renderer.update(delay=0.1)  # Step-by-step animation
        else:
            solver_fn(maze, start, goal, render=renderer)

    if renderer.running:
        renderer.wait_for_exit()