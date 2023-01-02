import matplotlib.pyplot as plt
import networkx as nx


class SimulationGraph:
    _g: nx.DiGraph

    def __init__(self):
        self._g = nx.DiGraph()
        self._g.add_edge(1, 2)
        self._g.add_edge(1, 3)
        print(self._g)

    def add_block(self):
        pass

    def add_connection(self):
        pass

    def get_graph(self) -> nx.Graph:
        return self._g.copy(as_view=True)

    def plot_graph(self):
        fig, ax = plt.subplots()
        nx.draw(self._g, None, ax, with_labels=True)
        plt.show()

