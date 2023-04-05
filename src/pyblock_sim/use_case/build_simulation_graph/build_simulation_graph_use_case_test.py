
class TestBuildGraphFromSpec:
    pass
    # TODO: write tests
    #
    # class MockBlockRepository(IBlockRepository):
    #     blocks: List[Tuple[BlockDistributionId, IBlockRuntime]]
    #
    #     def list_blocks(self) -> List[BlockDistributionId]:
    #         b = []
    #         for (block_id, _) in self.blocks:
    #             b.append(block_id)
    #         return b
    #
    #     def get_runtime(self, distribution_id: BlockDistributionId) -> IBlockRuntime:
    #         for (block_id, runtime) in self.blocks:
    #             if block_id == distribution_id:
    #                 return runtime
    #         raise KeyError()
    #
    #
    # def test_ok(self):
    #     block_repo = TestBuildGraphFromSpec.MockBlockRepository()
    #     use_cases = SimulationUseCases(
    #         signal_repository=SignalRepository(),
    #         block_repository=block_repo
    #     )
    #     block_repo.blocks = [
    #         (BlockDistributionId('block_1'), BlockRuntime())
    #     ]
    #
    #   def test_block_missing_in_block_repository(self):
    #       pass
    #
    #   def test_ports_in_spec_dont_exist_in_blocks(self):
    #       pass
    #
    #   def test_spec_has_repeated_blocks(self):
    #       pass
    #
