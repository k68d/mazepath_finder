import tkinter as tk
import time
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



def find_path_dfs(maze, canvas):
    start = "O"
    end = "X"
    start_pos = find_start(maze, start)

    stack = []
    stack.append((start_pos, [start_pos]))

    visited = set()
    step_counter = 0

    while len(stack) > 0:
        current_pos, path = stack.pop()
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
            return path, step_counter

        neighbors = find_neighbors(maze, row, col)
        for neighbor in neighbors:
            if neighbor in visited:
                continue

            r, c = neighbor
            if maze[r][c] == "#":
                continue

            new_path = path + [neighbor]
            stack.append((neighbor, new_path))
            visited.add(neighbor)

        step_counter += 1

def start_algorithm(content):
    maze = read_maze(content)

    canvas = tk.Canvas(root, width=len(maze[0]) * 20, height=len(maze) * 20)
    canvas.delete("all")
    canvas.pack()

    path, step_counter = find_path_dfs(maze, canvas)
    print("Steps:", step_counter)  # You can display this in a label or messagebox if needed

def read_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            start_algorithm(content)

root = tk.Tk()
root.title("Maze solver")
root.geometry("500x500")

start_button = tk.Button(root, text="Select File", command=read_file)
start_button.pack()

root.mainloop()