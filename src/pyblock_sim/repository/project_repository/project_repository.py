from src.block_library.ltspice_runner.ltspice_runner_config import LTSpiceRunnerConfig
from src.pyblock.block.block_distribution_id import BlockDistributionId
from src.pyblock.block.ports.port_id import PortId
from src.pyblock_sim.entity.block.block_instance_id import BlockInstanceId
from src.pyblock_sim.entity.project.block_specification import BlockSpecification
from src.pyblock_sim.entity.project.connection_specification import ConnectionSpecification
from src.pyblock_sim.entity.project.graph_specification import GraphSpecification
from src.pyblock_sim.entity.project.param_specification import ParamSpecification
from src.pyblock_sim.entity.project.project_entity import ProjectEntity


class ProjectRepository:
    def load(self) -> ProjectEntity:
        return self._create_ltspice_example()

    def _create_ltspice_example(self) -> ProjectEntity:
        project = ProjectEntity()
        project.graph_spec = GraphSpecification(
            blocks=[
                BlockSpecification(
                    dist_id=BlockDistributionId('br.ufmg.optma.signal_generator'),
                    instance_id=BlockInstanceId('sig_gen_1'),
                    name='Signal Generator',
                    params=[]
                ),
                BlockSpecification(
                    dist_id=BlockDistributionId('br.ufmg.optma.ltspice_runner'),
                    instance_id=BlockInstanceId('ltspice_1'),
                    name='LTSpice Integration',
                    params=[
                        ParamSpecification(
                            param_id='config',
                            type=LTSpiceRunnerConfig,
                            value=LTSpiceRunnerConfig(
                                schematic_file='../block_library/ltspice_runner/test_data/Transmissor.asc',
                                file_name_in_circuit='TX_input.txt',
                                add_instructions=[
                                    '; Simulation settings',
                                    '.tran 0 10m 0 1u'
                                ],
                                probe_signals=['I(D1)']
                            )
                        )
                    ]
                )
            ],
            connections=[
                ConnectionSpecification(
                    origin_block=BlockInstanceId('sig_gen_1'),
                    origin_port=PortId('signal_out'),
                    destination_block=BlockInstanceId('ltspice_1'),
                    destination_port=PortId('signal_in')
                )
            ]
        )
        return project
