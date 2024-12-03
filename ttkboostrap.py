import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
import random

# Setup root with ttkbootstrap
root = ttk.Window(themename="darkly")  # Utiliser un thème moderne
root.title("Maze Explorer 2.0")
root.geometry("600x700")

# Utilisation des widgets ttkbootstrap
title_label = ttk.Label(
    root,
    text="Maze Explorer 2.0",
    font=("Poppins", 24, "bold"),
    anchor="center",
)
title_label.pack(pady=20)

# Style des boutons avec ttkbootstrap
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

generate_button = ttk.Button(button_frame, text="Generate Maze", bootstyle=PRIMARY, command=lambda: print("Generate!"))
generate_button.grid(row=0, column=0, padx=10)

solve_button = ttk.Button(button_frame, text="Solve Maze", bootstyle=SUCCESS, command=lambda: print("Solve!"))
solve_button.grid(row=0, column=1, padx=10)

reset_button = ttk.Button(button_frame, text="Reset Maze", bootstyle=INFO, command=lambda: print("Reset!"))
reset_button.grid(row=0, column=2, padx=10)

# Add a slider for difficulty
difficulty_slider = ttk.Scale(
    root,
    from_=5,
    to=150,
    orient="horizontal",
    bootstyle=INFO,
    length=400,
)
difficulty_slider.set(25)
difficulty_slider.pack(pady=20)

# Add canvas to draw the maze
canvas = tk.Canvas(root, width=500, height=500, bg="#2C3E50", highlightthickness=0)
canvas.pack(pady=20)

# Run application
root.mainloop()
