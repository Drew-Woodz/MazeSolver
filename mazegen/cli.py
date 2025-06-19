# mazegen/cli.py

import argparse
import json
import numpy as np
from mazegen.interface import generate_maze

def ascii_render(maze, style="blocks"):
    themes = {
        "blocks": {0: "█", 1: "░"},
        "dots": {0: "█", 1: "·"},
        "unicode": {0: "⬛", 1: "⬜"},
        "roguelike": {0: "#", 1: "."},
    }
    chars = themes.get(style, themes["blocks"])
    return "\n".join("".join(chars[cell] for cell in row) for row in maze)

def main():
    parser = argparse.ArgumentParser(description="Maze generator CLI")
    parser.add_argument("--algo", type=str, required=True, help="Algorithm to use (e.g., dfs, prims)")
    parser.add_argument("--size", type=int, default=21, help="Size of the maze (must be odd)")
    parser.add_argument("--format", type=str, default="json", choices=["json", "ascii", "npy"], help="Output format")
    parser.add_argument("--output", type=str, default=None, help="Output file (default: stdout)")
    parser.add_argument("--style", type=str, default="blocks", choices=["blocks", "dots", "unicode", "roguelike"], help="Character style for ASCII output")

    args = parser.parse_args()

    maze, start, goal = generate_maze(args.algo, args.size)

    if args.format == "json":
        result = {
            "maze": maze.tolist(),
            "start": start,
            "goal": goal
        }
        output = json.dumps(result, indent=2)
    elif args.format == "ascii":
        output = ascii_render(maze, style=args.style)
    elif args.format == "npy":
        if not args.output:
            raise ValueError("Output file required for .npy format")
        np.save(args.output, maze)
        print(f"Saved .npy to {args.output}")
        return

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
    else:
        print(output)

if __name__ == "__main__":
    main()
