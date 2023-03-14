from typing import Union, List, Optional

from src.bdk.block_distribution_id import BlockDistributionId
from src.bdk.ports.port_id import PortId
from src.meow_sim.entity.block.block_entity import BlockEntity
from src.meow_sim.entity.block.block_instance_id import BlockInstanceId
from src.meow_sim.entity.block.port_entity import PortEntity
from src.meow_sim.entity.connection import Connection
from src.meow_sim.entity.graph.simulation_graph import SimulationGraph


class GraphBuilderUtil:
    _g: SimulationGraph

    def __init__(self):
        self._g = SimulationGraph()

    def with_block(
            self, name: str,
            inputs: Optional[List[str]] = None,
            outputs: Optional[List[str]] = None
    ) -> 'GraphBuilderUtil':
        if inputs is None:
            inputs = []
        if outputs is None:
            outputs = []

        self._g.add_block(self._block(name, inputs, outputs))
        return self

    def with_connection(self, name_u: str, port_u: str, name_v: str, port_v) -> 'GraphBuilderUtil':
        block_u = self.get_block(name_u)
        port_u = block_u.get_output(PortId(port_u))
        block_v = self.get_block(name_v)
        port_v = block_v.get_input(PortId(port_v))
        self._g.add_connection(Connection(from_port=port_u, to_port=port_v))

    def build(self) -> SimulationGraph:
        return self._g

    def get_block(self, name: str):
        for block in self._g.blocks:
            if block.name == name:
                return block
        raise KeyError(f"Block with name '{name}' does not exist in graph")

    def _block(self, name: str, inputs: List[str], outputs: List[str]):
        b = BlockEntity(
            distribution_id=BlockDistributionId(f'com.test.{name}'),
            instance_id=BlockInstanceId(f'id_{name}'),
            name=name,
        )
        b.inputs = [PortEntity(block=b, port_id=PortId(port_name)) for port_name in inputs]
        b.outputs = [PortEntity(block=b, port_id=PortId(port_name)) for port_name in outputs]
        return b
