import tkinter as tk
import sys
import random


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


exploring = False  # Add this global variable
max_depth = 0  # Add this global variable to track maximum recursion depth


def regenerate_maze():
    global maze, exploring
    if exploring:
        exploring = False  # Stop the exploration if in progress
    size = difficulty_slider.get() * 2 + 1  # Adjust size based on difficulty
    maze = generate_maze(size, size)
    draw_maze(maze)
    adjust_window_size(size)


def adjust_window_size(size):
    cell_size = max(1, 500 // size)  # Adjust cell size based on maze size
    canvas.config(width=size * cell_size, height=size * cell_size)
    root.geometry(
        f"{size * cell_size + 40}x{size * cell_size + 160}"
    )  # Increase height to ensure bottom-right corner is visible


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
        # max_depth_label.config(text=f"Max Depth: {max_depth}")  # Remove max depth label update
    # current_depth_label.config(text=f"Current Depth: {depth}")  # Remove current depth label update
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
    # When backtracking, return to path color
    canvas.create_rectangle(
        x * cell_size,
        y * cell_size,
        x * cell_size + cell_size,
        y * cell_size + cell_size,
        fill=COLORS["path"],
        outline=COLORS["path"],
        width=0,
    )
    canvas.update()
    canvas.after(1000 // speed_slider.get())  # Adjust speed based on slider value
    return False


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

# Style the menu frame
menu_frame = tk.Frame(root, bg=COLORS["background"], pady=10)
menu_frame.pack(side=tk.TOP, fill=tk.X)

# Style buttons
button_style = {
    "font": ("Helvetica", 10),
    "width": 12,
    "bg": COLORS["button_bg"],
    "fg": COLORS["button_fg"],
    "relief": "flat",
    "pady": 5,
}

regenerate_button = tk.Button(
    menu_frame, text="Regenerate", command=regenerate_maze, **button_style
)
regenerate_button.pack(side=tk.LEFT, padx=5)

play_button = tk.Button(menu_frame, text="Play", command=play, **button_style)
play_button.pack(side=tk.LEFT, padx=5)

# Create difficulty slider
difficulty_slider = tk.Scale(
    menu_frame,
    from_=5,
    to=100,  # Difficulty range from 5 to 100
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
    menu_frame,
    from_=1,
    to=100,  # Speed range from 1 to 100
    orient=tk.HORIZONTAL,
    label="Speed",
    bg=COLORS["background"],
    fg="white",
    troughcolor=COLORS["button_bg"],
    highlightthickness=0,
)
speed_slider.set(50)  # Set default speed
speed_slider.pack(side=tk.LEFT, padx=5)

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


for button in [regenerate_button, play_button]:
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

# Initialize the maze
max_depth_limit()
maze = generate_maze(51, 51)
draw_maze(maze)
adjust_window_size(51)

root.mainloop()
