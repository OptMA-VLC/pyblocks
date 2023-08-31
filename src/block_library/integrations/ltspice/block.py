import glob
import os
from pathlib import Path
from typing import List

from PyLTSpice import SimCommander
from PyLTSpice import RawRead

from src.block_library.integrations.ltspice.ltspice_runner_config import LTSpiceRunnerConfig
from src.pyblock.block.base_block import BaseBlock
from src.pyblock.block.block_info import BlockInfo
from src.pyblock.block.params.parameter import Parameter
from src.pyblock.block.ports.input_port import InputPort
from src.pyblock.block.ports.output_port import OutputPort
from src.pyblock.signals.multi_signal import MultiSignal
from src.pyblock.signals.signal_name import SignalName
from src.pyblock.signals.time_signal import TimeSignal


class LTSpiceRunner(BaseBlock):
    def __init__(self):
        self.info = BlockInfo(
            distribution_id='com.pyblocks.integrations.ltspice',
            name='LTSpice Runner Block',
            description='Takes a signal, simulates a circuit in LTSpice and provides an output'
        )

        self.param_schematic_file = Parameter(param_id='schematic_file', type=str)
        self.param_file_name_in_circuit = Parameter(param_id='file_name_in_circuit', type=str)
        self.param_add_instructions = Parameter(param_id='add_instructions', type=List[str])
        self.param_probe_signals = Parameter(param_id='probe_signals', type=List[str])

        self.signal_in = InputPort(port_id='signal_in', type=TimeSignal)
        self.signal_out = OutputPort(port_id='signal_out', type=MultiSignal)

    def run(self):
        config = LTSpiceRunnerConfig(
            schematic_file=Path(self.param_schematic_file.value),
            file_name_in_circuit=self.param_file_name_in_circuit.value,
            add_instructions=self.param_add_instructions.value,
            probe_signals=self.param_probe_signals.value
        )
        signal = self.signal_in.signal

        self.write_signal_file(config, signal)
        self.run_ltspice(config)
        out_signal = self.get_output(config)
        self.remove_temp_files(config)

        self.signal_out.signal = out_signal

    def write_signal_file(self, config: LTSpiceRunnerConfig, signal: TimeSignal):
        file_name_in_circuit = Path(config.file_name_in_circuit).resolve()

        with open(file_name_in_circuit, "w") as file_in_circuit:
            for idx in range(len(signal)):
                time = signal.time[idx]
                value = signal.signal[idx]
                file_in_circuit.write(f'{time}\t{value}\n')

    def run_ltspice(self, config: LTSpiceRunnerConfig):
        schematic_path = Path(config.schematic_file)
        if not schematic_path.exists():
            raise RuntimeError(f'Schematic file could not be found in the provided path {schematic_path.resolve()}')

        sim_commander = SimCommander(str(schematic_path))
        sim_commander.reset_netlist()

        add_instructions = config.add_instructions
        sim_commander.add_instructions(*add_instructions)

        run_netlist_file = f"{schematic_path.stem}.net"
        sim_commander.run(run_filename=run_netlist_file)
        sim_commander.wait_completion()

        # Sim Statistics
        print(f'Successful/Total Simulations: {str(sim_commander.okSim)}/{str(sim_commander.runno)}')

    def get_output(self, config) -> MultiSignal:
        try:
            raw_data = RawRead(f'{Path(config.schematic_file).stem}.raw')
        except FileNotFoundError:
            with open(f'{Path(config.schematic_file.stem)}.fail') as fail_file:
                error_msg = fail_file.read()
            raise RuntimeError(
                f'LTSpice simulation failed with message: {error_msg}'
            )

        signal_trace_dict = {'time': raw_data.get_axis()}
        signal_trace_dict.update({signal: raw_data.get_trace(signal) for signal in config.probe_signals})

        print(f'Recovered {len(signal_trace_dict)} signals, including time')
        time = signal_trace_dict['time']

        out_signals = MultiSignal()
        for (key, signal) in signal_trace_dict.items():
            if key != 'time':
                print(f'Recovered signal {key} for output')
                out_signal = TimeSignal(time, signal)
                out_signals.set(SignalName(key), out_signal)
                break

        if len(out_signals) == 0:
            raise RuntimeError('Could not recover an output signal from simulation')

        return out_signals

    def remove_temp_files(self, config: LTSpiceRunnerConfig):
        ltspice_file = Path().cwd() / Path("LtSpice") / Path(config.schematic_file)
        ltspice_file_parent = ltspice_file.parent

        log_files = glob.glob('*.log')
        net_lt_files = glob.glob(f'{ltspice_file_parent}\*.net')
        net_files = glob.glob('*.net')
        raw_files = glob.glob('*.raw')
        txt_files = glob.glob('*.txt')

        files = net_lt_files + net_files + raw_files + txt_files

        # os.remove("ltspice_file_asc.log")
        for exc_file in files:
            try:
                os.remove(exc_file)
            except OSError as e:
                print(f"Error:{e.strerror}")
