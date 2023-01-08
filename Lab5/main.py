from Genetics import GeneticAlgorithm
import matplotlib.pyplot as plt
import numpy as np


gr = GeneticAlgorithm(300, 290)
results = gr.launch_genetic_selection(1000, 16, 15, 20, 0.2)
ypoints = np.array(results[1])
plt.plot(ypoints)
plt.show()
print(f'The best route length: {results[0][0].fitness}')
print(f'The best route: {results[0][0].path}')
