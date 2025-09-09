import copy
import random
import time
from utility import is_valid
from grader import is_easy, is_medium, is_hard


class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.solutions_count = None
        self.empty_cells = None
        self.intended_solution = None

    def fill(self):
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                    random.shuffle(nums)
                    for i in nums:
                        if is_valid(self.grid, row, col, i):
                            self.grid[row][col] = i
                            if self.fill():
                                return True
                            self.grid[row][col] = 0

                    return False
        return True

    def get_empty_cells(self):
        return [(r, c) for r in range(9) for c in range(9) if self.grid[r][c] == 0]

    def solve(self, index):
        if self.solutions_count > 0:
            return

        if index == len(self.empty_cells):
            self.solutions_count += 1
            return

        row, col = self.empty_cells[index]
        for num in range(1, 10):
            if is_valid(self.grid, row, col, num) and num != self.intended_solution[row][col]:
                self.grid[row][col] = num
                self.solve(index + 1)
                self.grid[row][col] = 0

    def uniqueness_check(self):
        copy = [row[:] for row in self.grid]
        self.empty_cells = self.get_empty_cells()
        self.solutions_count = 0
        self.solve(0)
        self.grid = copy
        return self.solutions_count == 0

    def remove_clues_easy(self, target_removal=61):
        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)
        removed = 0

        for row, col in cells:
            if self.grid[row][col] == 0:
                continue
            backup = self.grid[row][col]
            self.grid[row][col] = 0
            if not self.uniqueness_check() or not is_easy(self.grid):
                    self.grid[row][col] = backup
                    continue

            removed += 1
            if removed >= target_removal:
                break

def generate_puzzle(difficulty):
    board = Board()
    board.fill()
    board.intended_solution = copy.deepcopy(board.grid)
    if difficulty == 'Easy':
        board.remove_clues_easy()
    print(*board.intended_solution, sep='\n', end='\n'+'//'+'\n')
    print(*board.grid, sep='\n', end='\n'+'//'+'\n')
    return board.grid



start_time = time.time()
end_time = time.time()
print(f"Runtime: {end_time - start_time:.4f} seconds")