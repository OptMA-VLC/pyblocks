from pathlib import Path

import cases
from src.experiments.vlc_simulator_validation.analysis.simulator_reader.simulator_reader import SimulatorReader
from src.experiments.vlc_simulator_validation.analysis.tek_reader.tek_reader import TekReader

# load experimental data
v_in = TekReader.read(Path('./tek_data/00_input.CSV'))
v_led_n = TekReader.read(Path('./tek_data/01_v_led_neg.CSV'))
v_led_p = TekReader.read(Path('./tek_data/02_v_led_pos.CSV'))
v_pd_3cm = TekReader.read(Path('./tek_data/03_v_pd_3cm.CSV'))
v_out_3cm = TekReader.read(Path('./tek_data/04_tx_out_3cm.CSV'))
v_led = v_led_p - v_led_n

# load initial simulation data
sim_initial_v_in = SimulatorReader.read(Path('./simulator_data/initial_v_in.csv'))
sim_initial_v_led_n = SimulatorReader.read(Path('./simulator_data/initial_v_led_n.csv'))
sim_initial_v_led_p = SimulatorReader.read(Path('./simulator_data/initial_v_led_p.csv'))
sim_initial_v_pd = SimulatorReader.read(Path('./simulator_data/initial_v_pd.csv'))
sim_initial_v_out = SimulatorReader.read(Path('./simulator_data/initial_out.csv'))
sim_initial_v_led = sim_initial_v_led_p - sim_initial_v_led_n

sim_adj_3cm_v_in = SimulatorReader.read(Path('./simulator_data/adjusted_3cm_v_in.csv'))
sim_adj_3cm_v_led_n = SimulatorReader.read(Path('./simulator_data/adjusted_3cm_v_led_n.csv'))
sim_adj_3cm_v_led_p = SimulatorReader.read(Path('./simulator_data/adjusted_3cm_v_led_p.csv'))
sim_adj_3cm_v_pd = SimulatorReader.read(Path('./simulator_data/adjusted_3cm_v_pd.csv'))
sim_adj_3cm_v_out = SimulatorReader.read(Path('./simulator_data/adjusted_3cm_v_out.csv'))
sim_adj_3cm_v_led = sim_adj_3cm_v_led_p - sim_adj_3cm_v_led_n


# plot figures
# cases.fig00_experimental_signal_chain(v_in, v_led, v_pd_3cm, v_out_3cm)

# cases.fig01_initial_simulation_signal_chain(
#     v_in, v_led, v_pd_3cm, v_out_3cm,
#     sim_initial_v_in, sim_initial_v_led, sim_initial_v_pd, sim_initial_v_out
# )

cases.fig01_initial_simulation_signal_chain(
    v_in, v_led, v_pd_3cm, v_out_3cm,
    sim_adj_3cm_v_in, sim_adj_3cm_v_led, sim_adj_3cm_v_pd, sim_adj_3cm_v_out
)

# cases.fig01_v_out_inicial(
#     simulated_csv=Path('./simulator_data/initial_out.csv'),
#     experimental_csv=Path('./tek_data/07_tx_out_10cm.CSV')
# )


# cases.compare_LED_voltage(
#     Path('./simulator_data/led_voltage.csv'),
#     Path('./tek_data/02_v_led_pos.CSV'),
#     Path('./tek_data/01_v_led_neg.CSV')
# )
#
