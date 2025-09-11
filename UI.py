import pygame
import sys
from generator import generate_puzzle


class SudokuGame:
    def __init__(self):
        pygame.init()

        self.WIDTH, self.HEIGHT = 540, 540
        self.CELL_SIZE = 60
        self.BG_COLOR = (255, 255, 255)
        self.LINE_COLOR = (0, 0, 0)
        self.SELECT_COLOR = (250, 220, 100)
        self.FONT = pygame.font.SysFont(None, 40)
        self.CANDIDATE_FONT = pygame.font.SysFont(None, 15)

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Sudoku")
        self.clock = pygame.time.Clock()
        self.state = 'menu'
        self.difficulty = None
        self.menu_buttons = {'Easy': pygame.Rect(70, 200, 120, 50), 'Medium': pygame.Rect(210, 200, 120, 50),
                             'Hard': pygame.Rect(350, 200, 120, 50), 'Start': pygame.Rect(70, 300, 400, 50), }

        self.grid = None
        self.solution = None
        self.solved = None
        self.selected_cell = None
        self.selected_type = None
        self.locked = None
        self.candidates = None

    def draw_menu(self):
        self.screen.fill(self.BG_COLOR)
        title = self.FONT.render('Select Difficulty', True, self.LINE_COLOR)
        self.screen.blit(title, (self.WIDTH // 2 - title.get_width() // 2, 100))
        for text, rect in self.menu_buttons.items():
            color = self.SELECT_COLOR if text == self.difficulty else (200, 200, 200)
            pygame.draw.rect(self.screen, color, rect)
            label = self.FONT.render(text, True, self.LINE_COLOR)
            self.screen.blit(label, (
                rect.x + rect.width // 2 - label.get_width() // 2,
                rect.y + rect.height // 2 - label.get_height() // 2
            ))

    def get_locked(self):
        return {(r, c) for r in range(9) for c in range(9) if self.grid[r][c] != 0}

    def draw_grid(self):
        self.screen.fill(self.BG_COLOR)
        for i in range(9 + 1):
            thickness = 4 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, self.LINE_COLOR, (0, i * self.CELL_SIZE), (self.WIDTH, i * self.CELL_SIZE),
                             thickness)
            pygame.draw.line(self.screen, self.LINE_COLOR, (i * self.CELL_SIZE, 0), (i * self.CELL_SIZE, self.HEIGHT),
                             thickness)

    def draw_numbers(self):
        for r in range(9):
            for c in range(9):
                num = self.grid[r][c]
                if num != 0:
                    color = (0, 0, 0) if (r, c) in self.locked else (0, 0, 200)
                    text = self.FONT.render(str(num), True, color)
                    self.screen.blit(text, (c * self.CELL_SIZE + 24, r * self.CELL_SIZE + 20))

    def draw_candidates(self):
        for r in range(9):
            for c in range(9):
                num = self.grid[r][c]
                if num == 0:
                    color = (0, 0, 0)
                    for candidate in self.candidates[(r, c)]:
                        text = self.CANDIDATE_FONT.render(str(candidate), True, color)
                        self.screen.blit(text, (c * self.CELL_SIZE + 10 + ((candidate - 1) % 3) * 20,
                                                r * self.CELL_SIZE + 10 + ((candidate - 1) // 3) * 20))

    def draw_selected_cell(self):
        if self.selected_cell:
            r, c = self.selected_cell
            pygame.draw.rect(self.screen, self.SELECT_COLOR,
                             (c * self.CELL_SIZE, r * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))

    def draw_winscreen(self):
        color = (200, 200, 200)
        pygame.draw.rect(self.screen, color, (200, 200, 150, 60))
        win_text = self.FONT.render('SOLVED', True, self.LINE_COLOR)
        self.screen.blit(win_text, (220,
                                    220))

    def playing_display(self):
        self.draw_grid()
        self.draw_selected_cell()
        self.draw_numbers()
        self.draw_candidates()
        if self.solved:
            self.draw_winscreen()

    def mouse_click_menu(self, pos):
        for text, rect in self.menu_buttons.items():
            if rect.collidepoint(pos):
                if text in ('Easy', 'Medium', 'Hard'):
                    self.difficulty = text
                elif text == 'Start':
                    if self.difficulty:
                        self.grid, self.solution = generate_puzzle(self.difficulty)
                        self.locked = self.get_locked()
                        self.state = 'playing'
                        self.solved = False
                        self.candidates = {(r, c): set() for r in range(9) for c in range(9)}

    def mouse_click_playing(self, key, pos):
        x, y = pos
        r, c = y // self.CELL_SIZE, x // self.CELL_SIZE
        if (r, c) not in self.locked:
            if key == 1:
                self.selected_cell = (r, c)
                self.selected_type = 1
            if key == 3:
                self.selected_cell = (r, c)
                self.selected_type = 2

    def handle_key_press(self, key, unicode):
        if key == pygame.K_ESCAPE:
            self.state = 'menu'

        elif self.selected_cell:
            r, c = self.selected_cell
            if key in [pygame.K_BACKSPACE, pygame.K_DELETE]:
                self.grid[r][c] = 0

            elif unicode in '123456789':
                num = int(unicode)
                if self.selected_type == 1:
                    self.grid[r][c] = num
                    if self.grid == self.solution:
                        self.solved = True
                else:
                    if num in self.candidates[(r, c)]:
                        self.candidates[(r, c)].remove(num)
                    else:
                        self.candidates[(r, c)].add(num)

    def run(self):
        running = True
        while running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == 'menu':
                        self.mouse_click_menu(pygame.mouse.get_pos())
                    else:
                        self.mouse_click_playing(event.button, pygame.mouse.get_pos())
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_press(event.key, event.unicode)

            if self.state == 'menu':
                self.draw_menu()

            else:
                self.playing_display()
            pygame.display.flip()

        pygame.quit()
        sys.exit()
