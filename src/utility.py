def is_valid(grid, row, col, num):
    for i in range(9):
        if grid[row][i] == num or grid[i][col] == num:
            return False

    start_row, start_col = 3*(row//3), 3*(col//3)
    for r in range(start_row,start_row + 3):
        for c in range(start_col,start_col + 3):
            if grid[r][c] == num:
                return False
    return True


def is_filled(grid):
    filled = True
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                filled = False

    return filled

def initialize_candidates_grid(grid):
    '''Initializes 9*9 grid of cells listing potential candidates
    that can be validly placed in each.'''
    candidates = [[set() for _ in range(9)] for _ in range(9)]
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                candidates[row][col] = {num for num in range(1, 10) if is_valid(grid, row, col, num)}
    return candidates


def copy_grid(grid):
    return [row.copy() for row in grid]

def get_filled(grid):
    return {(r, c) for r in range(9) for c in range(9) if grid[r][c] != 0}

