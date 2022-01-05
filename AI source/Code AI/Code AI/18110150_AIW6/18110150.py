#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
grid = np.zeros((8, 8), dtype = int)
from random import randint, shuffle, choice
from itertools import permutations


constellations_drawn  = []


def print_grid():
    global grid
    for line in grid:
        for square in line:
            if square == 0:
                print(".", end = " ")
            else :
                print("Q", end = " ")
        print()

solved = []

def prefilled_solved():
    global solved
    new_board = ['1', '2', '3', '4', '5', '6', '7', '8']
    new_board_i = ''.join(new_board)
    solved = permutations(new_board_i, 8)



def solve(y=0):
    global grid
    global solved
    global constellations_drawn
    list_solved = list(solved)
    len_solved = len(list_solved)
    board_drawn = list_solved[randint(0, len_solved-1)]
    board_drawn_str = ''.join(board_drawn)
    while board_drawn_str in constellations_drawn:
        board_drawn = list_solved[randint(0, len_solved - 1)]
    new_board_list = [int(item) for item in board_drawn]
    for i, x in enumerate(new_board_list):
        if grid[i-1][x-1] == 0:
            grid[i-1][x-1] = 1
            #y += 1
            #solve(y)
            #y -= 1 or y = 0 or y -=2
            # backtracking - bad choice
            # grid[y][x] = 0
    constellations_drawn.append(board_drawn_str)
    print_grid()
    print(grid)
    return
    input("More?")

if __name__ == '__main__':
    prefilled_solved()
    solve()

