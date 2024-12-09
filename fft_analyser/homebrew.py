import math
from typing import List, Dict

from fft_analyser.interface import FftAnalyserInterface


class FftHomebrew(FftAnalyserInterface):
    def __init__(self, sampling_rate: int) -> None:
        self._sampling_rate = sampling_rate

    def compute_for(self, signal: List[float]) -> Dict[float, float]:
        power = self._compute_power(signal)
        frequencies = self._compute_frequencies(signal)

        return dict(zip(frequencies,power))

    def _compute_frequencies(self, signal: List[float]) -> List[float]:
        signal_length = len(signal)
        return [(self._sampling_rate * k) / signal_length for k in range(signal_length // 2)]


    def _compute_power(self, signal: List[float]):
        signal_length = len(signal)
        real_part = [0] * signal_length
        imaginary_part = [0] * signal_length

        for frequency_index in range(signal_length):
            for time_index in range(signal_length):
                angle = 2 * math.pi * frequency_index * time_index / signal_length
                real_part[frequency_index] += signal[time_index] * math.cos(angle)
                imaginary_part[frequency_index] -= signal[time_index] * math.sin(angle)

        magnitudes = [math.sqrt(r ** 2 + i ** 2) for r, i in zip(real_part, imaginary_part)]
        return magnitudes[:signal_length // 2]