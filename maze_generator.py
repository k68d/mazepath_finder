import random
from collections import deque

class MazeGenerator:
    @staticmethod
    def generate_random_maze(width, height):
        while True:
            maze = [["#" if x == 0 or x == width - 1 or y == 0 or y == height - 1 else " " for x in range(width)] for y in range(height)]

            # Place 'O' at the top
            start_x = 1
            maze[0][start_x] = "O"

            # Place 'X' at the bottom
            end_x = width - 2
            maze[height - 1][end_x] = "X"

            # Generate random walls and paths with increased density
            for y in range(1, height - 1):
                for x in range(1, width - 1):
                    if random.random() < 0.5 and not ((x, y) == (start_x, 1) and maze[0][start_x] == "#") and not ((x, y) == (end_x, height - 2) and maze[height - 1][end_x] == "#"):
                        maze[y][x] = "#"

            # Check if the maze is solvable
            if MazeGenerator.is_maze_solvable(maze, (start_x, 0), (end_x, height - 1)):
                return maze

    @staticmethod
    def export_maze_to_file(maze, filename):
        with open(filename, 'w') as f:
            for row in maze:
                f.write(''.join(row) + '\n')

    @staticmethod
    def is_valid(x, y, width, height):
        return 0 <= x < width and 0 <= y < height

    @staticmethod
    def is_maze_solvable(maze, start, end):
        queue = deque([start])
        visited = set()
        visited.add(start)

        while queue:
            current = queue.popleft()

            if current == end:
                return True

            x, y = current
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if MazeGenerator.is_valid(new_x, new_y, len(maze[0]), len(maze)) and maze[new_y][new_x] != "#" and (new_x, new_y) not in visited:
                    queue.append((new_x, new_y))
                    visited.add((new_x, new_y))

        return False