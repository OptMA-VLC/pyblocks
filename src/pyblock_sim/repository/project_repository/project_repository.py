import json
from pathlib import Path
from typing import Dict, Any, List

from src.pyblock_sim.entity.block.parameter_entity import ParameterEntity
from src.pyblock_sim.entity.project.graph.block_specification import BlockSpecification
from src.pyblock_sim.repository.project_repository.command_parser import CommandParser
from src.pyblock_sim.entity.project.graph.connection_specification import ConnectionSpecification
from src.pyblock_sim.entity.project.graph.graph_specification import GraphSpecification
from src.pyblock_sim.entity.project.port_selector import PortSelector
from src.pyblock_sim.entity.project.project_entity import ProjectEntity
from src.pyblock_sim.entity.project.signal_selector import SignalSelector


class ProjectRepository:
    def parse_project_file(self, path: Path) -> ProjectEntity:
        json_dict = self._load_json(path)

        block_list = self._get_dict_key(
            json_dict, 'blocks',
            "Can't parse the project file because the 'blocks' section does not exist"
        )
        blocks = self._parse_block_list(block_list)

        connections_list = self._get_dict_key(
            json_dict, 'connections',
            "Can't parse the project file because the 'connections' section does not exist"
        )
        connections = self._parse_connections_list(connections_list)

        commands_list = json_dict.get('commands', [])
        commands = []
        for command_dict in commands_list:
            commands.append(CommandParser.parse(command_dict))

        return ProjectEntity(
            graph_spec=GraphSpecification(
                blocks=blocks,
                connections=connections
            ),
            commands=commands
        )

    def _load_json(self, path: Path) -> Dict:
        try:
            with open(path) as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    raise IOError(f"The file '{path.resolve()}' is not a valid JSON file")
        except FileNotFoundError:
            raise FileNotFoundError(f"The requested file {path.resolve()} does not exist")

    def _parse_block_list(self, block_list: List) -> List[BlockSpecification]:
        blocks = []
        for (idx, block_dict) in enumerate(block_list):
            try:
                blocks.append(self._parse_block(block_dict))
            except KeyError as ex:
                raise KeyError(f"Can't parse block {idx + 1} of {len(block_list)}")

        return blocks

    def _parse_block(self, block_dict) -> BlockSpecification:
        instance_id = self._get_dict_key(
            block_dict, 'instance_id',
            f"Block does not have a value for 'instance_id'"
        )
        distribution_id = self._get_dict_key(
            block_dict, 'distribution_id',
            f"Block does not have a value for 'distribution_id'"
        )
        name = block_dict.get('name', instance_id)

        params_list = block_dict.get('parameters', [])
        params = self._parse_params_list(params_list)

        return BlockSpecification(
            instance_id=instance_id,
            dist_id=distribution_id,
            name=name,
            params=params
        )

    def _parse_params_list(self, params_list: List) -> List[ParameterEntity]:
        params = []
        for param in params_list:
            param_id = self._get_dict_key(
                param, 'param_id',
                "Can't parse parameter because it does not contain a 'param_id' value"
            )
            value = self._get_dict_key(
                param, 'value',
                f"Can't parse parameter '{param_id}' because it does not contain a 'value' value"
            )

            params.append(ParameterEntity(param_id=param_id, value=value))

        return params

    def _parse_connections_list(self, connections_list: List) -> List[ConnectionSpecification]:
        connections = []
        for conn in connections_list:
            from_str = self._get_dict_key(
                conn, 'from',
                "Connection does not have a value for 'from'"
            )
            to_str = self._get_dict_key(
                conn, 'to',
                "Connection does not have a valuer for 'to'"
            )

            connections.append(ConnectionSpecification(
                origin=SignalSelector.parse(from_str),
                destination=PortSelector.parse(to_str)
            ))

        return connections

    def _get_dict_key(self, target_dict: Dict, key: str, error_str: str) -> Any:
        try:
            return target_dict[key]
        except KeyError:
            raise KeyError(error_str)

