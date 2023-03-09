import matplotlib.pyplot as plt
import networkx as nx

from src.meow_sim.repository.block_adapter.block_adapter import BlockAdapter


class SimulationGraph:
    _g: nx.DiGraph

    def __init__(self):
        self._g = nx.DiGraph()

    def add_block(self, block: BlockAdapter):
        self._g.add_node(block.id, block=block)
        pass

    def get_view(self) -> nx.Graph:
        return self._g.copy(as_view=True)

    def plot_graph(self):
        fig, ax = plt.subplots()
        nx.draw_networkx(
            self._g,
            None,
            ax,
            with_labels=True
        )
        plt.show()
