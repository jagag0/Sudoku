import copy
from utility import is_valid, is_filled, copy_grid
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

        self.easy_strategies = [(0, self.naked_singles), (0, self.hidden_singles)]
        self.medium_strategies = self.easy_strategies + [(1, self.naked_pairs), (2, self.hidden_pairs),
                           (2, self.naked_triples), (3, self.hidden_triples),
                           (2, self.locked_candidates_pointing), (2, self.locked_candidates_claiming)]

    def initialize_candidates_grid(self):
        '''Initializes 9*9 grid of cells listing potential candidates
        that can be validly placed in each.'''
        candidates = [[set() for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    candidates[row][col] = {num for num in range(1, 10) if is_valid(self.grid, row, col, num)}
        self.candidates_grid = candidates

    def basic_update(self, row, col, num):
        '''Updates the grid of candidates after cell was filled - row,column and box.'''
        for i in range(9):
            self.candidates_grid[row][i].discard(num)
            self.candidates_grid[i][col].discard(num)

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                self.candidates_grid[r][c].discard(num)

    def naked_singles(self):
        '''Finds cells where only one candidate is available
         and fills them in.'''
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0 and len(self.candidates_grid[row][col]) == 1:
                    num = self.candidates_grid[row][col].pop()
                    self.grid[row][col] = num
                    self.basic_update(row, col, num)
                    return True
        return False

    def hidden_singles(self):
        '''Finds candidates that appear in only one cell
         in a unit(row,column,box) and fills them in.'''
        for unit in self.units:
            possible_positions = {num: [] for num in range(1, 10)}
            for row, col in unit:
                if self.grid[row][col] != 0:
                    continue
                for candidate in self.candidates_grid[row][col]:
                    possible_positions[candidate].append((row, col))
                    
            for num, positions in possible_positions.items():
                if len(positions) == 1:
                    row, col = positions[0]
                    self.grid[row][col] = num
                    self.candidates_grid[row][col].clear()
                    self.basic_update(row, col, num)
                    return True
                    
        return False

    def naked_pairs(self):
        '''Finds two cells in a unit that have only the same two candidates and
         removes those candidates from other cells in the unit.'''
        progress = False
        for unit in self.units:
            pair_map = {}
            for row, col in unit:
                if len(self.candidates_grid[row][col]) == 2:
                    pair = tuple(sorted(self.candidates_grid[row][col]))
                    if pair not in pair_map:
                        pair_map[pair] = []
                    pair_map[pair].append((row, col))

            for pair, cells in pair_map.items():
                if len(cells) == 2:
                    num1, num2 = pair
                    for row, col in unit:
                        if (row, col) not in cells:
                            old = self.candidates_grid[row][col].copy()
                            self.candidates_grid[row][col].discard(num1)
                            self.candidates_grid[row][col].discard(num2)
                            if self.candidates_grid[row][col] != old:
                                progress = True
                    if progress:
                        return True
        return False

    def hidden_pairs(self):
        '''Finds two candidates that are only in the same two cells in a unit and
        removes other candidates those cells.'''
        for unit in self.units:
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
                            self.candidates_grid[row1][col1] = {num1, num2}
                            self.candidates_grid[row2][col2] = {num1, num2}
                            return True
        return False

    def naked_triples(self):
        '''Finds three cells in a unit that share the same three candidates and
        removes those candidates from other cells in the unit.'''
        progress = False
        for unit in self.units:
            unsolved = [(row, col) for row, col in unit if 3 >= len(self.candidates_grid[row][col]) > 1]
            for triple in combinations(unsolved, 3):
                union = set.union(*(self.candidates_grid[row][col] for row, col in triple))
                if len(union) == 3:
                    for row, col in unit:
                        if (row, col) not in triple:
                            if union.intersection(self.candidates_grid[row][col]):
                                progress = True
                                self.candidates_grid[row][col] -= union
                    if progress:
                        return True

        return False

    def hidden_triples(self):
        '''Finds three candidates that are only in the same three cells 
        in a unit and removes other candidates those cells.'''
        progress = False
        for unit in self.units:
            number_positions = {num: [] for num in range(1, 10)}
            for row, col in unit:
                for num in self.candidates_grid[row][col]:
                    number_positions[num].append((row, col))

            for a,b,c in combinations(range(1, 10), 3):
                if not (2 <= len(number_positions[a]) <= 3): continue
                if not (2 <= len(number_positions[b]) <= 3): continue
                if not (2 <= len(number_positions[c]) <= 3): continue
                shared_cells = (set(number_positions[a]) & set(number_positions[b]) & set(number_positions[c]))
                if len(shared_cells) == 3:
                    for row, col in shared_cells:
                        extras = self.candidates_grid[row][col] - set([a,b,c])
                        if extras:
                            progress = True
                            self.candidates_grid[row][col] -= extras
                    if progress:
                        return True

        return False

    def locked_candidates_pointing(self):
        ''' Checks positions of candidate in every box unit,
         if a candidate is in only one row/col removes the 
         candidate from cells inside the row/col and outside the box unit. '''
        progress = False
        for box in self.boxes:
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
                        return True

                cols = {col for _, col in positions}
                if len(cols) == 1:
                    col = cols.pop()
                    for row in range(9):
                        if (row, col) not in box and num in self.candidates_grid[row][col]:
                            self.candidates_grid[row][col].remove(num)
                            progress = True

                    if progress:
                        return True
        return False

    def locked_candidates_claiming(self):
        ''' Checks candidate positions in every row/col, if candidate positions
        in a row/col are only in one box unit removes the candidate from
        cells inside the box unit and outside the row/col'''
        progress = False
        for unit in self.rows + self.columns:
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
                        return True
        return False


def is_easy(puzzle):
    sudoku = Sudoku()
    backup = copy_grid(puzzle)
    sudoku.grid = backup
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

def is_medium(puzzle):
    sudoku = Sudoku()
    backup = copy_grid(puzzle)
    sudoku.grid = backup
    sudoku.initialize_candidates_grid()
    rating = 0

    progress = True
    while progress:
        progress = False
        for score, strategy in sudoku.medium_strategies:
            if strategy():
                rating += score
                progress = True
                break

    if is_filled(sudoku.grid):
        if 2 <= rating <= 10:
            return True
    return False





