import cv2
import matplotlib.pyplot as plt

image = cv2.imread('image1.png')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# # 16x16
start_x = 695
start_y = 154
width = 33

# 9x9
# start_x = 715
# start_y = 185
# width = 55

# for r in range(16):
#     for c in range(16):
#         x = start_x + c * width
#         y = start_y + r * width
#         cv2.circle(image, (x, y), 10, (0, 0, 255))

start_x = 700
start_y = 850

# 60 for 1->9
# 80 for A->G

for num in range(9):
    x = start_x + num * 60
    y = start_y
    print(x, y)
    cv2.circle(image, (x, y), 10, (0, 0, 255))

plt.imshow(image)
plt.show()

# import time

# def slide():

#     pyautogui.moveTo(1180, 850)

#     pyautogui.mouseDown(button='left')
#     pyautogui.dragTo(600, 850, 0.2)
#     pyautogui.mouseUp(button='left')

# slide()

