from typing import List, Dict, Optional

from scipy.signal import welch

from fft_analyser.interface import FftAnalyserInterface


class FftWelch(FftAnalyserInterface):
    def __init__(self, sampling_rate: int,
                 point_per_segment: int = None,
                 overlap: int = None) -> None:
        self._sampling_rate = sampling_rate
        self._point_per_segment = point_per_segment
        self._overlap = overlap

    def compute_for(self, signal: List[float]) -> Dict[float, float]:
        signal_length = len(signal)
        nperseg = self._compute_point_per_segment(signal_length)
        noverlap = self._compute_overlap(signal_length)

        frequencies, power = welch(x=signal,
                                   fs=self._sampling_rate,
                                   nperseg=nperseg,
                                   noverlap=noverlap)
        return dict(zip(frequencies.tolist(), power.tolist()))

    def _compute_point_per_segment(self, signal_length: int) -> Optional[int]:
        if not self._point_per_segment:
            return signal_length
        return min(self._point_per_segment, signal_length)

    def _compute_overlap(self, signal_length: int) -> Optional[int]:
        if not self._overlap:
            return signal_length // 2
        return min(self._overlap, signal_length // 2)
