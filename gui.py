import tkinter as tk
import time
import queue
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

def read_maze(content):
    return [list(line.strip()) for line in content.split('\n')]

def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j
    return None

def find_neighbors(maze, row, col):
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))
    if row + 1 < len(maze):
        neighbors.append((row + 1, col))
    if col > 0:
        neighbors.append((row, col - 1))
    if col + 1 < len(maze[0]):
        neighbors.append((row, col + 1))
    return neighbors

import tkinter as tk
from tkinter import filedialog
import time
import queue

# ... (previous code remains the same)

def find_path(maze, canvas, algorithm, step_label):
    start = "O"
    end = "X"
    start_pos = find_start(maze, start)

    if algorithm == "DFS":
        stack = [(start_pos, [start_pos])]
        data_structure = stack
    elif algorithm == "BFS":
        queue_obj = queue.Queue()
        queue_obj.put((start_pos, [start_pos]))
        data_structure = queue_obj

    visited = set()
    step_counter = 0

    while data_structure:
        if algorithm == "DFS":
            current_pos, path = data_structure.pop()
        elif algorithm == "BFS":
            current_pos, path = data_structure.get()

        row, col = current_pos

        canvas.delete("all")
        for i, row_vals in enumerate(maze):
            for j, value in enumerate(row_vals):
                color = "red" if value == "#" else "white"
                canvas.create_rectangle(j * 20, i * 20, (j + 1) * 20, (i + 1) * 20, fill=color)
                if (i, j) in path:
                    canvas.create_text((j * 20) + 10, (i * 20) + 10, text="X", fill="green")
        
        canvas.update()
        time.sleep(0.2)

        if maze[row][col] == end:
            step_label.config(text=f"{algorithm} Steps: {step_counter}")
            return path, step_counter
        
        neighbors = find_neighbors(maze, row, col)
        for neighbor in neighbors:
            if neighbor in visited:
                continue

            r, c = neighbor
            if maze[r][c] == "#":
                continue

            new_path = path + [neighbor]
            data_structure.put((neighbor, new_path)) if algorithm == "BFS" else data_structure.append((neighbor, new_path))
            visited.add(neighbor)
        
        step_counter += 1

def start_algorithm(content, canvas, algorithm, step_label):
    canvas.delete("all")  # Clear canvas before starting a new maze drawing
    maze = read_maze(content)
    path, step_counter = find_path(maze, canvas, algorithm, step_label)

def read_file(canvas, algorithm, step_label):
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            start_algorithm(content, canvas, algorithm, step_label)

root = tk.Tk()
root.title("Maze Solver")
root.geometry("500x550")  # Increased height to accommodate the step label

canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

step_label = tk.Label(root, text="", fg="black")
step_label.pack()

dfs_button = tk.Button(root, text="Select File (DFS)", command=lambda: read_file(canvas, "DFS", step_label))
dfs_button.pack()

bfs_button = tk.Button(root, text="Select File (BFS)", command=lambda: read_file(canvas, "BFS", step_label))
bfs_button.pack()

root.mainloop()
