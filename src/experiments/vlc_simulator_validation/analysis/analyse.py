from pathlib import Path

import matplotlib.pyplot as plt

from src.experiments.vlc_simulator_validation.analysis import tools, figures
from src.experiments.vlc_simulator_validation.analysis.simulator_reader.simulator_reader import SimulatorReader
from src.experiments.vlc_simulator_validation.analysis.tek_reader.tek_reader import TekReader

# load experimental data
v_in = TekReader.read(Path('./tek_data/00_input.CSV'))
v_led_n = TekReader.read(Path('./tek_data/01_v_led_neg.CSV'))
v_led_p = TekReader.read(Path('./tek_data/02_v_led_pos.CSV'))
v_pd_3cm = TekReader.read(Path('./tek_data/03_v_pd_3cm.CSV'))
v_pd_10cm = TekReader.read(Path('./tek_data/20_v_pd_10cm_cap.CSV'))
v_out_3cm = TekReader.read(Path('./tek_data/04_tx_out_3cm.CSV'))
v_out_5cm = TekReader.read(Path('./tek_data/05_tx_out_5cm.CSV'))
v_out_7cm = TekReader.read(Path('./tek_data/06_tx_out_7cm.CSV'))
v_out_10cm = TekReader.read(Path('./tek_data/07_tx_out_10cm.CSV'))
v_out_12cm = TekReader.read(Path('./tek_data/08_tx_out_12cm.CSV'))
v_out_15cm = TekReader.read(Path('./tek_data/09_tx_out_15cm.CSV'))
v_out_18cm = TekReader.read(Path('./tek_data/10_tx_out_18cm.CSV'))
v_out_20cm = TekReader.read(Path('./tek_data/11_tx_out_20cm.CSV'))
v_led = v_led_p - v_led_n


# load initial simulation data
sim_initial_v_in = SimulatorReader.read(Path('./simulator_data/initial_v_in.csv'))
sim_initial_v_led_n = SimulatorReader.read(Path('./simulator_data/initial_v_led_n.csv'))
sim_initial_v_led_p = SimulatorReader.read(Path('./simulator_data/initial_v_led_p.csv'))
sim_initial_v_pd = SimulatorReader.read(Path('./simulator_data/initial_v_pd.csv'))
sim_initial_v_out_3cm = SimulatorReader.read(Path('./simulator_data/initial_v_out_3cm.csv'))
sim_initial_v_out_10cm = SimulatorReader.read(Path('./simulator_data/initial_v_out_10cm.csv'))
sim_initial_v_led = sim_initial_v_led_p - sim_initial_v_led_n

sim_adj_3cm_v_in = SimulatorReader.read(Path('./simulator_data/adjusted_3cm_v_in.csv'))
sim_adj_3cm_v_led_n = SimulatorReader.read(Path('./simulator_data/adjusted_3cm_v_led_n.csv'))
sim_adj_3cm_v_led_p = SimulatorReader.read(Path('./simulator_data/adjusted_3cm_v_led_p.csv'))
sim_adj_3cm_v_pd = SimulatorReader.read(Path('./simulator_data/adjusted_3cm_v_pd.csv'))
sim_adj_3cm_v_out = SimulatorReader.read(Path('./simulator_data/adjusted_3cm_v_out.csv'))
sim_adj_3cm_v_led = sim_adj_3cm_v_led_p - sim_adj_3cm_v_led_n

sim_adj_10cm_v_in = SimulatorReader.read(Path('./simulator_data/adjusted_10cm_v_in.csv'))
sim_adj_10cm_v_led_n = SimulatorReader.read(Path('./simulator_data/adjusted_10cm_v_led_n.csv'))
sim_adj_10cm_v_led_p = SimulatorReader.read(Path('./simulator_data/adjusted_10cm_v_led_p.csv'))
sim_adj_10cm_v_pd = SimulatorReader.read(Path('./simulator_data/adjusted_10cm_v_pd.csv'))
sim_adj_10cm_v_out = SimulatorReader.read(Path('./simulator_data/adjusted_10cm_v_out.csv'))
sim_adj_10cm_v_led = sim_adj_10cm_v_led_p - sim_adj_10cm_v_led_n


# plot figures
figures.fig00_experimental_signals(v_in, v_out_3cm, v_out_10cm)


figures.fig01_output_sim_vs_exp_3cm_10cm(
    v_out_3cm, v_out_10cm,
    sim_initial_v_out_3cm, sim_initial_v_out_10cm,
    sim_adj_3cm_v_out, sim_adj_10cm_v_out
)

