import pyautogui

class Mouse:
    @classmethod
    def click_cell(cls, row, col, start, width):
        start_x = start[0] + 20
        start_y = start[1] + 20

        target_x = start_x + col * width
        target_y = start_y + row * width 

        pyautogui.click(target_x, target_y)

    @classmethod
    def click_value(cls, value, start):
        target_x, target_y = Mouse.compute_pos(value, start)

        pyautogui.click(target_x, target_y)

    @classmethod
    def compute_pos(cls, value, start):
        start_x, target_y = start[0] + 5, 850

        if type(value) == int:
            target_x = start_x + (value-1) * 60
        else:
            target_x = start_x + (ord(value) - ord('A')) * 80

        return target_x, target_y

 
    @classmethod
    def slide(cls, direct, start):
        target_y = 850
        if direct == 'left':
            value_9_pos = Mouse.compute_pos(9, start)
            value_1_pos = Mouse.compute_pos(1, start)

            start = value_9_pos
            target = (value_1_pos[0] - 120, value_1_pos[1])

        elif direct == 'right':
            value_G_pos = Mouse.compute_pos('G', start)
            value_A_pos = Mouse.compute_pos('A', start)

            start = value_A_pos
            target = (value_G_pos[0] + 120, value_G_pos[1])
        pyautogui.moveTo(start[0], start[1])

        pyautogui.mouseDown(button='left')
        pyautogui.dragTo(target[0], target[1], 0.2)
        # pyautogui.mouseUp(button='left')

    @classmethod
    def fill(cls, start, row, col, value, grid_size):
        Mouse.click_cell(row, col, grid_size)
        Mouse.click_value(value, start)

