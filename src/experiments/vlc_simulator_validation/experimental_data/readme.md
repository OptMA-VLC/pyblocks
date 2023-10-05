## Log de experimentos no lab - 05/10

## Setup Information
Vdd = -Vss = 5V (rx e tx)
v_sig = 3.3V
f = 10kHz

Distance regulated by measuring that point where LED and
diode touch is located @ 30mm in the sliding rail. 
Distance was measured from this point by looking at the 
distance rule in the sliding rail.


## Files

TX information:
```
TEK0000.csv -> V_sig
TEK0001.csv -> V_led-
TEK0002.csv -> V_led+
```

RX information:
```
TEK0003.csv -> Voltage over led (CH2 - CH1)
Measurements taken @ d = 3cm. It was found that CH2
(PD lead not connected to amp op) was connected to V+ and
not GND. Circuit simulation was changed to reflect the fact.
```

Distance tests

With lights on (3 fluorescent tube lamps)
V_out:
```
TEK0004.csv -> 3cm
TEK0005.csv -> 5cm
TEK0006.csv -> 7cm
TEK0007.csv -> 10cm
TEK0011.csv -> 12cm    # Note the jump in file order!
TEK0012.csv -> 15cm
TEK0013.csv -> 18cm
TEK0014.csv -> 20cm (Vpp, not counting ringing = 200mv)
```
Complementary measurements:
```
TEK0008.csv -> 10cm (with lights off)
```

Noise measurements:
```
TEK0009.csv -> ruído (luz apagada, sem led) ; RMS = 2.3mV, avg = 1.2mV
TEK0010.csv -> ruído (3 luzes acessas, sem led) ; RMS = 9.2mV, avg = 9.0mV, pico-a-pico = 23mV
```


