from pathlib import Path
from typing import List, Any, Union

import cycler
import matplotlib
from matplotlib import pyplot as plt

from src.experiments.vlc_simulator_validation.analysis.simulator_reader.simulator_reader import SimulatorReader
from src.experiments.vlc_simulator_validation.analysis.simulator_reader.simulator_result import SimulatorResult
from src.experiments.vlc_simulator_validation.analysis.tek_reader.tek_reader import TekReader
from src.experiments.vlc_simulator_validation.analysis.tek_reader.tek_result import TekResult


def compare_LED_voltage(simul_led_v: Path, exp_led_pos: Path, exp_led_neg: Path):
    simul_led_v = SimulatorReader.read(simul_led_v)
    exp_led_pos = TekReader.read(exp_led_pos)
    exp_led_neg = TekReader.read(exp_led_neg)

    plt.plot(exp_led_pos.time, exp_led_pos.signal - exp_led_neg.signal)
    plt.plot(simul_led_v.time, simul_led_v.signal)
    plt.title('Voltage over LED')
    plt.grid(True)
    plt.show()


def fig00_experimental_signal_chain(
        rx_in: TekResult, v_led: TekResult, v_pd: TekResult, tx_out: TekResult
):
    # adjust v_pd position:
    v_pd.time += 55 * 10**-6

    fig, axs = plt.subplots(2, 2)
    _do_subplot(axs[0][0], [rx_in], 'v_{IN}', [-20, 80], [-1, 6])
    _do_subplot(axs[0][1], [v_led], 'v_{LED}', [-20, 80], [0, 2])
    _do_subplot(axs[1][0], [v_pd], 'v_{PD}', [-20, 80], [-1, 6])
    _do_subplot(axs[1][1], [tx_out], 'v_{OUT}', [-20, 80], [-1, 6])

    plt.tight_layout()
    plt.show()


def fig01_initial_simulation_signal_chain(
        v_in: TekResult, v_led: TekResult, v_pd: TekResult, v_out: TekResult,
        sim_v_in: SimulatorResult, sim_v_led: SimulatorResult,
        sim_v_pd: SimulatorResult, sim_v_out: SimulatorResult
):
    sim_v_in.trigger_at(3)
    sim_v_led.trigger_at((min(sim_v_led.signal) + max(sim_v_led.signal)) / 2)
    sim_v_pd.trigger_at(0.1)
    v_pd.time += 56 * 10**-6
    sim_v_out.trigger_at(2)

    fig, axs = plt.subplots(2, 2)
    _do_subplot(axs[0][0], [v_in, sim_v_in], 'v_{IN}', [-20, 100], [-1, 6])
    _do_subplot(axs[0][1], [v_led, sim_v_led], 'v_{LED}', [-20, 100], [0, 2])
    _do_subplot(axs[1][0], [v_pd, sim_v_pd], 'v_{PD}', [-20, 100], [-1, 6])
    _do_subplot(axs[1][1], [v_out, sim_v_out], 'v_{OUT}', [-20, 100], [-1, 6])

    # handles, labels = axs[1][1].get_legend_handles_labels()
    # fig.legend(handles, labels, loc='upper center')
    plt.tight_layout()
    plt.show()


def _do_subplot(
        ax: Any, signals: List[TekResult], signal_name: str,
        xlim=None, ylim=None
):
    styles = ['k', 'b']
    for i, signal in enumerate(signals):
        ax.plot(signal.time * 1_000_000, signal.signal, styles[i], linewidth=0.5)
    ax.set_title(f'${signal_name}$')
    ax.set(xlabel='Tempo (µs)', ylabel=f'Tensão (V)')
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.grid(True)


def fig01_v_out_inicial(simulated_csv: Path, experimental_csv: Path):
    simulated_result = SimulatorReader.read(simulated_csv)
    tek_result = TekReader.read(experimental_csv)

    trig_value = (max(simulated_result.signal) + min(simulated_result.signal)) / 2
    simulated_result.trigger_at(trig_value)

    # plot
    # plt.subplot()
    plt.plot(
        simulated_result.time * 1_000_000, simulated_result.signal,
        label='$v_{out}$ (simulado)', color='blue', linewidth=1
    )
    plt.plot(
        tek_result.time * 1_000_000, tek_result.signal,
        label='$v_{out}$ (experimental)', color='red', linewidth=1
    )

    plt.title('$v_{out} - Simulação Inicial$')
    plt.xlabel('tempo (µs)')
    plt.ylabel('$v_{out}$ (V)')
    plt.xlim(-20, 80)
    plt.legend()
    plt.grid(True)

    # Display the plot
    plt.show()


def plot_two_signals(
        label1, x1, y1,
        label2, x2, y2,
        title=None, x_label=None, y_label=None
):
    plt.plot(x1, y1, label=label1, color='blue', linewidth=1)
    plt.plot(x2, y2, label=label2, color='red', linewidth=1)

    # Add labels, title, legend, and grid
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.grid(True)

    # Display the plot
    plt.show()


