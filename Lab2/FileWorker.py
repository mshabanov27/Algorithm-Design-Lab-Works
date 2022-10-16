class FileWorker:
    @staticmethod
    def read_grid(filename):
        file = open(filename, 'r')
        grid_str = file.read()
        file.close()
        grid = FileWorker.turn_to_grid(grid_str)
        return grid

    @staticmethod
    def write_grid(filename, grid):
        file = open(filename, 'w')
        file.write(FileWorker.convert_grid_to_str(grid))
        file.close()

    @staticmethod
    def turn_to_grid(grid_str):
        grid_lines = grid_str.split('\n')
        grid = []
        for i, line in enumerate(grid_lines):
            grid.append([])
            for element in str(line):
                grid[i].append(int(element))

        return grid

    @staticmethod
    def convert_grid_to_str(grid):
        grid_str = ''

        for line in grid:
            for element in line:
                grid_str += str(element)
            grid_str += '\n'

        return grid_str