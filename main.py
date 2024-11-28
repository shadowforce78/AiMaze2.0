import tkinter as tk
from mazeGenerator import *

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
    to=1000,  # Speed range from 1 to 100
    orient=tk.HORIZONTAL,
    label="Speed",
    bg=COLORS["background"],
    fg="white",
    troughcolor=COLORS["button_bg"],
    highlightthickness=0,
)
speed_slider.set(100)  # Set default speed
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