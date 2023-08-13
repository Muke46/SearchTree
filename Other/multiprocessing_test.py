import multiprocessing
import sys
sys.path.append('C:\Files\SearchTree')
from SearchTree import NPuzzleSearchTree
import random
import time
import pandas as pd
import matplotlib.pyplot as plt
import logging

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def generate_puzzle(n_moves):
    # Create a solved 4x4 grid
    grid = [[4*j+i+1 for i in range(4)] for j in range(4)]
    grid[3][3] = 0  # Replace last element with 0 (blank tile)

    # Shuffle the grid by making random moves
    for _ in range(n_moves):
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
    size = len(grid) #Square grid only
    for row in range(size):
        for col in range(size):
            if grid[row][col]==0: return row, col


algList=['A*', 'BFS', 'DFS', 'GreedyBFS']
statList=["iterations", "time", "expNodes", "maxNodes", "Depth"]
iteractionsLimit=10000

tests = []

def solve_puzzle(alg, puzzle, iteractionsLimit):
        
    tree = NPuzzleSearchTree(puzzle)
    result = tree.find(searchtype=alg, avoidRepeat="path", print_steps=False, iteractionsLimit=iteractionsLimit)

    if result is not None:
        result['Algorithm'] = alg
        del result['path']

    return result

n=4

def main():
    num_iterations = int(63)
    num_processes = multiprocessing.cpu_count()  # Number of CPU cores
    
    start_time = time.time()
    
    tests = []

    for i in range(num_iterations):
        logging.info("Iteration: %d", i)

        puzzle=[]
        n_moves=[]
        for i in range(n):
            m=random.randint(0,100)
            n_moves.append(m)
            puzzle.append(generate_puzzle(m))

        pool = multiprocessing.Pool(processes=num_processes)
        results=[]
        for alg in algList:
            for i in range(4):
                results.append(pool.apply_async(solve_puzzle, args=(alg, puzzle[i], iteractionsLimit)))
        pool.close()
        pool.join()

        for i in range(n):
            print(f'Mosse: {n_moves[i]}', end='')
            for j, alg in enumerate(algList):
                r=results[j+i*n].get()
                if r==None: print('\t-', end='')
                else: 
                    r=r['iterations']
                    print(f'\t{alg} {r}', end='')
            print('\n')

        for result in results:
            tests.append(result.get())

    execution_time = time.time() - start_time

    print("Total execution time: {:.2f} seconds".format(execution_time))
    
    #Save results to file
    import json
    with open('results.json', 'w') as file:
        json.dump(tests, file)

if __name__ == "__main__":
    main()
