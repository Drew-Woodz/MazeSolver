# mazegen/cli.py

import os
from datetime import datetime
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
    parser.add_argument("--style", type=str, default="blocks", choices=["blocks", "dots", "unicode", "roguelike"], help="ASCII style")
    parser.add_argument("--save-meta", action="store_true", help="Save metadata about the maze generation")


    args = parser.parse_args()
    maze, start, goal = generate_maze(args.algo, args.size)

    if args.format == "json":
        result = {
            "maze": maze.tolist(),
            "start": start,
            "goal": goal
        }
        output = json.dumps(result, indent=2)
        if args.output:
            with open(args.output, "w") as f:
                f.write(output)
        else:
            print(output)

    elif args.format == "ascii":
        output = ascii_render(maze, style=args.style)
        if args.output:
            with open(args.output, "w") as f:
                f.write(output)
        else:
            print(output)        

    elif args.format == "npy":
        if not args.output:
            raise ValueError("Output file required for .npy format")

        # Save maze to .npy
        np.save(args.output, maze)

        # Also save start and goal as JSON sidecar
        meta_path = args.output.rsplit(".", 1)[0] + "_meta.json"
        with open(meta_path, "w") as f:
            json.dump({"start": start, "goal": goal}, f)

        print(f"Saved .npy to {args.output}")
        print(f"Saved metadata to {meta_path}")

    if args.save_meta and args.output and args.format != "npy":
        meta = {
            "algo": args.algo,
            "size": args.size,
            "start": start,
            "goal": goal,
            "format": args.format,
            "style": args.style if args.format == "ascii" else None,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        meta_path = os.path.splitext(args.output)[0] + ".meta.json"
        with open(meta_path, "w") as f:
            json.dump(meta, f, indent=2)
        print(f"Saved metadata to {meta_path}")

if __name__ == "__main__":
    main()
