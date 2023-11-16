from itertools import cycle
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
    _do_subplot(axs[0][0], [rx_in], '$v_{IN}$', [-20, 80], [-1, 6])
    _do_subplot(axs[0][1], [v_led], '$v_{LED}$', [-20, 80], [0, 2])
    _do_subplot(axs[1][0], [v_pd], '$v_{PD}$', [-20, 80], [-1, 6])
    _do_subplot(axs[1][1], [tx_out], '$v_{OUT}$', [-20, 80], [-1, 6])

    plt.tight_layout()
    plt.show()


def fig01_initial_simulation_signal_chain(
        v_in: TekResult, v_led: TekResult, v_pd: TekResult, v_out: TekResult,
        sim_v_in: SimulatorResult, sim_v_led: SimulatorResult,
        sim_v_pd: SimulatorResult, sim_v_out: SimulatorResult
):
    xlim = [-20, 80]
    sim_v_in.trigger_at(sim_v_in.get_v_half())
    sim_v_led.trigger_at(sim_v_led.get_v_half())
    sim_v_pd.trigger_at(0.1)
    sim_v_out.trigger_at(1)
    v_pd.time += 56 * 10**-6

    fig, axs = plt.subplots(2, 2)
    _do_subplot(axs[0][0], [v_in, sim_v_in], '$v_{IN}$', xlim, [-1, 6])
    _do_subplot(axs[0][1], [v_led, sim_v_led], '$v_{LED}$', xlim, [0, 2.5])
    _do_subplot(axs[1][0], [v_pd, sim_v_pd], '$v_{PD}$', xlim, [-1, 6])
    _do_subplot(axs[1][1], [v_out, sim_v_out], '$v_{OUT}$', xlim, [-1, 6])

    plt.tight_layout()
    plt.show()


def fig02_output_sim_vs_exp_3cm_10cm(
        experimental_3cm: TekResult, experimental_10cm: TekResult,
        initial_3cm: SimulatorResult, initial_10cm: SimulatorResult,
        adjusted_3cm: SimulatorResult, adjusted_10cm: SimulatorResult

):
    initial_3cm.trigger_at(1)
    initial_10cm.trigger_at(initial_10cm.get_v_half())
    adjusted_3cm.trigger_at(adjusted_3cm.get_v_half())
    adjusted_10cm.trigger_at(adjusted_10cm.get_v_half())
    xlim = [-20, 80]
    ylim = [-0.5, 1.6]

    fig, axs = plt.subplots(2, 2)
    _do_subplot(axs[0][0], [experimental_3cm, initial_3cm], '$v_{OUT}$ - Inicial, 3cm', xlim=xlim, ylim=ylim)
    _do_subplot(axs[0][1], [experimental_10cm, initial_10cm], '$v_{OUT}$ - Inicial, 10cm', xlim=xlim, ylim=ylim)
    _do_subplot(axs[1][0], [experimental_3cm, adjusted_3cm], '$v_{OUT}$ - Ajustado, 3cm', xlim=xlim, ylim=ylim)
    _do_subplot(
        axs[1][1], [experimental_10cm, adjusted_10cm],
        '$v_{OUT}$ - Ajustado, 10cm', labels=['Experimental', 'Simulado'], xlim=xlim, ylim=ylim
    )

    handles, labels = axs[1][1].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=2)
    plt.tight_layout()
    fig.set_size_inches(8.5, 6.5)
    plt.subplots_adjust(left=0.1, bottom=0.12)
    plt.show()

def fig03_adjusted_signal_chain(
        v_in: TekResult, v_led: TekResult, v_pd: TekResult, v_out: TekResult,
        sim_v_in: SimulatorResult, sim_v_led: SimulatorResult,
        sim_v_pd: SimulatorResult, sim_v_out: SimulatorResult
):
    xlim = [-20, 80]
    sim_v_in.trigger_at(sim_v_in.get_v_half())
    sim_v_led.trigger_at(sim_v_led.get_v_half())
    sim_v_pd.trigger_at(0.15)
    sim_v_out.trigger_at(sim_v_out.get_v_half())
    v_pd.time += (56) * 10**-6

    fig, axs = plt.subplots(2, 2)
    _do_subplot(axs[0][0], [v_in, sim_v_in], '$v_{IN}$', xlim, [-1, 6])
    _do_subplot(axs[0][1], [v_led, sim_v_led], '$v_{LED}$', xlim, [0, 2.5])
    _do_subplot(axs[1][0], [v_pd, sim_v_pd], '$v_{PD}$', xlim, [-0.2, 0.2])
    _do_subplot(
        axs[1][1], [v_out, sim_v_out],
        '$v_{OUT}$', xlim, [-1, 6], labels=['Experimental', 'Simulado']
    )

    handles, labels = axs[1][1].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=2)
    plt.tight_layout()
    fig.set_size_inches(8.5, 6.5)
    plt.subplots_adjust(left=0.1, bottom=0.12)
    plt.show()

def _do_subplot(
        ax: Any, signals: List[TekResult], title: str,
        xlim=None, ylim=None, labels=['']
):
    styles = cycle(['k', 'r'])
    linewidths = cycle([0.4, 0.6])
    labels = cycle(labels)
    for i, signal in enumerate(signals):
        ax.plot(
            signal.time * 1_000_000, signal.signal,
            next(styles), linewidth=next(linewidths), label=next(labels)
        )
    ax.set_title(f'{title}')
    ax.set(xlabel='Tempo (µs)', ylabel=f'Tensão (V)')
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.grid(True)




def fig09_v_out_inicial(simulated_csv: Path, experimental_csv: Path):
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


def figxx_outuput_voltage_by_distance(distances: List[float], vpp_by_distance: List[float]):
    plt.plot(distances, vpp_by_distance, color='gray')
    plt.plot(distances, vpp_by_distance, 'ok')
    plt.show()
