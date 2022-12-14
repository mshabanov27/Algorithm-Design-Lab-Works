# Graph representation of the maze


class Graph:
    def __init__(self, maze):
        self.__graph = self.__generate_graph(maze)
        self.__dead_ends = self.count_dead_ends()

    @property
    def graph(self):
        return self.__graph

    @property
    def dead_ends(self):
        return self.__dead_ends

    def __generate_graph(self, grid):
        tempGraph = {}
        for x, row in enumerate(grid):
            for y, col in enumerate(row):
                if not col:
                    tempGraph[(x, y)] = self.__get_instant_neighbours(grid, x, y)
        return tempGraph


    @staticmethod
    def reconstruct_path(came_from, start, goal):
        current = (1, goal)
        path = [current]
        while current[1] != start:
            current = came_from[current[1]]
            path.append(current)
        path.reverse()
        return path

    @staticmethod
    def __get_instant_neighbours(grid, i, j):
        neighbors = [(1, (i + 1, j)), (1, (i, j + 1)), (1, (i - 1, j)), (1, (i, j - 1))]

        if i == 1 or grid[i - 1][j] == 1:
            neighbors.remove((1, (i - 1, j)))
        if j == 1 or grid[i][j - 1] == 1:
            neighbors.remove((1, (i, j - 1)))
        if i == len(grid) - 2 or grid[i + 1][j] == 1:
            neighbors.remove((1, (i + 1, j)))
        if j == len(grid[i]) - 2 or grid[i][j + 1] == 1:
            neighbors.remove((1, (i, j + 1)))

        return neighbors

    def count_dead_ends(self):
        dead_ends = 0
        for dot in self.__graph:
            if len(self.__graph[dot]) == 1:
                dead_ends += 1

        return dead_ends
