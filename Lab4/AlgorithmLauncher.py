import copy
from Bee_Colony import BeeColony
from Graph import Graph


class AlgorithmLauncher:
    @staticmethod
    def start_bee_colony(graph_size, max_edges):
        graph = Graph(graph_size, max_edges)
        results = []
        plot_values = []
        for i in range(1000):
            bee_colony = BeeColony(copy.deepcopy(graph), graph_size)

            while bee_colony.available_vertexes:
                best_node = bee_colony.scout_bee_work()
                bee_colony.onlooker_bee_work(best_node)
            results.append(bee_colony.used_colors)
            plot_values.append(len(AlgorithmLauncher.__get_best_result(results)))

            if i % 20 == 0:
                print(results[i])

        best_result = AlgorithmLauncher.__get_best_result(results)
        print(f'Used colors: {best_result}; Chromatic number is {len(best_result)}')

    @staticmethod
    def __get_best_result(lst):
        minimum = lst[0]
        for i in lst:
            if len(i) < len(minimum):
                minimum = i
        return minimum
