import tkinter as tk
import time
import queue
from tkinter import filedialog
from tkinter import ttk

from maze_generator import MazeGenerator

class GUIapp(tk.Frame):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        canvas = tk.Canvas(self.parent, width=400, height=400)
        canvas.place(relx=0.1, rely=0.1, anchor=tk.NW)

        step_label = tk.Label(self.parent, text="", fg="black")
        step_label.pack()

        self.maze_generator_frame = tk.Frame(self.parent)
        self.maze_generator_frame.pack()

        algorithm_frame = tk.Frame(self.parent)
        algorithm_frame.place(relx=0.5, rely=0.95, anchor="s")

        dfs_button = tk.Button(algorithm_frame, height=3, width=15, background="SkyBlue", text="Depth First Search", command=lambda: self.read_file(canvas, "DFS", step_label))
        dfs_button.pack(side=tk.LEFT, padx=10, pady=10)

        bfs_button = tk.Button(algorithm_frame, height=3, width=15, background="cyan", text="Breadth First Search", command=lambda: self.read_file(canvas, "BFS", step_label))
        bfs_button.pack(side=tk.LEFT, padx=10, pady=10)

        gen_button = tk.Button(algorithm_frame, height=3, width=15, background="cyan", text="Generate Maze", command=self.generate_maze)
        gen_button.pack(side=tk.LEFT, padx=10, pady=10)
    
    def generate_maze(self):
        width = 20
        height = 15
        maze = MazeGenerator.generate_random_maze(width, height)
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            MazeGenerator.export_maze_to_file(maze, filename)
            
    def read_maze(self, content):
        return [list(line.strip()) for line in content.split('\n')]

    def find_start(self, maze, start):
        for i, row in enumerate(maze):
            for j, value in enumerate(row):
                if value == start:
                    return i, j
        return None

    def find_neighbors(self, maze, row, col):
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

    def find_path(self, maze, canvas, algorithm, step_label):
        start = "O"
        end = "X"
        start_pos = self.find_start(maze, start)

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
            
            neighbors = self.find_neighbors(maze, row, col)
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

    def start_algorithm(self, content, canvas, algorithm, step_label):
        canvas.delete("all")  # Clear canvas before starting a new maze drawing
        maze = self.read_maze(content)
        path, step_counter = self.find_path(maze, canvas, algorithm, step_label)

    def read_file(self, canvas, algorithm, step_label):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.start_algorithm(content, canvas, algorithm, step_label)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Maze Solver")
    root.geometry("1000x1000")  # Increased height to accommodate the step label
    root.resizable(False, False)

    app = GUIapp(root)
    app.pack()  # Don't forget to pack the Frame or Grid it as needed

    root.mainloop()