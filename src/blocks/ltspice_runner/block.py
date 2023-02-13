import glob
import os
from pathlib import Path
from typing import Any

from PyLTSpice import SimCommander
from PyLTSpice.LTSpice_RawRead import LTSpiceRawRead

from src.bdk.base_block import BaseBlock
from src.bdk.block_info import BlockInfo
from src.bdk.params.parameter import Parameter
from src.bdk.ports.PortBundle import PortBundle
from src.bdk.ports.port import Port
from src.bdk.signals.signal_wave import SignalWave
from src.blocks.ltspice_runner.ltspice_runner_config import LTSpiceRunnerConfig

from src.meow_sim.entity.param_bundle import ParamBundle


class LTSpiceRunner(BaseBlock):
    def __init__(self):
        self.block_info = BlockInfo(
            distribution_id='br.ufmg.optma.ltspice_runner',
            name='LTSpice Runner Block',
            description='Takes a signal, simulates a circuit in LTSpice and provides an output'
        )
        self.params = ParamBundle(
            Parameter(id='config', type=Any, required=True)
        )
        self.inputs = PortBundle(
            Port(port_id='signal_in', signal_type=SignalWave)
        )
        self.outputs = PortBundle(
            Port(port_id='signal_out', signal_type=SignalWave)
        )

        super().__init__()

    def run(self):
        config = self.params.get_param('config')
        signal = self.inputs.get_signal('signal_in')
        self.write_signal_file(config, signal)

        self.run_ltspice(config)

        out_signal = self.get_output(config)
        self.outputs.set_signal('signal_out', out_signal)

        self.remove_temp_files(config)

    def write_signal_file(self, config: LTSpiceRunnerConfig, signal: SignalWave):
        file_name_in_circuit = Path(config.file_name_in_circuit).resolve()

        with open(file_name_in_circuit, "w") as file_in_circuit:
            for idx in range(len(signal)):
                time = signal.time[idx]
                value = signal.wave[idx]
                file_in_circuit.write(f'{time}\t{value}\n')

    def run_ltspice(self, config: LTSpiceRunnerConfig):
        schematic_path = Path(config.schematic_file)
        if not schematic_path.exists():
            raise RuntimeError(f'Schematic file could not be found in the provided path {schematic_path}')

        sim_commander = SimCommander(str(schematic_path))
        sim_commander.reset_netlist()

        add_instructions = config.add_instructions
        sim_commander.add_instructions(*add_instructions)

        run_netlist_file = f"{schematic_path.stem}.net"
        sim_commander.run(run_filename=run_netlist_file)
        sim_commander.wait_completion()

        # Sim Statistics
        print(f'Successful/Total Simulations: {str(sim_commander.okSim)}/{str(sim_commander.runno)}')

    def get_output(self, config) -> SignalWave:
        raw_data = LTSpiceRawRead(f'{Path(config.schematic_file).stem}.raw')

        signal_trace_dict = {'time': raw_data.get_axis()}
        signal_trace_dict.update({signal: raw_data.get_trace(signal) for signal in config.probe_signals})

        print(f'Recovered {len(signal_trace_dict)} signals, including time')
        time = signal_trace_dict['time']

        out_signal = None
        for (key, signal) in signal_trace_dict.items():
            if key != 'time':
                print(f'Recovered signal {key} for output')
                out_signal = signal
                break

        if out_signal is None:
            raise RuntimeError('Could not recover a signal from simulation to use as output')

        return SignalWave(time, out_signal)

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
