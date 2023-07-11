import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from src.pyblock import TimeSignal
from src.pyblock.block.base_block import BaseBlock
from src.pyblock.block.block_info import BlockInfo
from src.pyblock.block.params.parameter import Parameter
from src.pyblock.block.ports.output_port import OutputPort
from src.pyblock.signals.multi_signal import MultiSignal
from src.pyblock.signals.signal_name import SignalName


@dataclass
class CombineSignalSpec:
    name: str
    time_column: str
    value_column: str


class CsvReaderBlock(BaseBlock):
    def __init__(self):
        self.info = BlockInfo(
            distribution_id='com.pyblocks.basic.csv_reader',
            name='CSV Reader'
        )
        self.csv_path = Parameter(param_id='file', type=str)
        self.combine_signals = Parameter(param_id='combine_signals', type=List[Dict], default=None)
        self.output = OutputPort(port_id='output', type=MultiSignal)

    def run(self):
        csv_path_str = self.csv_path.value
        csv_signals_dict = self.read_columns(Path(csv_path_str))
        combine_signals = self.get_combine_signals()

        out_signals = MultiSignal()

        for cs in combine_signals:
            combined = TimeSignal(
                time=csv_signals_dict[cs.time_column],
                signal=csv_signals_dict[cs.value_column]
            )

            del csv_signals_dict[cs.time_column]
            del csv_signals_dict[cs.value_column]

            out_signals.set(SignalName(cs.name), combined)

        for (name, signal) in csv_signals_dict.items():
            out_signals.set(name, signal)

        self.output.signal = out_signals

    def get_combine_signals(self) -> List[CombineSignalSpec]:
        combine_signal_param = self.combine_signals.value
        if combine_signal_param is None:
            return []

        combine_spec_list = []
        
        for combine_signal_dict in combine_signal_param:
            try:
                name = combine_signal_dict['name']
                time_col = combine_signal_dict['time_column']
                value_col = combine_signal_dict['value_column']
            except KeyError:
                raise KeyError(f'Error reading param combine_signals, got {combine_signal_dict}')
    
            combine_spec_list.append(
                CombineSignalSpec(
                    name=name,
                    time_column=time_col,
                    value_column=value_col
                )
            )

        return combine_spec_list

    def read_columns(self, csv_path: Path) -> Dict:
        with open(csv_path, newline='') as f:
            reader = csv.reader(f)
            csv_dict = None

            for row in reader:
                if row == []:
                    continue

                if csv_dict is None:
                    csv_dict = {}
                    for header in row:
                        csv_dict[str.strip(header)] = []
                else:
                    parsed_row = self._parse_csv_row(row, len(csv_dict))

                    for (i, col_header) in enumerate(csv_dict.keys()):
                        csv_dict[col_header].append(parsed_row[i])

        return csv_dict

    def _parse_csv_row(self, row: List, expected_len: int) -> List:
        parsed_row = []

        for value in row:
            if isinstance(value, str):
                value = str.strip(value)
                if value == '':
                    value = None
                if value[0] == '"' and value[-1] == '"':
                    value = value[1:(len(value)-1)]
                if value.count(',') == 1:
                    value = value.replace(',', '.')

            try:
                value = float(value)
            except:
                value = None

            parsed_row.append(value)

        len_difference = expected_len - len(parsed_row)
        additional_nones = []
        if len_difference > 0:
            additional_nones = [None] * len_difference

        return parsed_row + additional_nones
