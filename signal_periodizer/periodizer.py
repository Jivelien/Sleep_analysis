from typing import List

from signal_periodizer.interface import SignalPeriodizerInterface


class SignalPeriodizer(SignalPeriodizerInterface):
    def __init__(self, point_per_period: int):
        self._point_per_period = point_per_period

    def period_for(self, signal: List[float], n_of_period: int) -> List[float]:
        return signal[0:100]
