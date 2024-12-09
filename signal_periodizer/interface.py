from typing import List


class SignalPeriodizerInterface:
    def period_for(self, signal: List[int], n_of_period: int) -> List[float]:
        raise NotImplementedError()
