from copy import deepcopy

class Solver:
    c2i = {chr(ord('A') + i) : 10+i for i in range(7)}
    i2c = {i : c for c,i in c2i.items()}

    @classmethod
    def mapping(cls, grid, i2c=True):
        grid_size = len(grid)

        for row in range(grid_size):
            for col in range(grid_size):
                key = grid[row][col]
                if i2c:
                    if key in Solver.i2c:
                        grid[row][col] = Solver.i2c[key]
                else:
                    if key in Solver.c2i:
                        grid[row][col] = Solver.c2i[key]

    @classmethod
    def solve(cls, grid):
        solution = deepcopy(grid)
        Solver.mapping(solution, i2c=False)

        if not Solver.solve_(solution, len(grid)):
            return False
        else:
            Solver.mapping(solution, i2c=True)
            return solution

    @classmethod
    def is_safe(self, grid, row, col, grid_size, num):
        for i in range(grid_size):
            if grid[row][i] == num or grid[i][col] == num:
                return False
            
        grid_size_square_root = int(grid_size**.5)
            
        start_row = row - row % grid_size_square_root
        start_col = col - col % grid_size_square_root

        for r in range(grid_size_square_root):
            for c in range(grid_size_square_root):
                if grid[start_row + r][start_col + c] == num:
                    return False
        
        return True

    @classmethod
    def solve_(cls, grid, grid_size, row=0, col=0):
        if row == grid_size - 1 and col == grid_size:
            return True
        
        if col == grid_size:
            row += 1
            col = 0

        if grid[row][col] > 0:
            return Solver.solve_(grid, grid_size, row, col+1)

        for num in range(1, grid_size+1):
            if Solver.is_safe(grid, row, col, grid_size, num):
                grid[row][col] = num

                if Solver.solve_(grid, grid_size, row, col+1):
                    return True
            
            grid[row][col] = 0

        return False