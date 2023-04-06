from matplotlib import pyplot as plt

from src.pyblock.signals.time_signal import TimeSignal


def plot(signal: TimeSignal):
    fig, ax1 = plt.subplots()
    ax1.plot(signal.time, signal.wave, color='k')
    plt.legend()
    plt.show()
