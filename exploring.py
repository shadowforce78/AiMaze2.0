import tkinter as tk
import heapq

COLORS = {
    "explored": "#3498DB",
    "path": "#ECF0F1",
}

def find_path(maze, x, y, path, algorithm, canvas, difficulty_slider, speed_slider, exploring, max_depth, depth=0):
    if algorithm == "DFS":
        return dfs(maze, x, y, path, canvas, difficulty_slider, speed_slider, exploring, max_depth, depth)
    elif algorithm == "A*":
        return a_star(maze, x, y, path, canvas, difficulty_slider, speed_slider, exploring)
    elif algorithm == "BFS":
        return bfs(maze, x, y, path, canvas, difficulty_slider, speed_slider, exploring)
    return False

# DFS (Depth First Search) algorithm
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

# A* algorithm (A Star)
def a_star(maze, x, y, path, canvas, difficulty_slider, speed_slider, exploring):
    if not exploring:
        return False

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    start = (x, y)
    goal = (len(maze[0]) - 2, len(maze) - 2)
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    explored_cells = set()  # To track all explored cells

    size = difficulty_slider.get() * 2 + 1
    cell_size = max(1, 500 // size)

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()

            # Color the final path
            for (px, py) in path:
                canvas.create_rectangle(
                    px * cell_size,
                    py * cell_size,
                    px * cell_size + cell_size,
                    py * cell_size + cell_size,
                    fill=COLORS["explored"],
                    outline=COLORS["explored"],
                    width=0
                )

            # Color incorrect paths in orange
            for (ex, ey) in explored_cells:
                if (ex, ey) not in path:
                    canvas.create_rectangle(
                        ex * cell_size,
                        ey * cell_size,
                        ex * cell_size + cell_size,
                        ey * cell_size + cell_size,
                        # fill="orange",  # Orange for incorrect paths
                        # outline="orange",
                        fill = COLORS["path"],
                        outline = COLORS["path"],
                        width=0
                    )
            canvas.update()
            return True

        explored_cells.add(current)  # Mark cell as explored

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < len(maze[0]) and 0 <= neighbor[1] < len(maze) and maze[neighbor[1]][neighbor[0]] == 0:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

                    # Draw the exploration cell
                    canvas.create_rectangle(
                        neighbor[0] * cell_size,
                        neighbor[1] * cell_size,
                        neighbor[0] * cell_size + cell_size,
                        neighbor[1] * cell_size + cell_size,
                        fill=COLORS["explored"],
                        outline=COLORS["explored"],
                        width=0
                    )
                    canvas.update()
                    canvas.after(1000 // speed_slider.get())  # Adjust speed based on slider value

    # If no path is found, still color the explored cells
    for (ex, ey) in explored_cells:
        canvas.create_rectangle(
            ex * cell_size,
            ey * cell_size,
            ex * cell_size + cell_size,
            ey * cell_size + cell_size,
            fill="orange",  # Orange for explored cells
            outline="orange",
            width=0
        )
    canvas.update()
    return False

# BFS (Breadth First Search) algorithm
def bfs(maze, x, y, path, canvas, difficulty_slider, speed_slider, exploring):
    if not exploring:
        return False

    start = (x, y)
    goal = (len(maze[0]) - 2, len(maze) - 2)
    queue = [start]
    came_from = {}
    explored_cells = set()  # To track all explored cells

    size = difficulty_slider.get() * 2 + 1
    cell_size = max(1, 500 // size)

    while queue:
        current = queue.pop(0)

        if current == goal:
            while current != start:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()

            # Color the final path
            for (px, py) in path:
                canvas.create_rectangle(
                    px * cell_size,
                    py * cell_size,
                    px * cell_size + cell_size,
                    py * cell_size + cell_size,
                    fill=COLORS["explored"],
                    outline=COLORS["explored"],
                    width=0
                )

            # Color incorrect paths in orange
            for (ex, ey) in explored_cells:
                if (ex, ey) not in path:
                    canvas.create_rectangle(
                        ex * cell_size,
                        ey * cell_size,
                        ex * cell_size + cell_size,
                        ey * cell_size + cell_size,
                        fill="orange",  # Orange for incorrect paths
                        outline="orange",
                        width=0
                    )
            canvas.update()
            return True

        explored_cells.add(current)  # Mark cell as explored

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < len(maze[0]) and 0 <= neighbor[1] < len(maze) and maze[neighbor[1]][neighbor[0]] == 0 and neighbor not in came_from:
                came_from[neighbor] = current
                queue.append(neighbor)

                # Draw the exploration cell
                canvas.create_rectangle(
                    neighbor[0] * cell_size,
                    neighbor[1] * cell_size,
                    neighbor[0] * cell_size + cell_size,
                    neighbor[1] * cell_size + cell_size,
                    fill=COLORS["explored"],
                    outline=COLORS["explored"],
                    width=0
                )
                canvas.update()
                canvas.after(1000 // speed_slider.get())
                
    # If no path is found, still color the explored cells
    for (ex, ey) in explored_cells:
        canvas.create_rectangle(
            ex * cell_size,
            ey * cell_size,
            ex * cell_size + cell_size,
            ey * cell_size + cell_size,
            fill="orange",  # Orange for explored cells
            outline="orange",
            width=0
        )
        
    canvas.update()
    return False
