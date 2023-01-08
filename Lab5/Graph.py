from random import random


class Graph:
    def __init__(self, size, max_edges):
        self.adjacency_matrix = self.__generate_matrix(size, max_edges)
        self.__print_matrix(self.adjacency_matrix)

    def __generate_matrix(self, size, max_edges):
        matrix = []
        self.__fill_with_infs(matrix, size)

        for i in range(size):
            while matrix[i].count(float('inf')) > size - max_edges:
                index = round(random() * (size - 1))
                while index == i:
                    index = round(random() * (size - 1))
                if random() < 0.5:
                    matrix[i][index] = round(random() * 149 + 5)
                    matrix[index][i] = matrix[i][index]
                else:
                    matrix[i][index] = round(random() * 149 + 5)
        return matrix

    @staticmethod
    def __print_matrix(graph):
        print('Graph adjacency matrix:')
        print('\n'.join([''.join(['{:6}'.format(item) for item in row])
                         for row in graph]))
        print()

    @staticmethod
    def __fill_with_infs(matrix, size):
        for i in range(size):
            matrix.append([])

        for i in matrix:
            for j in range(size):
                i.append(float('inf'))
