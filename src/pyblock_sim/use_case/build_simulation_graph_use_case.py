from src.pyblock_sim.entity.block.block_entity import BlockEntity
from src.pyblock_sim.entity.graph.connection_entity import ConnectionEntity
from src.pyblock_sim.entity.graph.simulation_graph import SimulationGraph
from src.pyblock_sim.entity.project.graph_specification import GraphSpecification
from src.pyblock_sim.repository.block_repository.interface_block_repository import IBlockRepository


class BuildSimulationGraphUseCase:
    _block_repo: IBlockRepository

    def __init__(self, block_repository: IBlockRepository):
        self._block_repo = block_repository

    def build_simulation_graph(self, graph_spec: GraphSpecification) -> SimulationGraph:
        graph = SimulationGraph()

        self._add_blocks_to_graph(graph, graph_spec)
        self._add_connections_to_graph(graph, graph_spec)

        return graph

    def _add_blocks_to_graph(self, graph: SimulationGraph, graph_spec: GraphSpecification):
        for block_spec in graph_spec.blocks:
            if not self._block_repo.is_block_known(block_spec.dist_id):
                raise RuntimeError(
                    f"The simulation graph can't be created because the block "
                    f"'{block_spec.dist_id}' does not exist in the block library"
                )

            block = BlockEntity(
                distribution_id=block_spec.dist_id,
                instance_id=block_spec.instance_id,
                name=block_spec.name
            )

            runtime = self._block_repo.get_runtime(block_spec.dist_id)
            block.load(runtime)
            block.param_manager.set_user_params(block_spec.params)

            graph.add_block(block)

    def _add_connections_to_graph(self, graph: SimulationGraph, graph_spec: GraphSpecification):
        for conn_spec in graph_spec.connections:
            graph.add_connection(
                ConnectionEntity(
                    origin_block=conn_spec.origin_block,
                    origin_port=conn_spec.origin_port,
                    destination_block=conn_spec.destination_block,
                    destination_port=conn_spec.destination_port
                )
            )
