#### Comparison of two VLC Circuit Designs

### Code Organization

The folders `basic_circuit` and `adaptative_circuit` contain the project file 
and circuit schematic files for each one of the circuits. Inside each of these 
folders a `sweep_result` folder is generated when the simulator is run.

A third folder `analysis` contains the scripts for comparing the two circuits.
It also has a `sweep_result` folder but this one is not generated as an output
of the simulator, instead, this is a copy that exists only for `analyze_circuit.py`
to be able to load the results from `basic_circuit_data.pkl` and `adaptative_circuit_data.pkl`.

These two pickle (.pkl) files are copied and renamed from the results generated
by the parameter sweep. The source files are `./basic_circuit/sweep_result/data.pkl` 
and `./adaptative_circuit/sweep_result/data.pkl`.