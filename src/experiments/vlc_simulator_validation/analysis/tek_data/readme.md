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
00_input.csv -> V_sig (square wave from sig generator injected at TX)
01_v_led_neg.csv -> V_led-
02_v_led_pos.csv -> V_led+
```

RX information:
```
03_v_pd_3cm.csv -> Voltage over pd (CH2 - CH1)
Measurements taken @ d = 3cm. It was found that CH2
(PD lead not connected to amp op) was connected to V+ and
not GND. Circuit simulation was changed to reflect the fact.
```

Distance tests

With lights on (3 fluorescent tube lamps)
V_out:
```
04_tx_out_3cm.csv -> 3cm
05_tx_out_5cm.csv -> 5cm
06_tx_out_7cm.csv -> 7cm
07_tx_out_10cm.csv -> 10cm
08_tx_out_12cm.csv -> 12cm
09_tx_out_15cm.csv -> 15cm
10_tx_out_18cm.csv -> 18cm
11_tx_out_20cm.csv -> 20cm (Vpp, not counting ringing = 200mv)
```
Complementary measurements:
```
TEK0008 12_tx_out_10cm_light_off.csv -> 10cm (with lights off)
```

Noise measurements:
```
13_noise_dark.csv -> ruído (luz apagada, sem led) ; RMS = 2.3mV, avg = 1.2mV
14_noise_3_lights.csv -> ruído (3 luzes acessas, sem led) ; RMS = 9.2mV, avg = 9.0mV, pico-a-pico = 23mV
```


