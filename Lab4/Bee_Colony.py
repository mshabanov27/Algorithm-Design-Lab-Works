from random import random
import random


class BeeColony:
    def __init__(self, graph_obj, graph_size):
        self.__graph = graph_obj
        self.__available_vertexes = [*range(graph_size)]
        self.__available_colors = ['red', 'blue', 'green', 'purple', 'yellow', 'pink', 'black',
                                   'white', 'grey', 'brown', 'cyan', 'magenta', 'coral', 'olive',
                                   'teal', 'lavender', 'lime', 'beige', 'mint', 'maroon', 'silver', 'heather',
                                   'iris', 'plum', 'jam', 'lilac', 'vine', 'grape', 'orchid', 'chiffon']
        self.__used_colors = []

    def scout_bee_work(self):
        if len(self.__available_vertexes) > 2:
            best_nodes = random.sample(self.__available_vertexes, 2)
            if self.__graph.adjacency_matrix[best_nodes[0]].count(1) > self.__graph.adjacency_matrix[best_nodes[1]].count(1):
                return best_nodes[0]
            else:
                return best_nodes[1]
        else:
            return self.__available_vertexes[0]

    def onlooker_bee_work(self, best_node):
        self.__color_node(best_node)
        self.__color_neighbors(best_node)
        self.__available_vertexes.remove(best_node)

    def __color_node(self, best_node):
        color_iter = 0
        self.__graph.colors[best_node] = [self.__available_colors[color_iter], 0]
        while self.__check_same_color(self.__available_colors[color_iter], best_node):
            color_iter += 1
            self.__graph.colors[best_node] = [self.__available_colors[color_iter], 0]
        if not self.__available_colors[color_iter] in self.__used_colors:
            self.__used_colors.append(self.__available_colors[color_iter])

    def __color_neighbors(self, best_node):
        color_iter = 0
        for i in range(len(self.__graph.adjacency_matrix[best_node])):
            if self.__graph.adjacency_matrix[best_node][i] == 1 and self.__graph.colors[i][1] != 0:
                self.__graph.colors[i][0] = self.__available_colors[color_iter]
                while self.__check_same_color(self.__graph.colors[i][0], i):
                    color_iter += 1
                    self.__graph.colors[i][0] = self.__available_colors[color_iter]
                if not self.__available_colors[color_iter] in self.__used_colors:
                    self.__used_colors.append(self.__available_colors[color_iter])
            color_iter = 0

    def __check_same_color(self, color, node):
        for i in range(len(self.__graph.adjacency_matrix[node])):
            if self.__graph.adjacency_matrix[node][i] == 1 and self.__graph.colors[i][0] == color:
                return True
        return False

    @property
    def available_vertexes(self):
        return self.__available_vertexes

    @property
    def used_colors(self):
        return self.__used_colors
