from mazeGenerator import *
import tkinter as tk
from mazeGenerator import COLORS

exploring = False  # Add this global variable
max_depth = 0  # Add this global variable to track maximum recursion depth

def play():
    global exploring
    if exploring:
        return  # Do nothing if already exploring
    exploring = True
    path = []
    find_path(maze, 1, 1, path)
    exploring = False  # Reset exploring flag when done

def find_path(maze, x, y, path, depth=0):
    global exploring, max_depth
    if not exploring:
        return False
    if depth > max_depth:
        max_depth = depth
    if (x, y) == (len(maze[0]) - 2, len(maze) - 2):
        path.append((x, y))
        return True
    if maze[y][x] == 1 or (x, y) in path:
        return False

    path.append((x, y))
    size = difficulty_slider.get() * 2 + 1
    cell_size = max(1, 500 // size)  # Adjust cell size based on maze size
    # Draw the exploration cell
    canvas.create_rectangle(
        x * cell_size,
        y * cell_size,
        x * cell_size + cell_size,
        y * cell_size + cell_size,
        fill=COLORS["explored"],
        outline=COLORS["explored"],
        width=0,
    )
    canvas.update()
    canvas.after(1000 // speed_slider.get())  # Adjust speed based on slider value

    # Check boundaries before recursive calls
    if (
        (x + 1 < len(maze[0]) and find_path(maze, x + 1, y, path, depth + 1))
        or (x - 1 >= 0 and find_path(maze, x - 1, y, path, depth + 1))
        or (y + 1 < len(maze) and find_path(maze, x, y + 1, path, depth + 1))
        or (y - 1 >= 0 and find_path(maze, x, y - 1, path, depth + 1))
    ):
        return True

    path.pop()
    # When backtracking, leave an orange trail
    canvas.create_rectangle(
        x * cell_size,
        y * cell_size,
        x * cell_size + cell_size,
        y * cell_size + cell_size,
        fill="orange",
        outline="orange",
        width=0,
    )
    canvas.update()
    canvas.after(1000 // speed_slider.get())  # Adjust speed based on slider value
    return False