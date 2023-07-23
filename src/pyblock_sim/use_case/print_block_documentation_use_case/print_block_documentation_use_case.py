from src.pyblock.block.block_distribution_id import BlockDistributionId
from src.pyblock_sim.repository.block_repository.block_repository import BlockRepository
from src.pyblock_sim.repository.cli.cli import CLI


class PrintBlockDocumentationUseCase:
    _block_repo: BlockRepository
    _cli: CLI

    def __init__(self, block_repo: BlockRepository, cli: CLI):
        self._block_repo = block_repo
        self._cli = cli

    def print_block_documentation(self, block: BlockDistributionId):
        block_runtime = self._block_repo.get_runtime(block)

        info = block_runtime.get_info()
        inputs = block_runtime.list_inputs(None)
        outputs = block_runtime.list_outputs(None)
        params = block_runtime.list_parameters(None)

        doc = '========================= Block Documentation =======================\n\n'
        if info.name is not None:
            doc += f'  Name: {info.name}\n'
        if info.description is not None:
            doc += f'  Description: {info.description}\n'
        doc += f'  Distribution ID: {info.distribution_id}\n'

        doc += '\n## Inputs Ports:\n'
        for inpt in inputs:
            doc += f'- {inpt.port_id}\n'

        doc += '\n## Output Ports:\n'
        for outpt in outputs:
            doc += f'- {outpt.port_id}\n'

        doc += '\n## Parameters:\n'
        for param in params:
            doc += f'- {param.param_id}\n'

        doc = '\n=====================================================================\n'

        self._cli.print(doc)
