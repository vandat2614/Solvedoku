import cv2
import matplotlib.pyplot as plt

img1 = cv2.imread('grid_image\img_3_1.png', cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('grid_image\img_battle.png', cv2.IMREAD_GRAYSCALE)


start_x, start_y, width = 735, 212, 52

draw1 = img1.copy()
draw2 = img2.copy()

for row in range(9):
    for col in range(9):
        x = start_x + col * width
        y = start_y + row * width

        cv2.circle(draw1, (x, y), 5, (0, 255, 0), 3)
        cv2.circle(draw2, (x, y), 5, (0, 255, 0), 3)


plt.imshow(draw1)
# plt.imshow(draw2)
# plt.axis('off')

plt.show()