import random
from random import sample
from random import random
from Graph import Graph
from Individual import Individual


class GeneticAlgorithm:
    def __init__(self, size, edges):
        self.graph_size = size
        self.graph = Graph(size, edges)

    def launch_genetic_selection(self, iterations, population_size, crossovers_number, mutations_number, mutation_probability):
        population = self.__generate_population(population_size)
        best_results = [population[0].fitness]
        for i in range(iterations):
            self.__generate_crossovers(crossovers_number, population)
            self.__generate_mutations(mutations_number, mutation_probability, population)
            population.sort()
            population = population[:population_size]
            best_results.append(population[0].fitness)
            if i % 10 == 0:
                print(f'Current best route length: {population[0].fitness}')
        return population, best_results

    def __generate_crossovers(self, crossovers_number, population):
        for j in range(crossovers_number):
            descendants = self.__crossover(population)
            population.append(Individual(self.__local_improvement(descendants[0]), self.graph.adjacency_matrix))
            population.append(Individual(self.__local_improvement(descendants[1]), self.graph.adjacency_matrix))

    def __generate_mutations(self, mutations_number, mutation_probability, population):
        for j in range(mutations_number):
            descendants = self.__crossover(population)
            mutants = [self.__try_mutation(mutation_probability, descendants[0]),
                       self.__try_mutation(mutation_probability, descendants[1])]
            if mutants[0] is not None:
                population.append(Individual(self.__local_improvement(mutants[0]), self.graph.adjacency_matrix))
            elif descendants[0] is not None:
                population.append(Individual(self.__local_improvement(descendants[0]), self.graph.adjacency_matrix))
            if mutants[1] is not None:
                population.append(Individual(self.__local_improvement(mutants[1]), self.graph.adjacency_matrix))
            elif descendants[1] is not None:
                population.append(Individual(self.__local_improvement(descendants[1]), self.graph.adjacency_matrix))

    def __generate_population(self, population_size):
        population = []
        for i in range(population_size - 1):
            population.append(Individual(self.__create_random_path(), self.graph.adjacency_matrix))
        return population

    def __crossover(self, population):
        parents = sample(population, 2)
        breaking_point = round(random() * (len(parents[0]) - 1) + 1)
        first_descendant = parents[0][:breaking_point]
        self.__add_chromosome_part(first_descendant, parents, breaking_point, 1)
        second_descendant = parents[1][:breaking_point]
        self.__add_chromosome_part(second_descendant, parents, breaking_point, 0)
        return first_descendant, second_descendant

    def __try_mutation(self, probability, descendant):
        if random() < probability:
            return self.__start_mutation(descendant)

    @staticmethod
    def __local_improvement(improved):
        i = round(random() * (len(improved) - 2) + 1)
        j = round(random() * (len(improved) - 2) + 1)
        improved[i], improved[j] = improved[j], improved[i]
        return improved

    def __create_random_path(self):
        random_path = [0]
        while len(random_path) <= self.graph_size:
            if len(random_path) == self.graph_size:
                random_path.append(0)
            else:
                temp = round(random() * (self.graph_size - 1))
                if temp not in random_path:
                    random_path.append(temp)
        return random_path

    def __add_chromosome_part(self, descendant, parents, breaking_point, parent_number):
        i = breaking_point
        while i < len(parents[parent_number]):
            if parents[parent_number][i] not in descendant:
                descendant.append(parents[parent_number][i])
            i += 1

        if len(descendant) < len(parents[parent_number]) - 1:
            self.__fill_till_end(descendant, parents, parent_number)
        descendant.append(0)

    @staticmethod
    def __fill_till_end(descendant, parents, parent_number):
        if parent_number == 0:
            another_parent_number = 1
        else:
            another_parent_number = 0
        i = 0
        while i < len(parents[another_parent_number]):
            if parents[another_parent_number][i] not in descendant:
                descendant.append(parents[another_parent_number][i])
            i += 1

    def __check_child(self, descendant):
        matrix = self.graph.adjacency_matrix
        index = 0
        for i in range(len(descendant) - 1):
            if matrix[index][descendant[i + 1]] == float('inf'):
                return False
        return True

    def __start_mutation(self, descendant):
        indexes = sample([*range(1, len(descendant))], 2)
        descendant[indexes[0]], descendant[indexes[1]] = descendant[indexes[1]], descendant[indexes[0]]
        if self.__check_child(descendant):
            return descendant
