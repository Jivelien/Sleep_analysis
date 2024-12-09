from typing import List

from signal_periodizer.interface import SignalPeriodizerInterface


class SignalPeriodizer(SignalPeriodizerInterface):
    def __init__(self, point_per_period: int):
        self._point_per_period = point_per_period

    def period_for(self, signal: List[float], n_of_period: int) -> List[float]:
        starting_point = n_of_period * self._point_per_period
        ending_point = starting_point + self._point_per_period
        return signal[starting_point:ending_point]

    def last_period_for(self, signal: List[float]) -> int:
        return (len(signal) // self._point_per_period) - 1
