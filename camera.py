import pyautogui
import numpy as np

class Camera:

    @classmethod
    def take_screenshort(cls):
        screenshort = pyautogui.screenshot()
        image =  np.array(screenshort)
        return image