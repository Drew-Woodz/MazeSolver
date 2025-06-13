# visualizer/grid_plot.py
import matplotlib.pyplot as plt

def plot_maze(maze, start=None, goal=None):
    plt.figure(figsize=(6,6))
    plt.imshow(maze, cmap="gray", vmin=0, vmax=1, interpolation="none")

    if start:
        plt.plot(start[1], start[0], "bo")  # blue dot for start
    if goal:
        plt.plot(goal[1], goal[0], "go")    # green dot for goal
    plt.xticks([]); plt.yticks([])
    plt.show()
