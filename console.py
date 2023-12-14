import curses
from curses import wrapper
import queue
import time

def read_maze(file_path):
    with open(file_path, 'r') as file:
        maze = [list(line.strip()) for line in file]
    return maze

def print_maze(maze, stdscr, path=[]):
    GREEN = curses.color_pair(1)
    RED = curses.color_pair(2)

    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if(i, j) in path:
                stdscr.addstr(i, j * 2, "X", GREEN)
            else:
                stdscr.addstr(i, j * 2, value, RED)

    stdscr.refresh()

def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j

    return None

def find_path_dfs(maze, stdscr):
    start = "O"
    end = "X"
    start_pos = find_start(maze, start)

    # Create the depth-first search algorithm that also draws the path in console in the maze
    stack = []
    stack.append((start_pos, [start_pos]))

    visited = set()
    step_counter = 0

    while len(stack) > 0:
        current_pos, path = stack.pop()
        row, col = current_pos

        stdscr.clear()
        print_maze(maze, stdscr, path)
        time.sleep(0.2)
        stdscr.refresh()

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

def find_path_bfs(maze, stdscr): # Method that finds the path using the Breadth-First Search algorithm
    start = "O"
    end = "X"
    start_pos = find_start(maze, start)

    q = queue.Queue()
    q.put((start_pos, [start_pos]))

    visited = set()
    step_counter = 0

    while not q.empty():
        current_pos, path = q.get()
        row, col = current_pos

        stdscr.clear()
        print_maze(maze, stdscr, path)
        time.sleep(0.2)
        stdscr.refresh()

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
            q.put((neighbor, new_path))
            visited.add(neighbor)

        step_counter += 1

def find_neighbors(maze, row, col):
    neighbors = []

    # UP
    if row > 0:  
        neighbors.append((row - 1, col))
    # DOWN
    if row + 1 < len(maze):  
        neighbors.append((row + 1, col))
    # LEFT
    if col > 0:  
        neighbors.append((row, col - 1))
    # RIGHT
    if col + 1 < len(maze[0]):  
        neighbors.append((row, col + 1))

    return neighbors


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    file_path = 'C:\\Users\\68\\Desktop\\projects\\mazepath_finder\\maze3.txt'
    maze = read_maze(file_path)
    path, step_counter = find_path_bfs(maze, stdscr)

    stdscr.addstr(len(maze) + 2, 0, f"Steps: {step_counter}", curses.color_pair(1))
    stdscr.refresh()
    stdscr.getch()

wrapper(main)
