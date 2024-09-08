import tkinter as tk
from tkinter import PhotoImage

from reader import Reader
from solver import Solver
from camera import Camera
from mouse import Mouse
from numpy.random import shuffle

import threading
import time

class Agent:
    READY = 1
    RUNNING = 2
    NUM_DOT = 8
    TEXT_FONT = 'Android Assassin'

    BG_COLOR = '#060D10'
    TEXT_COLOR = '#87DF2C'
    SELECTED_COLOR = '#27403E'

    def __init__(self):
        self.screen = tk.Tk()
        self.screen.title('Sudoku Solver')
        self.screen.geometry(f'385x320')
        self.screen.config(bg=Agent.BG_COLOR)
        self.screen.bind('<KeyPress>', self.handle_key_board)
        self.screen.attributes('-topmost', True)

        self.screen.iconphoto(False, PhotoImage(file='image\\maze_cornea.png'))
    

        self.agent_button = tk.Button(self.screen, text='Start', font = (Agent.TEXT_FONT, 19), bg = Agent.BG_COLOR, bd = 2, relief='ridge', fg=Agent.TEXT_COLOR,)
        self.agent_button.place(x = 15, y = 20, width=290, height=80)
        self.agent_button.config(command=self.call_agent)
        self.state = Agent.READY

        self.button_size9 = tk.Button(self.screen, text='9x9', font = (Agent.TEXT_FONT, 8), bg = Agent.BG_COLOR, bd = 2, relief='ridge', fg=Agent.TEXT_COLOR)
        self.button_size9.config(command = lambda : self.change_grid_size(9))
        self.button_size9.place(x = 320, y = 20, width=50, height=35)

        self.button_size16 = tk.Button(self.screen, text='16x16', font = (Agent.TEXT_FONT, 8), bg = Agent.BG_COLOR, bd = 2, relief='ridge', fg=Agent.TEXT_COLOR)
        self.button_size16.place(x = 320, y = 65, width=50, height=35)
        self.button_size16.config(command = lambda : self.change_grid_size(16))

        self.challenge_button = tk.Button(self.screen, text='Challenge', font = (Agent.TEXT_FONT, 19), bg = Agent.BG_COLOR, bd = 2, relief='ridge', fg=Agent.TEXT_COLOR,)
        self.challenge_button.place(x = 15, y = 120, width=290, height=80)
        self.challenge_button.config(command=self.run_challenge)

        self.battle_button = tk.Button(self.screen, text='Battle', font = (Agent.TEXT_FONT, 19), bg = Agent.BG_COLOR, bd = 2, relief='ridge', fg=Agent.TEXT_COLOR,)
        self.battle_button.place(x = 15, y = 220, width=290, height=80)

        self.button_game_run_10 = tk.Button(self.screen, text='10', font = (Agent.TEXT_FONT, 15), bg = Agent.BG_COLOR, bd = 2, relief='ridge', fg=Agent.TEXT_COLOR)
        self.button_game_run_10.place(x = 320, y = 120, width=50, height=50)

        self.button_game_run_20 = tk.Button(self.screen, text='20', font = (Agent.TEXT_FONT, 12), bg = Agent.BG_COLOR, bd = 2, relief='ridge', fg=Agent.TEXT_COLOR)
        self.button_game_run_20.place(x = 320, y = 185, width=50, height=50)

        self.button_game_run_50 = tk.Button(self.screen, text='50', font = (Agent.TEXT_FONT, 12), bg = Agent.BG_COLOR, bd = 2, relief='ridge', fg=Agent.TEXT_COLOR)
        self.button_game_run_50.place(x = 320, y = 250, width=50, height=50)

        self.change_grid_size(9)

    def challenge_func(self, counter=0):
        if counter == 5:
            return
        
        delay = 500

        if counter==0:
            Mouse.click(1000, 910)
            time.sleep(1)
            Mouse.click(1000, 750)
            time.sleep(3)
            counter = 1
            self.call_agent()
        elif self.state == Agent.READY:
            counter += 1
            delay = 200

            time.sleep(5)


            Mouse.click(950, 450)
            Mouse.click(950, 450)
            time.sleep(3)

            Mouse.click(950, 780)
            Mouse.click(950, 780)
            time.sleep(1.5)

            Mouse.click(1000, 890)
            Mouse.click(1000, 890)
            time.sleep(1)

            Mouse.click(1000, 750)
            time.sleep(5)

            self.call_agent()

        self.screen.after(delay, self.challenge_func, counter)
        

    def run_challenge(self, counter=0):
        threading.Thread(target=self.challenge_func).start()


        # for iter in range(10):
        #     self.call_agent()

        #     Mouse.click(1000, 890)
        #     time.sleep(0.5)

            # Mouse.click(950, 450)
            # time.sleep(0.5)

            # Mouse.click(950, 770)
            # time.sleep(0.5)

            # Mouse.click(1000, 750)
            # time.sleep(0.5)




    def handle_key_board(self, event):
        key = event.keysym.lower()

        if key == 'r':
            self.reset()

    def update_text(self, text):
        self.agent_button.config(text=text)

    def reset(self, text='Start'):
        self.state = Agent.READY
        self.update_text(text)


    def change_grid_size(self, size):
        if self.state != Agent.READY:
            return

        self.button_size9.config(bg=Agent.BG_COLOR)
        self.button_size16.config(bg=Agent.BG_COLOR)

        if size == 9:
            self.button_size9.config(bg=Agent.SELECTED_COLOR)   
        elif size == 16:
            self.button_size16.config(bg=Agent.SELECTED_COLOR)
        
        self.grid_size = size

    def shuffle_cells(self, grid, solution, size):
        digit_cells = []
        alpha_cells = []

        for row in range(size):
            for col in range(size):

                if grid[row][col] != 0:
                    continue
                
                value = solution[row][col]

                if type(value) == str:
                    alpha_cells.append((row, col))
                else: digit_cells.append((row, col))

        shuffle(alpha_cells)
        shuffle(digit_cells)

        return digit_cells + alpha_cells

    def fill(self, grid, solution, start, width):
        size = len(solution)

        number_slide = True
        empty_cells = self.shuffle_cells(grid, solution, size)

        if self.state == Agent.READY:
            return

        for row, col in empty_cells:
            value = solution[row][col]

            if type(value) == int:
                if number_slide == False:
                    Mouse.slide('right', start)
                    number_slide = True
            else:
                if number_slide == True:
                    Mouse.slide('left', start)
                    number_slide = False

            Mouse.click_cell(row, col, start, width)
            Mouse.click_value(value, start)

            if size == 16:
                Mouse.click_value(value, start)

        self.reset()

    def call_tool(self):
        img = Camera.take_screenshort()
        grid, start, width = Reader.read(img, self.grid_size)

        if grid == Reader.CANNOT_DETECT:
            self.reset(text='Try again')
            return

        solution = Solver.solve(grid)

        if solution == False:
            self.reset(text='Try again')
        else:
            self.fill(grid, solution, start, width)


    def running_func(self, counter=0):
        if counter == 0:
            threading.Thread(target=self.call_tool).start()

        if self.state == Agent.RUNNING:
            text = '.  ' * (counter%Agent.NUM_DOT)
            if counter%Agent.NUM_DOT == Agent.NUM_DOT-1:
                text = text[:-2]

            self.update_text(text)
            self.screen.after(200, self.running_func, counter+1)

    def call_agent(self):
        if self.state == Agent.READY:
            self.state = Agent.RUNNING
            threading.Thread(target=self.running_func).start()

    def run(self):
        self.screen.mainloop()

agent_sudoku = Agent()
agent_sudoku.run()