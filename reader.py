import cv2
import numpy as np
import matplotlib.pyplot as plt

class Reader:
    WIDTH = HEIGHT = 1080
    GRID9_AREA_THRES = 240000
    GRID16_AREA_THRES = 270000

    @classmethod
    def detect(cls, gray_image):
        blur_image = cv2.GaussianBlur(gray_image, (5, 5), 1)
        canny_image = cv2.Canny(blur_image, 75, 75)

        contours, hierachy = cv2.findContours(canny_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        max_contour = max(contours, key = lambda contour : cv2.contourArea(contour))
        max_area = cv2.contourArea(max_contour)

        if max_area >= cls.GRID16_AREA_THRES:
            grid_size = 16
        elif max_area >= cls.GRID9_AREA_THRES:
            grid_size = 9

        peri = cv2.arcLength(max_contour, True)
        approx = cv2.approxPolyDP(max_contour, 0.02*peri, True) # l-t, l-d, r-d, r-t

        return approx, grid_size
    
    @classmethod
    def extract(cls, grid_image, grid_size):
        board = [[0] * grid_size for _ in range(grid_size)]

        grid = np.zeros((grid_size, grid_size), dtype=np.int8)
        _, binary_image = cv2.threshold(grid_image, 127, 255, cv2.THRESH_BINARY)

        if grid_size == 16:
            cell_width = grid_image.shape[0] // grid_size
            offset = [[10, -5], [10, -4]]
        elif grid_size == 9:
            cell_width = 120
            offset = [[10, -10], [10, -10]]

        num = 0
        for row in range(grid_size):
            for col in range(grid_size):
                cell = binary_image[row * cell_width + offset[0][0] : (row + 1) * cell_width + offset[0][1],
                                    col * cell_width + offset[1][0]: (col + 1) * cell_width + offset[1][1]]

                plt.subplot(grid_size, grid_size, num+1)
                plt.imshow(cell, cmap='gray')
                plt.axis('off')
                num += 1
        plt.show()

    @classmethod
    def read(cls, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        approx, grid_size = Reader.detect(gray_image)

        print(approx[0]) # 680, 137 -> 16x16
        # 696, 168 -> 9x9

        points_src = np.float32([approx[0], approx[3], approx[1], approx[2]])
        points_dst = np.float32([[0, 0], [cls.WIDTH, 0], [0, cls.HEIGHT], [cls.WIDTH, cls.HEIGHT]])

        matrix = cv2.getPerspectiveTransform(points_src, points_dst)
        grid_image = cv2.warpPerspective(gray_image, matrix, (cls.WIDTH, cls.HEIGHT))

        Reader.extract(grid_image, grid_size)
    

image = cv2.imread('image9.png')
grid_image = Reader.read(image)

