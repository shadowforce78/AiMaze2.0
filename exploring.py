import tkinter as tk

COLORS = {
    "explored": "#3498DB",
    "path": "#ECF0F1",
}

def find_path(maze, x, y, path, algorithm, canvas, difficulty_slider, speed_slider, exploring, max_depth, depth=0):
    if algorithm == "DFS":
        return dfs(maze, x, y, path, canvas, difficulty_slider, speed_slider, exploring, max_depth, depth)
    elif algorithm == "BFS":
        return bfs(maze, x, y, path, canvas, difficulty_slider, speed_slider, exploring)
    return False

def dfs(maze, x, y, path, canvas, difficulty_slider, speed_slider, exploring, max_depth, depth=0):
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
        (x + 1 < len(maze[0]) and dfs(maze, x + 1, y, path, canvas, difficulty_slider, speed_slider, exploring, max_depth, depth + 1))
        or (x - 1 >= 0 and dfs(maze, x - 1, y, path, canvas, difficulty_slider, speed_slider, exploring, max_depth, depth + 1))
        or (y + 1 < len(maze) and dfs(maze, x, y + 1, path, canvas, difficulty_slider, speed_slider, exploring, max_depth, depth + 1))
        or (y - 1 >= 0 and dfs(maze, x, y - 1, path, canvas, difficulty_slider, speed_slider, exploring, max_depth, depth + 1))
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

def bfs(maze, x, y, path, canvas, difficulty_slider, speed_slider, exploring):
    # Implement BFS algorithm here
    pass