import sys
sys.path.append('../SearchTree')
from SearchTree import NPuzzleSearchTree
import pyautogui
import time

import random

def generate_puzzle():
    # Create a solved 4x4 grid
    grid = [[4*j+i+1 for i in range(4)] for j in range(4)]
    grid[3][3] = 0  # Replace last element with 0 (blank tile)

    # Shuffle the grid by making random moves
    for _ in range(100):
        possible_moves = []
        row, col = find_blank(grid)
        if row > 0:
            possible_moves.append((row - 1, col))  # Move blank tile up
        if row < 3:
            possible_moves.append((row + 1, col))  # Move blank tile down
        if col > 0:
            possible_moves.append((row, col - 1))  # Move blank tile left
        if col < 3:
            possible_moves.append((row, col + 1))  # Move blank tile right
        new_row, new_col = random.choice(possible_moves)
        grid[row][col], grid[new_row][new_col] = grid[new_row][new_col], grid[row][col]

    # Convert grid to the desired format and return
    return [[grid[i][j] for j in range(4)] for i in range(4)]

def find_blank(grid):
    for i in range(4):
        for j in range(4):
            if grid[i][j] == 0:
                return i, j

# Example usage
puzzle = generate_puzzle()
print(puzzle)


Dict={}

tree = NPuzzleSearchTree(puzzle)

result = tree.find(searchtype='GreedyBFS', avoidRepeat="Tree", stepByStep=False, print_steps=False, iteractionsLimit=50000)
for key,val in result.items():
    if key != "path":
        print(key, end=": ")
        print(val)

tree = NPuzzleSearchTree(puzzle)  
result = tree.find(searchtype='A*', avoidRepeat="Tree", stepByStep=False, print_steps=False, iteractionsLimit=50000)
for key,val in result.items():
    if key != "path":
        print(key, end=": ")
        print(val)
