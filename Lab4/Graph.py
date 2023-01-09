from random import random


class Graph:
    def __init__(self, size, max_edges):
        self.__adjacency_matrix = self.__generate_random_graph(size, max_edges)
        self.colors = self.__set_colours()

    def __generate_random_graph(self, size, max_edges):
        matrix = []
        for i in range(size):
            matrix.append([])

        for i in matrix:
            for j in range(size):
                i.append(0)

        for i in range(size):
            the_ones = round(random() * (max_edges - 1) + 1)
            while matrix[i].count(1) < the_ones:
                index = round(random() * (size - 1))
                while index == i:
                    index = round(random() * (size - 1))
                matrix[i][index] = 1
                matrix[index][i] = 1
        return matrix

    def __set_colours(self):
        colors = {}
        for i in range(len(self.__adjacency_matrix)):
            colors[i] = ['NoColour', 1]
        return colors

    @property
    def adjacency_matrix(self):
        return self.__adjacency_matrix
