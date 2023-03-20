from numbers import Real
from typing import Type, List

import numpy as np


class SignalWave:
    """
    Represents a time-series signal
    <wave> has the np.array for the actual signal amplitude.
    <time> has the np.array for the related time axis, with same length.
    <sample_frequency> is the calculated based on the <time> axis spacing between each sample.
    """

    wave: np.ndarray = None
    time: np.ndarray = None

    @property
    def sample_frequency(self):
        time_interval = (np.max(self.time) - np.min(self.time)) / (len(self.time) - 1)
        return 1 / time_interval

    def __init__(self, time: np.ndarray or List, signal: np.ndarray or List):
        self.wave = np.asarray(signal)
        self.time = np.asarray(time)

    def get_start_time(self) -> Real:
        return self.time[0]

    def get_end_time(self) -> Real:
        return self.time[-1]

    def get_duration(self) -> Real:
        return self.get_end_time() - self.get_start_time()

    def get_time_step(self) -> Real:
        """Method to get the time step."""
        return 1 / self.sample_frequency

    def __len__(self) -> int:
        if len(self.wave) != len(self.time):
            raise ValueError('SignalWave.wave and SignalWave.time should always have the same length.')
        return len(self.wave)

    def __add__(self, other: 'SignalWave' or Real) -> 'SignalWave':
        """Operator <add> overload for SignalWave"""
        if isinstance(other, Real):
            return SignalWave(signal=self.wave + other, time=self.time)
        self._assert_type(other, self.__class__)
        return SignalWave(signal=self.wave + other.wave, time=self.time)

    def __sub__(self, other: 'SignalWave' or Real) -> 'SignalWave':
        """Operator <sub> overload for SignalWave"""
        if isinstance(other, Real):
            return SignalWave(signal=self.wave - other, time=self.time)
        self._assert_type(other, self.__class__)
        return SignalWave(signal=self.wave - other.wave, time=self.time)

    def __mul__(self, other: 'SignalWave' or Real) -> 'SignalWave':
        """Operator <mul> overload for SignalWave"""
        if isinstance(other, Real):
            return SignalWave(signal=self.wave * other, time=self.time)
        self._assert_type(other, self.__class__)
        return SignalWave(signal=self.wave * other.wave, time=self.time)

    def __truediv__(self, other: 'SignalWave' or Real) -> 'SignalWave':
        """Operator <truediv> overload for SignalWave"""
        if isinstance(other, Real):
            return SignalWave(signal=self.wave / other, time=self.time)
        self._assert_type(other, self.__class__)
        return SignalWave(signal=self.wave / other.wave, time=self.time)

    def __pow__(self, other: int) -> 'SignalWave':
        """Operator <pow> overload for SignalWave"""
        if isinstance(other, int):
            return SignalWave(signal=self.wave ** other, time=self.time)

    def __abs__(self) -> 'SignalWave':
        """Operator <abs> overload for SignalWave"""
        return SignalWave(signal=abs(self.wave), time=self.time)

    def __lt__(self, other: 'SignalWave' or Real) -> List:
        """Operator <lt> overload for SignalWave"""
        if isinstance(other, SignalWave):
            return [point < other[idx] for idx, point in enumerate(self.wave)]
        self._assert_type(other, self.__class__)
        return [point < other for point in self.wave]

    def __le__(self, other: 'SignalWave' or Real) -> List:
        """Operator <le> overload for SignalWave"""
        if isinstance(other, SignalWave):
            return [point <= other[idx] for idx, point in enumerate(self.wave)]
        self._assert_type(other, self.__class__)
        return [point <= other for point in self.wave]

    def __gt__(self, other: 'SignalWave' or Real) -> List:
        """Operator <gt> overload for SignalWave"""
        if isinstance(other, SignalWave):
            return [point > other[idx] for idx, point in enumerate(self.wave)]
        self._assert_type(other, self.__class__)
        return [point > other for point in self.wave]

    def __ge__(self, other: 'SignalWave' or Real) -> List:
        """Operator <ge> overload for SignalWave"""
        if isinstance(other, SignalWave):
            return [point >= other[idx] for idx, point in enumerate(self.wave)]
        self._assert_type(other, self.__class__)
        return [point >= other for point in self.wave]

    def __eq__(self, other: 'SignalWave' or Real) -> List:
        """Operator <eq> overload for SignalWave"""
        if isinstance(other, SignalWave):
            return [point == other[idx] for idx, point in enumerate(self.wave)]
        self._assert_type(other, self.__class__)
        return [point == other for point in self.wave]

    def __ne__(self, other: 'SignalWave' or Real) -> List:
        """Operator <ne> overload for SignalWave"""
        if isinstance(other, SignalWave):
            return [point != other[idx] for idx, point in enumerate(self.wave)]
        self._assert_type(other, self.__class__)
        return [point != other for point in self.wave]

    def __getitem__(self, key) -> np.ndarray:
        return self.wave[key]

    def _assert_type(self, value, type: Type):
        if not isinstance(value, type):
            raise TypeError(f'Expected type {type} but received {value.__class__}')
