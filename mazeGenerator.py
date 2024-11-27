import tkinter as tk
from tkinter import ttk
import random

def generate_maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]
    stack = [(1, 1)]
    maze[1][1] = 0

    while stack:
        x, y = stack[-1]
        neighbors = []

        if x > 2 and maze[y][x-2] == 1:
            neighbors.append((x-2, y))
        if x < width-3 and maze[y][x+2] == 1:
            neighbors.append((x+2, y))
        if y > 2 and maze[y-2][x] == 1:
            neighbors.append((x, y-2))
        if y < height-3 and maze[y+2][x] == 1:
            neighbors.append((x, y+2))

        if neighbors:
            nx, ny = random.choice(neighbors)
            maze[ny][nx] = 0
            maze[(ny+y)//2][(nx+x)//2] = 0
            stack.append((nx, ny))
        else:
            stack.pop()

    return maze

# Define color scheme
COLORS = {
    'background': '#2C3E50',
    'wall': '#34495E',
    'path': '#ECF0F1',
    'start': '#2ECC71',
    'end': '#E74C3C',
    'explored': '#3498DB',
    'button_bg': '#3498DB',
    'button_fg': 'white'
}

def draw_maze(maze):
    canvas.delete("all")
    cell_size = 10
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if (x, y) == (1, 1):
                color = COLORS['start']
            elif (x, y) == (len(maze[0])-2, len(maze)-2):
                color = COLORS['end']
            else:
                color = COLORS['wall'] if maze[y][x] == 1 else COLORS['path']
            
            # Draw all cells, not just walls
            canvas.create_rectangle(
                x*cell_size,
                y*cell_size,
                x*cell_size+cell_size,
                y*cell_size+cell_size,
                fill=color,
                outline=color,
                width=0
            )

exploring = False  # Add this global variable

def regenerate_maze():
    global maze, exploring
    if exploring:
        exploring = False  # Stop the exploration if in progress
    maze = generate_maze(51, 51)
    draw_maze(maze)

def play():
    global exploring
    if exploring:
        return  # Do nothing if already exploring
    exploring = True
    path = []
    find_path(maze, 1, 1, path)
    exploring = False  # Reset exploring flag when done

def find_path(maze, x, y, path):
    global exploring
    if not exploring:
        return False
    if (x, y) == (len(maze[0])-2, len(maze)-2):
        path.append((x, y))
        return True
    if maze[y][x] == 1 or (x, y) in path:
        return False
    
    path.append((x, y))
    cell_size = 10
    # Draw the exploration cell
    canvas.create_rectangle(
        x*cell_size,
        y*cell_size,
        x*cell_size+cell_size,
        y*cell_size+cell_size,
        fill=COLORS['explored'],
        outline=COLORS['explored'],
        width=0
    )
    canvas.update()
    canvas.after(20)

    if (find_path(maze, x+1, y, path) or find_path(maze, x-1, y, path) or
        find_path(maze, x, y+1, path) or find_path(maze, x, y-1, path)):
        return True
    
    path.pop()
    # When backtracking, return to path color
    canvas.create_rectangle(
        x*cell_size,
        y*cell_size,
        x*cell_size+cell_size,
        y*cell_size+cell_size,
        fill=COLORS['path'],
        outline=COLORS['path'],
        width=0
    )
    canvas.update()
    canvas.after(50)
    return False

root = tk.Tk()
root.title("Maze Explorer")
root.configure(bg=COLORS['background'])

# Create title
title_label = tk.Label(
    root,
    text="Maze Explorer",
    font=("Helvetica", 16, "bold"),
    bg=COLORS['background'],
    fg='white',
    pady=10
)
title_label.pack()

# Style the menu frame
menu_frame = tk.Frame(root, bg=COLORS['background'], pady=10)
menu_frame.pack(side=tk.TOP, fill=tk.X)

# Style buttons
button_style = {
    'font': ('Helvetica', 10),
    'width': 12,
    'bg': COLORS['button_bg'],
    'fg': COLORS['button_fg'],
    'relief': 'flat',
    'pady': 5
}

regenerate_button = tk.Button(menu_frame, text="Regenerate", command=regenerate_maze, **button_style)
regenerate_button.pack(side=tk.LEFT, padx=5)

play_button = tk.Button(menu_frame, text="Play", command=play, **button_style)
play_button.pack(side=tk.LEFT, padx=5)

# Create a frame for the canvas with padding
canvas_frame = tk.Frame(
    root,
    bg=COLORS['background'],
    padx=20,
    pady=20
)
canvas_frame.pack(expand=True, fill=tk.BOTH)

canvas = tk.Canvas(
    canvas_frame,
    width=500,
    height=500,
    bg=COLORS['path'],
    highlightthickness=0
)
canvas.pack()

# Add hover effects for buttons
def on_enter(e):
    e.widget['background'] = '#2980B9'

def on_leave(e):
    e.widget['background'] = COLORS['button_bg']

for button in [regenerate_button, play_button]:
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

# Initialize the maze
maze = generate_maze(51, 51)
draw_maze(maze)

root.mainloop()
