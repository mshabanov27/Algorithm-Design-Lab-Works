from AlgorithmLauncher import AlgorithmLauncher
from InputReceiver import InputReceiver

graph_size = InputReceiver.receive_graph_size()
max_edges = InputReceiver.receive_number_input(graph_size)
AlgorithmLauncher.start_bee_colony(graph_size, max_edges)
