from copy import deepcopy
from utility import is_valid, is_filled
from itertools import combinations

class Sudoku:
    def __init__(self):
        self.grid = None
        self.candidates_grid = None
        self.rows = [[(row, col) for col in range(9)] for row in range(9)]
        self.columns = [[(row, col) for row in range(9)] for col in range(9)]
        self.boxes = [[(row, col) for row in range(start_row, start_row + 3) for col in range(start_col, start_col + 3)]
                      for start_row in [0, 3, 6] for start_col in [0, 3, 6]]
        self.units = self.rows + self.columns + self.boxes

        self.strategies = [('naked_singles', 0, self.naked_singles), ('hidden_singles', 0, self.hidden_singles),
                           ('naked_pairs', 1, self.naked_pairs), ('hidden_pairs', 1, self.hidden_pairs),
                           ('naked_triples', 1, self.naked_triples), ('hidden_triples', 2, self.hidden_triples),
                           ('locked_candidates_pointing', 3, self.locked_candidates_pointing), ('locked_candidates_claiming', 3, self.locked_candidates_claiming)]

    def initialize_candidates_grid(self):
        candidates = [[set() for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    candidates[row][col] = {num for num in range(1, 10) if is_valid(self.grid, row, col, num)}
        self.candidates_grid = candidates

    def basic_update(self, row, col, num):
        for i in range(9):
            self.candidates_grid[row][i].discard(num)
            self.candidates_grid[i][col].discard(num)

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                self.candidates_grid[r][c].discard(num)

    def naked_singles(self):
        progress = False
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0 and len(self.candidates_grid[row][col]) == 1:
                    progress = True
                    num = self.candidates_grid[row][col].pop()
                    self.grid[row][col] = num
                    self.basic_update(row, col, num)
        return progress

    def hidden_singles(self):
        progress = False
        for unit in self.units:
            possible_positions = {num: [] for num in range(1, 10)}
            for row, col in unit:
                for candidate in self.candidates_grid[row][col]:
                    possible_positions[candidate].append((row, col))
            for num, positions in possible_positions.items():
                if len(positions) == 1:
                    progress = True
                    row, col = positions[0]
                    self.grid[row][col] = num
                    self.basic_update(row, col, num)
        return progress

    def naked_pairs(self):
        progress = False

        for unit in self.units:
            if progress:
                break
            pair_map = {}
            for row, col in unit:
                if len(self.candidates_grid[row][col]) == 2:
                    pair = tuple(sorted(self.candidates_grid[row][col]))
                    if pair not in pair_map:
                        pair_map[pair] = []
                    pair_map[pair].append((row, col))

            for pair, cells in pair_map.items():
                if progress:
                    break
                if len(cells) == 2:
                    num1, num2 = pair
                    for row, col in unit:
                        if (row, col) not in cells:
                            old = self.candidates_grid[row][col].copy()
                            self.candidates_grid[row][col].discard(num1)
                            self.candidates_grid[row][col].discard(num2)
                            if self.candidates_grid[row][col] != old:
                                progress = True
        return progress

    def hidden_pairs(self):
        progress = False

        for unit in self.units:
            if progress:
                break

            number_positions = {num: [] for num in range(1, 10)}
            for row, col in unit:
                for num in self.candidates_grid[row][col]:
                    number_positions[num].append((row, col))

            for num1 in range(1, 9):
                positions1 = number_positions[num1]
                if len(positions1) != 2:
                    continue

                for num2 in range(num1 + 1, 10):
                    positions2 = number_positions[num2]
                    if positions2 == positions1:
                        row1, col1 = positions1[0]
                        row2, col2 = positions1[1]
                        if len(self.candidates_grid[row1][col1]) > 2 or len(self.candidates_grid[row2][col2]) > 2:
                            progress = True
                            self.candidates_grid[row1][col1] = {num1, num2}
                            self.candidates_grid[row2][col2] = {num1, num2}
                            break

        return progress

    def naked_triples(self):
        progress = False

        for unit in self.units:
            if progress:
                break

            unsolved = [(row, col) for row, col in unit if 3 >= len(self.candidates_grid[row][col]) > 1]
            for triple in combinations(unsolved, 3):
                union = set.union(*(self.candidates_grid[row][col] for row, col in triple))
                if len(union) == 3:
                    for row, col in unit:
                        if (row, col) not in triple:
                            if union.intersection(self.candidates_grid[row][col]):
                                progress = True
                                self.candidates_grid[row][col] -= union

        return progress

    def hidden_triples(self):
        progress = False

        for unit in self.units:
            if progress:
                break

            number_positions = {num: [] for num in range(1, 10)}
            for row, col in unit:
                for num in self.candidates_grid[row][col]:
                    number_positions[num].append((row, col))

            for triple in combinations(range(1, 10), 3):
                shared_cells = (set(number_positions[triple[0]]) & set(number_positions[triple[1]]) & set(
                    number_positions[triple[2]]))
                if len(shared_cells) == 3:
                    for row, col in shared_cells:
                        extras = self.candidates_grid[row][col] - set(triple)
                        if extras:
                            progress = True
                            self.candidates_grid[row][col] -= extras

        return progress

    def locked_candidates_pointing(self):
        ''' Checks positions of candidate in every box unit, if a candidate is in
        only one row/col removes the candidate from cells inside the row/col
         and outside the box unit '''
        progress = False

        for box in self.boxes:
            if progress:
                break

            for num in range(1, 10):
                positions = [(row, col) for row, col in box if num in self.candidates_grid[row][col]]
                if not positions:
                    continue

                rows = {row for row, _ in positions}
                if len(rows) == 1:
                    row = rows.pop()
                    for col in range(9):
                        if (row, col) not in box and num in self.candidates_grid[row][col]:
                            self.candidates_grid[row][col].remove(num)
                            progress = True

                if progress:
                    break

                cols = {col for _, col in positions}
                if len(cols) == 1:
                    col = cols.pop()
                    for row in range(9):
                        if (row, col) not in box and num in self.candidates_grid[row][col]:
                            self.candidates_grid[row][col].remove(num)
                            progress = True

                if progress:
                    break

        return progress

    def locked_candidates_claiming(self):
        ''' Checks candidate positions in every row/col, if candidate positions
        in a row/col are only in one box unit removes the candidate from
        cells inside the box unit and outside  the row/col.'''
        progress = False

        for unit in self.rows + self.columns:
            if progress:
                break

            for num in range(1, 10):
                positions = [(row, col) for row, col in unit if num in self.candidates_grid[row][col]]
                if not positions:
                    continue

                boxes = {(row // 3, col // 3) for row, col in positions}
                if len(boxes) == 1:
                    a, b = boxes.pop()
                    for row in range(a * 3, a * 3 + 3):
                        for col in range(b * 3, b * 3 + 3):
                            if (row, col) not in unit and num in self.candidates_grid[row][col]:
                                self.candidates_grid[row][col].remove(num)
                                progress = True
                if progress:
                    break

        return progress


def is_easy(puzzle):
    sudoku = Sudoku()
    copy = deepcopy(puzzle)
    sudoku.grid = copy
    sudoku.initialize_candidates_grid()

    while True:
        if sudoku.naked_singles():
            continue
        if sudoku.hidden_singles():
            continue
        break

    if is_filled(sudoku.grid):
        return True
    return False

def is_medium():
    return

def is_hard():
    return