import sys
import random
import tkinter as tk
from tkinter import messagebox
import time
from exploring import find_path  # Import the find_path function

# Define color scheme
COLORS = {
    "background": "#2C3E50",
    "wall": "#34495E",
    "path": "#ECF0F1",
    "start": "#2ECC71",
    "end": "#E74C3C",
    "explored": "#3498DB",
    "button_bg": "#3498DB",
    "button_fg": "white",
}

exploring = False  # Add this global variable
max_depth = 0  # Add this global variable to track maximum recursion depth
warning_shown = False  # Add this global variable

def max_depth_limit():
    sys.setrecursionlimit(10**6)

def generate_maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]
    stack = [(1, 1)]
    maze[1][1] = 0

    while stack:
        x, y = stack[-1]
        neighbors = []

        if x > 2 and maze[y][x - 2] == 1:
            neighbors.append((x - 2, y))
        if x < width - 3 and maze[y][x + 2] == 1:
            neighbors.append((x + 2, y))
        if y > 2 and maze[y - 2][x] == 1:
            neighbors.append((x, y - 2))
        if y < height - 3 and maze[y + 2][x] == 1:
            neighbors.append((x, y + 2))

        if neighbors:
            nx, ny = random.choice(neighbors)
            maze[ny][nx] = 0
            maze[(ny + y) // 2][(nx + x) // 2] = 0
            stack.append((nx, ny))
        else:
            stack.pop()

    return maze

def draw_maze(maze):
    canvas.delete("all")
    size = difficulty_slider.get() * 2 + 1
    cell_size = max(1, 500 // size)  # Adjust cell size based on maze size
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if (x, y) == (1, 1):
                color = COLORS["start"]
            elif (x, y) == (len(maze[0]) - 2, len(maze) - 2):
                color = COLORS["end"]
            else:
                color = COLORS["wall"] if maze[y][x] == 1 else COLORS["path"]

            # Draw all cells, not just walls
            canvas.create_rectangle(
                x * cell_size,
                y * cell_size,
                x * cell_size + cell_size,
                y * cell_size + cell_size,
                fill=color,
                outline=color,
                width=0,
            )

def adjust_window_size(size):
    cell_size = max(1, 500 // size)  # Adjust cell size based on maze size
    canvas.config(width=size * cell_size, height=size * cell_size)
    root.geometry(f"{size * cell_size + 40}x{size * cell_size + 220}")  # Adjust height dynamically

def regenerate_maze():
    global maze, exploring, warning_shown
    if exploring:
        exploring = False  # Stop the exploration if in progress
    size = difficulty_slider.get() * 2 + 1  # Adjust size based on difficulty
    if size > 150 and not warning_shown:
        messagebox.showwarning("Warning", "High difficulty may impact performance.")
        warning_shown = True  # Set the flag to True after showing the warning
    maze = generate_maze(size, size)
    draw_maze(maze)
    adjust_window_size(size)

def clear_canvas():
    draw_maze(maze)  # Redraw the maze in its initial state

def play():
    global exploring, warning_shown, execution_times
    warning_shown = False  # Reset the warning flag when starting a new exploration
    if exploring:
        return  # Do nothing if already exploring
    exploring = True
    path = []
    start_time = time.time()  # Record start time
    find_path(
        maze,
        1,
        1,
        path,
        algorithm_var.get(),
        canvas,
        difficulty_slider,
        speed_slider,
        exploring,
        max_depth,
    )  # Pass the necessary parameters
    exploring = False  # Reset exploring flag when done
    end_time = time.time()  # Record end time
    elapsed_time = end_time - start_time  # Calculate elapsed time
    time_label.config(text=f"Time: {elapsed_time:.2f} seconds")

root = tk.Tk()
root.title("Maze Explorer")
root.configure(bg=COLORS["background"])

# Create title
title_label = tk.Label(
    root,
    text="Maze Explorer",
    font=("Helvetica", 16, "bold"),
    bg=COLORS["background"],
    fg="white",
    pady=10,
)
title_label.pack()

# Define button style
button_style = {
    "font": ("Helvetica", 10),
    "width": 10,
    "bg": COLORS["button_bg"],
    "fg": COLORS["button_fg"],
    "relief": "flat",
    "pady": 5,
}

# Style the menu frame
menu_frame = tk.Frame(root, bg=COLORS["background"], pady=10)
menu_frame.pack(side=tk.TOP, fill=tk.X)

# Create a frame for buttons and sliders
controls_frame = tk.Frame(menu_frame, bg=COLORS["background"])
controls_frame.pack(side=tk.LEFT, padx=5)

# Create a frame for buttons
button_frame = tk.Frame(controls_frame, bg=COLORS["background"])
button_frame.pack(side=tk.TOP, padx=5, pady=5)

regenerate_button = tk.Button(button_frame, text="Regenerate", command=regenerate_maze, **button_style)
regenerate_button.pack(side=tk.LEFT, padx=5)

play_button = tk.Button(button_frame, text="Play", command=play, **button_style)
play_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(button_frame, text="Clear", command=clear_canvas, **button_style)
clear_button.pack(side=tk.LEFT, padx=5)

# Create a frame for sliders
sliders_frame = tk.Frame(controls_frame, bg=COLORS["background"])
sliders_frame.pack(side=tk.TOP, padx=5, pady=5)

# Create difficulty slider
difficulty_slider = tk.Scale(
    sliders_frame,
    from_=5,
    to=150,  # Difficulty range from 5 to 150
    orient=tk.HORIZONTAL,
    label="Difficulty",
    bg=COLORS["background"],
    fg="white",
    troughcolor=COLORS["button_bg"],
    highlightthickness=0,
)
difficulty_slider.set(25)  # Set default difficulty
difficulty_slider.pack(side=tk.LEFT, padx=5)

# Create speed slider
speed_slider = tk.Scale(
    sliders_frame,
    from_=1,
    to=500,  # Speed range from 1 to 500
    orient=tk.HORIZONTAL,
    label="Speed",
    bg=COLORS["background"],
    fg="white",
    troughcolor=COLORS["button_bg"],
    highlightthickness=0,
)
speed_slider.set(100)  # Set default speed
speed_slider.pack(side=tk.LEFT, padx=5)

# Create a frame for the timer and algorithm dropdown
timer_algo_frame = tk.Frame(menu_frame, bg=COLORS["background"], pady=10)
timer_algo_frame.pack(side=tk.LEFT, padx=5)

# Create time label
time_label = tk.Label(
    timer_algo_frame,
    text="Time: 0.00 seconds",
    font=("Helvetica", 12),
    bg=COLORS["background"],
    fg="white",
    pady=10,
)
time_label.pack(side=tk.TOP, pady=5)

# Create algorithm dropdown menu
algorithm_var = tk.StringVar(root)
algorithm_var.set("DFS")  # Set default algorithm

algorithm_menu = tk.OptionMenu(
    timer_algo_frame,
    algorithm_var,
    "DFS",
    "A*",
    "BFS",
    "Right-Hand",
    "Left-Hand",
    "Flood Fill",
)
algorithm_menu.config(
    bg=COLORS["button_bg"],
    fg=COLORS["button_fg"],
    font=("Helvetica", 10),
    relief="flat",
)
algorithm_menu.pack(side=tk.TOP, pady=5)

# Create a frame for the canvas with padding
canvas_frame = tk.Frame(root, bg=COLORS["background"], padx=20, pady=20)
canvas_frame.pack(expand=True, fill=tk.BOTH)

canvas = tk.Canvas(
    canvas_frame, width=500, height=500, bg=COLORS["path"], highlightthickness=0
)
canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

# Add hover effects for buttons
def on_enter(e):
    e.widget["background"] = "#2980B9"

def on_leave(e):
    e.widget["background"] = COLORS["button_bg"]

for button in [regenerate_button, play_button, clear_button]:
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

# Initialize the maze
max_depth_limit()
maze = generate_maze(51, 51)
draw_maze(maze)
adjust_window_size(51)

root.mainloop()
