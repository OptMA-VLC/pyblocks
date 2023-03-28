from matplotlib import pyplot as plt

from src.pyblock.signals.signal_wave import SignalWave


def plot(signal: SignalWave):
    fig, ax1 = plt.subplots()
    ax1.plot(signal.time, signal.wave, color='k')
    plt.legend()
    plt.show()
