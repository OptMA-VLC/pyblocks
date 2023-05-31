from src.block_library.basic.csv_reader.block import CsvReaderBlock
from src.pyblock import TimeSignal
from src.pyblock.signals.multi_signal import MultiSignal
from src.pyblock.signals.signal_name import SignalName
from src.pyblock.testing.block_runner.block_runner import BlockRunner


class TestCsvBlock:
    def test_reads_simple(self, tmp_path):
        csv_path = tmp_path / 'test_file.csv'
        with open(csv_path, mode='w') as f:
            f.write('''
                col_1, col_2
                1.0  , 1
                1.1
                1.2  , 3
                1.3  ,  
                1.4  , 5'''
        )

        runner = BlockRunner(CsvReaderBlock)
        runner.set_parameter('file', csv_path)

        runner.run()

        outputs = runner.get_outputs()
        multi_signal: MultiSignal = outputs['output']

        assert multi_signal.get(SignalName('col_1')) == [1.0, 1.1, 1.2, 1.3, 1.4]
        assert multi_signal.get(SignalName('col_2')) == [1.0, None, 3.0, None, 5.0]

    def test_combine_signals(self, tmp_path):
        csv_path = tmp_path / 'test_file.csv'
        with open(csv_path, mode='w') as f:
            f.write('''
                col_time, col_2, col_value
                1.0     , 1    , 1
                1.1     ,      , 2
                1.2     , 3    , 3
                1.3     ,
                1.4     , 5    , 5'''
        )

        runner = BlockRunner(CsvReaderBlock)
        runner.set_parameter('file', csv_path)
        runner.set_parameter('combine_signals', [{
            'name': 'combined_signal',
            'time_column': 'col_time',
            'value_column': 'col_value'
        }])

        runner.run()

        outputs = runner.get_outputs()
        multi_signal: MultiSignal = outputs['output']

        combined_signal: TimeSignal = multi_signal.get(SignalName('combined_signal'))
        time = combined_signal.time.tolist()
        value = combined_signal.wave.tolist()
        assert time == [1.0, 1.1, 1.2, 1.3, 1.4]
        assert value == [1,   2,   3,  None,  5]
        assert multi_signal.get(SignalName('col_2')) == [1.0, None, 3.0, None, 5.0]
