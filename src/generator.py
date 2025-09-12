import copy
import random
import time
from utility import is_valid
from grader import is_easy, is_medium


class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.cells = [(r, c) for r in range(9) for c in range(9)]
        self.solutions_count = None
        self.empty_cells = None
        self.solution = None

    def fill(self):
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    nums = [a for a in range(1, 10)]
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
            if is_valid(self.grid, row, col, num) and num != self.solution[row][col]:
                self.grid[row][col] = num
                self.solve(index + 1)
                self.grid[row][col] = 0

    def uniqueness_check(self):
        backup = copy.deepcopy(self.grid)
        self.empty_cells = self.get_empty_cells()
        self.solutions_count = 0
        self.solve(0)
        self.grid = backup
        return self.solutions_count == 0

    def remove_clues_easy(self, target_removal):
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

    def remove_clues_medium(self, target_removal,max_tries):
        backup = copy.deepcopy(self.grid)

        for _ in range(max_tries):
            self.grid = copy.deepcopy(backup)
            removed = 0

            for r, c in random.sample(self.cells, 81):
                if self.grid[r][c] == 0:
                    continue

                clue = self.grid[r][c]
                self.grid[r][c] = 0
                if not self.uniqueness_check():
                    self.grid[r][c] = clue
                    continue

                removed += 1
                if removed >= target_removal:
                    if is_medium(self.grid):
                        return True
                    break

        return False


def generate_puzzle(difficulty):
    board = Board()
    board.fill()
    board.solution = copy.deepcopy(board.grid)
    if difficulty == 'Easy':
        board.remove_clues_easy(random.randint(38, 45))
    elif difficulty == 'Medium':
        while not board.remove_clues_medium(random.randint(48, 53), 50):
            board.grid = [[0 for _ in range(9)] for _ in range(9)]
            board.fill()
            board.solution = copy.deepcopy(board.grid)
            
    return board.grid, board.solution
