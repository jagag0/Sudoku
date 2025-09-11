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

def copy_grid(grid):
    return [row.copy() for row in grid]
