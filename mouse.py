import pyautogui


class Mouse:
    @classmethod
    def click_cell(cls, row, col, grid_size):
        if grid_size == 9:
            start_x, start_y, width = 715, 185, 55
        elif grid_size == 16:
            start_x, start_y, width = 695, 154, 33

        target_x = start_x + col * width
        target_y = start_y + row * width 

        pyautogui.click(target_x, target_y)

    @classmethod
    def click_value(cls, value):
        start_x, target_y = 700, 850
        
        if type(value) == int:
            target_x = start_x + value * 60
        else:
            target_x = start_x + (ord(value) - ord('A')) * 80

        pyautogui.click(target_x, target_y)
 
    @classmethod
    def slide(direct):
        if direct == 'left':
            start, target = (1200, 850), (600, 850)
        elif direct == 'right':
            start, target = (680, 850), (1250, 850)

        pyautogui.moveTo(start[0], start[1])

        pyautogui.mouseDown(button='left')
        pyautogui.dragTo(target[0], target[1], 0.2)
        pyautogui.mouseUp(button='left')

    @classmethod
    def fill(cls, row, col, value, grid_size):
        Mouse.click_cell(row, col, grid_size)
        Mouse.click_value(value)

