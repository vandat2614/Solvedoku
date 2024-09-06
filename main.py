from reader import Reader
from solver import Solver
from camera import Camera
from mouse import Mouse
import time


img = Camera.take_screenshort()
grid, start, width = Reader.read(img)
solution = Solver.solve(grid)
    
size = len(solution)

number_slide = True

for row in range(size):
    for col in range(size):
        value = solution[row][col]

        if grid[row][col] != 0:
            continue

        if type(value) == int:
            if number_slide == False:
                Mouse.slide('right')
                number_slide = True
        else:
            if number_slide == True:
                Mouse.slide('left')
                number_slide = False

        Mouse.click_cell(row, col, start, width)
        Mouse.click_value(value)
        
