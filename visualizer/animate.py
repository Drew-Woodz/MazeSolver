import matplotlib.pyplot as plt
from IPython.display import clear_output, display
import time

def animate_maze_step(maze_frame):
    clear_output(wait=True)
    plt.imshow(maze_frame, cmap="gray", vmin=0, vmax=1)
    plt.axis("off")
    display(plt.gcf())
    plt.pause(0.001)
