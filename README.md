# Sudoku

This is a Sudoku game/generator built wit Python and Pygame by Jakub Gago. 


Project Structure
-------------------------------------------------------------------------------------------------------

src/

├─ main.py --Entry point and game loop

├─ user_interface.py --Renders menu, grid, handles input events

├─ generator.py --Creates valid puzzles using backtracking algorithm to verify uniqueness

├─ solver.py --Verifies puzzle solvability with human techniques, determines difficulty level

└─ utils.py --Helpers

requirements.txt

README.md   


How To Install
----------------------------------------------------------------------------------------------------------





How To Play
----------------------------------------------------------------------------------------------------
Upon starting the game there is a difficulty selection menu. After choosing any difficulty level and clicking on the start button
the game will start with Sudoku of desired difficulty. Player may use the left-mouse-click + num-keys to fill in solved
numbers and the right-mouse-click + num-keys to pencilmark which candidates are available
for each cell. Filled in numbers can be deleted with backspace/delete, candidates can be removed
by repeating their input process. When the puzzle is successfully solved, a winmessage "SOLVED" will appear on the screen.

To access the menu to change difficulty or generate another puzzle,
press Escape( WARNING!: You WILL NOT be able to access your current puzzle again! ).
