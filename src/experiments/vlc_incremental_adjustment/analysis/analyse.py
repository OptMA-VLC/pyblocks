from pathlib import Path

import matplotlib.pyplot as plt

from src.experiments.vlc_incremental_adjustment.analysis import util, figures
from src.experiments.vlc_incremental_adjustment.analysis.simulator_reader.simulator_reader import SimulatorReader
from src.experiments.vlc_incremental_adjustment.analysis.tek_reader.tek_reader import TekReader

# load experimental data
v_in = TekReader.read(Path('./tek_data/00_input.CSV'))
v_out_3cm = TekReader.read(Path('./tek_data/04_tx_out_3cm.CSV'))
v_out_10cm = TekReader.read(Path('./tek_data/07_tx_out_10cm.CSV'))

# load simulation data
sim_1_initial_3cm = SimulatorReader.read(Path('./simulator_data/1_vout_initial_3cm.csv'))
sim_1_initial_10cm = SimulatorReader.read(Path('./simulator_data/1_vout_initial_10cm.csv'))
sim_2_pd_3cm = SimulatorReader.read(Path('./simulator_data/2_vout_pd_3cm.csv'))
sim_2_pd_10cm = SimulatorReader.read(Path('./simulator_data/2_vout_pd_10cm.csv'))
sim_3_led_3cm = SimulatorReader.read(Path('./simulator_data/3_vout_led_3cm.csv'))
sim_3_led_10cm = SimulatorReader.read(Path('./simulator_data/3_vout_led_10cm.csv'))
sim_4_cap_3cm = SimulatorReader.read(Path('./simulator_data/4_vout_cap_3cm.csv'))
sim_4_cap_10cm = SimulatorReader.read(Path('./simulator_data/4_vout_cap_10cm.csv'))


# adjust signals
sim_1_initial_3cm.trigger_at(1)
sim_1_initial_10cm.trigger_at(1)
sim_2_pd_3cm.trigger_at(0.5)
sim_2_pd_10cm.trigger_at(0.5)
sim_3_led_3cm.trigger_at(0.5)
sim_3_led_10cm.trigger_at(0.5)
sim_4_cap_3cm.trigger_at(0.5)
sim_4_cap_10cm.trigger_at(0.5)

# plot figures
figures.plot_side_by_side(
    v_out_3cm, sim_1_initial_3cm,
    v_out_10cm, sim_1_initial_10cm,
    title1='$v_{out}   -   $3cm', title2='$v_{out}   -   $10cm',
    xlim1=[-20, 80], xlim2=[-20, 80],
    ylim1=[-0.5, 4], ylim2=[-0.5, 4]
)

figures.plot_side_by_side(
    v_out_3cm, sim_2_pd_3cm,
    v_out_10cm, sim_2_pd_10cm,
    title1='$v_{out}   -   $3cm', title2='$v_{out}   -   $10cm',
    xlim1=[-20, 80], xlim2=[-20, 80],
    ylim1=[-0.5, 2], ylim2=[-0.5, 2]
)

figures.plot_side_by_side(
    v_out_3cm, sim_3_led_3cm,
    v_out_10cm, sim_3_led_10cm,
    title1='$v_{out}   -   $3cm', title2='$v_{out}   -   $10cm',
    xlim1=[-20, 80], xlim2=[-20, 80],
    ylim1=[-0.5, 2], ylim2=[-0.5, 2]
)

figures.plot_side_by_side(
    v_out_3cm, sim_4_cap_3cm,
    v_out_10cm, sim_4_cap_10cm,
    title1='$v_{out}   -   $3cm', title2='$v_{out}   -   $10cm',
    xlim1=[-20, 80], xlim2=[-20, 80],
    ylim1=[-0.5, 2], ylim2=[-0.5, 2]
)