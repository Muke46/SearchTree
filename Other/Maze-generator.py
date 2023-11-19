import random
from PIL import Image

def generate_maze(width, height):
    # Initialize the maze grid
    maze = [[1] * width for _ in range(height)]
    
    # Starting and ending points
    start_x, start_y = 1, 1
    end_x, end_y = width - 2, height - 2
    maze[start_y][start_x] = 0
    maze[end_y][end_x] = 0
    
    # Recursive backtracking to generate the maze
    stack = [(start_x, start_y)]
    while stack:
        x, y = stack[-1]
        neighbors = []
        for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                neighbors.append((nx, ny))
        if neighbors:
            nx, ny = random.choice(neighbors)
            maze[ny][nx] = 0
            maze[y + (ny - y) // 2][x + (nx - x) // 2] = 0
            stack.append((nx, ny))
        else:
            stack.pop()
    
    # Draw the maze as an image
    maze_img = Image.new("RGB", (width, height), "black")
    maze_pixels = maze_img.load()
    for y in range(height):
        for x in range(width):
            if maze[y][x] == 0:
                maze_pixels[x, y] = (255, 255, 255)
    
    # Save the maze as a JPEG image
    maze_img.save("C:\Files\SearchTree\maze_unique_solution.png")

if __name__ == "__main__":
    maze_width = 501
    maze_height = 501
    generate_maze(maze_width, maze_height)
