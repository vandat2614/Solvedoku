from copy import deepcopy

class Solver:
    c2i = {chr(ord('A') + i) : 10+i for i in range(7)}
    i2c = {i : c for c,i in c2i.items()}

    @classmethod
    def mapping(cls, grid, i2c=True):
        grid_size = len(grid)
        result = deepcopy(grid)

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
    def get_solution(cls, grid):
        solution = deepcopy(grid)
        Solver.mapping(solution, i2c=False)

        if not Solver.solve(solution, len(grid)):
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
    def solve(cls, grid, grid_size, row=0, col=0):
        if row == grid_size - 1 and col == grid_size:
            return True
        
        if col == grid_size:
            row += 1
            col = 0

        if grid[row][col] > 0:
            return Solver.solve(grid, grid_size, row, col+1)

        for num in range(1, grid_size+1):
            if Solver.is_safe(grid, row, col, grid_size, num):
                grid[row][col] = num

                if Solver.solve(grid, grid_size, row, col+1):
                    return True
            
            grid[row][col] = 0

        return False


grid = [
    [0, 'B', 'C', 'E', 0, 'D', 2, 0, 0, 3, 0, 0, 0, 4, 7, 0],
    [0, 'D', 0, 0, 5, 0, 0, 'G', 0, 4, 7, 0, 0, 1, 0, 'E'],
    ['A', 3, 0, 0, 9, 1, 0, 0, 0, 0, 0, 'E', 6, 'F', 0, 0],
    [9, 4, 0, 0, 7, 'E', 0, 'F', 'A', 0, 0, 0, 3, 0, 5, 0],
    [0, 2, 0, 'B', 1, 0, 0, 'C', 0, 0, 0, 3, 0, 'A', 'D', 0],
    ['G', 'C', 6, 4, 'B', 0, 0, 5, 'D', 'F', 9, 'A', 7, 0, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 'A', 0, 0, 'G', 4, 0, 0, 9, 'F'],
    ['D', 9, 0, 'A', 0, 0, 0, 0, 0, 1, 0, 7, 4, 8, 0, 'B'],
    [0, 'G', 0, 0, 0, 'F', 0, 0, 3, 'D', 2, 0, 5, 'C', 6, 'A'],
    [3, 6, 4, 0, 8, 0, 'A', 'D', 0, 0, 1, 0, 0, 0, 'G', 2],
    [8, 0, 2, 5, 0, 'B', 6, 0, 'G', 'E', 'A', 'C', 0, 0, 0, 0],
    [7, 0, 'F', 'D', 0, 0, 'G', 'E', 0, 9, 5, 0, 0, 0, 0, 0],
    [0, 0, 0, 6, 'C', 4, 'E', 0, 9, 0, 8, 2, 0, 5, 'A', 3],
    [0, 0, 0, 1, 0, 6, 0, 'B', 0, 0, 0, 5, 8, 2, 'C', 'G'],
    [2, 0, 0, 0, 'F', 'G', 0, 0, 0, 0, 4, 0, 0, 'D', 1, 0],
    ['C', 'F', 3, 'G', 0, 8, 5, 0, 'E', 7, 0, 0, 'B', 9, 4, 0]
]

for r in Solver.get_solution(grid):
    print(r)