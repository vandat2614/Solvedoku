import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

class Reader:
    GRID9_AREA_THRES = 200000
    GRID16_AREA_THRES = 270000
    model = tf.keras.models.load_model('train_model\pre_trained_model.h5')

    @classmethod
    def detect(cls, gray_image):
        blur_image = cv2.GaussianBlur(gray_image, (5, 5), 3)
        canny_image = cv2.Canny(blur_image, 50, 50)

        contours, hierachy = cv2.findContours(canny_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        max_contour = max(contours, key = lambda contour : cv2.contourArea(contour))
        max_area = cv2.contourArea(max_contour)

        if max_area >= cls.GRID16_AREA_THRES:
            grid_size = 16
        elif max_area >= cls.GRID9_AREA_THRES:
            grid_size = 9

        peri = cv2.arcLength(max_contour, True)
        approx = cv2.approxPolyDP(max_contour, 0.02*peri, True) # l-t, l-d, r-d, r-t
        width = peri//4//grid_size

        return approx, grid_size, width
    
    @classmethod
    def extract(cls, grid_image, grid_size):
        board = [[0] * grid_size for _ in range(grid_size)]

        grid = np.zeros((grid_size, grid_size), dtype=np.int8)
        _, binary_image = cv2.threshold(grid_image, 127, 255, cv2.THRESH_BINARY)

        if grid_size == 16:
            cell_width = grid_image.shape[0] // grid_size
            offset = [[10, 0], [10, -5]]
            new_size = (64, 64)
        elif grid_size == 9:
            cell_width = 120
            offset = [[10, -8], [8, -7]]
            new_size = (256, 256)

        cells = []
        for row in range(grid_size):
            for col in range(grid_size):
                cell = binary_image[row * cell_width + offset[0][0]: (row + 1) * cell_width + offset[0][1],
                                    col * cell_width + offset[1][0] : (col + 1) * cell_width + offset[1][1]]
                
                cell = cv2.resize(cell, new_size)
                cell_canny = cv2.Canny(cell, 50, 50)

                contours, hierachy = cv2.findContours(cell_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                
                if contours:
                    max_contour = min(contours, key = lambda contour : cv2.contourArea(contour))
                    area = cv2.contourArea(max_contour)

                    peri = cv2.arcLength(max_contour, True)
                    approx = cv2.approxPolyDP(max_contour, 0.02*peri, True)

                    x,y,w,h = cv2.boundingRect(approx)

                    cell = cell[y:y+h, x:x+w]
                    cell = cv2.resize(cell, (64, 64))

                    cells.append(cell)
                else: 
                    cell = cv2.resize(cell, (64, 64))
                    cells.append(cell)


        return cells
    
    @classmethod
    def convert_grid(cls, grid):
        size = len(grid)
        new_grid = [[0] * size for _ in range(size)]

        for row in range(size):
            for col in range(size):
                value = grid[row][col]
                if value >= 10:
                    value = chr(ord('A') - 10 + value)
                new_grid[row][col] = value

        return new_grid

    @classmethod
    def read(cls, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        approx, grid_size, width = Reader.detect(gray_image)

        points_src = np.float32([approx[0], approx[3], approx[1], approx[2]])
        points_dst = np.float32([[0, 0], [1080, 0], [0, 1080], [1080, 1080]])

        matrix = cv2.getPerspectiveTransform(points_src, points_dst)
        grid_image = cv2.warpPerspective(gray_image, matrix, (1080, 1080))

        cells =  Reader.extract(grid_image, grid_size)
        cells = np.array(cells).reshape(-1, 64, 64, 1).astype('float32') / 255.0

        predict = np.argmax(cls.model.predict(cells), axis = 1).reshape(grid_size, grid_size)
        grid = Reader.convert_grid(predict)

        return grid, approx[0][0], width
