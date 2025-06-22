# gui/helpers.py

def convert_maze_for_gui(maze):
    # Strip walls, leave only real cells
    return maze[1::2, 1::2]

def convert_coords_for_gui(coord):
    x, y = coord
    return ((x - 1) // 2, (y - 1) // 2)
