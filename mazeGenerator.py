import tkinter as tk
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

def draw_maze(maze):
    canvas.delete("all")
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if (x, y) == (1, 1):
                color = 'green'
            elif (x, y) == (len(maze[0])-2, len(maze)-2):
                color = 'red'
            else:
                color = 'black' if maze[y][x] == 1 else 'white'
            canvas.create_rectangle(x*10, y*10, x*10+10, y*10+10, fill=color, outline=color)

def regenerate_maze():
    global maze
    maze = generate_maze(51, 51)
    draw_maze(maze)

def play():
    path = []
    find_path(maze, 1, 1, path)

def find_path(maze, x, y, path):
    if (x, y) == (len(maze[0])-2, len(maze)-2):
        path.append((x, y))
        return True
    if maze[y][x] == 1 or (x, y) in path:
        return False
    path.append((x, y))
    canvas.create_rectangle(x*10, y*10, x*10+10, y*10+10, fill='blue', outline='blue')
    canvas.update()
    canvas.after(20)  # Delay to visualize the exploration
    if (find_path(maze, x+1, y, path) or find_path(maze, x-1, y, path) or
        find_path(maze, x, y+1, path) or find_path(maze, x, y-1, path)):
        return True
    path.pop()
    canvas.create_rectangle(x*10, y*10, x*10+10, y*10+10, fill='white', outline='white')
    canvas.update()
    canvas.after(50)
    return False

root = tk.Tk()
root.title("Maze Generator")

menu_frame = tk.Frame(root)
menu_frame.pack(side=tk.TOP, fill=tk.X)

regenerate_button = tk.Button(menu_frame, text="Regenerate", command=regenerate_maze)
regenerate_button.pack(side=tk.LEFT)

play_button = tk.Button(menu_frame, text="Play", command=play)
play_button.pack(side=tk.LEFT)

fastest_path_button = tk.Button(menu_frame, text="Fastest Path")
fastest_path_button.pack(side=tk.LEFT)

canvas = tk.Canvas(root, width=500, height=500, bg='white')
canvas.pack()

maze = generate_maze(51, 51)
draw_maze(maze)

root.mainloop()
