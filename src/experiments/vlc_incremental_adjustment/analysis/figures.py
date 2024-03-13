from itertools import cycle
from typing import List, Any

from matplotlib import pyplot as plt

from src.experiments.vlc_incremental_adjustment.analysis.simulator_reader.simulator_result import SimulatorResult
from src.experiments.vlc_incremental_adjustment.analysis.tek_reader.tek_result import TekResult

def plot_side_by_side(
    exp1, sim1, exp2, sim2,
    title1 = '', title2 = '',
    xlim1 = None, xlim2 = None,
    ylim1 = None, ylim2 = None
):
    fig, axs = plt.subplots(1, 2, figsize=(11, 6))
    _do_subplot(axs[0], [exp1, sim1], title1, xlim1, ylim1)
    _do_subplot(axs[1], [exp2, sim2], title2, xlim2, ylim2)

    plt.tight_layout()
    plt.show()


def fig00_experimental_signals(
        rx_in: TekResult, tx_out_3cm: TekResult, tx_out_10cm: TekResult
):
    fig, axs = plt.subplots(3, 1)
    _do_subplot(axs[0], [rx_in], '$v_{IN}$', [-20, 80], [-1, 6])
    _do_subplot(axs[1], [tx_out_3cm], '$v_{OUT} \; (3cm)$', [-20, 80], [-1, 6])
    _do_subplot(axs[2], [tx_out_10cm], '$v_{OUT} \; (10cm)$', [-20, 80], [-1, 6])

    plt.tight_layout()
    plt.show()


def fig01_output_sim_vs_exp_3cm_10cm(
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



def _do_subplot(
        ax: Any, signals: List[TekResult], title: str,
        xlim=None, ylim=None, labels=['']
):
    styles = cycle(['k', 'r'])
    linewidths = cycle([0.4, 1])
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

