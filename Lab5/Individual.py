class Individual:
    def __init__(self, path, matrix):
        self.path = path
        self.matrix = matrix
        self.fitness = self.__calculate_fitness()

    def __calculate_fitness(self):
        fitness = 0
        index = 0
        for i in range(len(self.path) - 1):
            fitness += self.matrix[index][self.path[i + 1]]
            index = self.path[i]
        return fitness

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __gt__(self, other):
        return self.fitness > other.fitness

    def __getitem__(self, offset):
        return self.path[offset]

    def __len__(self):
        return len(self.path)

    def __getslice__(self, low, high):
        return Individual(self.path[low:high], self.matrix)
