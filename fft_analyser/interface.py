from typing import List, Dict


class FftAnalyserInterface:

    def compute_for(self, signal: List[float]) -> Dict[float, float]:
        raise NotImplementedError
