import math
import unittest

from matplotlib import pyplot as plt

from fft_analyser.homebrew import FftHomebrew
from fft_analyser.welch import FftWelch


def generate_sinusoidal_signal(amplitude: float,
                               frequency: float,
                               sampling_rate: int,
                               duration: float,
                               phase: float = 0.0):
    num_samples = int(sampling_rate * duration)
    signal = []
    for i in range(num_samples):
        t = i / sampling_rate
        value = amplitude * math.sin(2 * math.pi * frequency * t + phase)
        signal.append(value)

    return signal


class TestFFTHomebrew(unittest.TestCase):
    def test_fft_return_an_empty_dictionnary_when_no_signal_is_provided(self):
        fft = FftHomebrew(sampling_rate=100)
        signal = []

        sut = fft.compute_for(signal)

        self.assertEqual({}, sut)

    def test_fft_return_a_dictionnary_with_frequency_and_power(self):
        fft = FftHomebrew(sampling_rate=100)
        signal = [0.0, 1.0, 0.0, -1.0]

        sut = fft.compute_for(signal)

        self.assertAlmostEqual(0., sut.get(0.),5)
        self.assertNotAlmostEqual(0., sut.get(25.),5)

    def test_fft_return_a_dictionnary_with_frequency_and_power2(self):
        fft = FftHomebrew(sampling_rate=100)
        signal = generate_sinusoidal_signal(amplitude=5, frequency=12, sampling_rate=100, duration=5)

        sut = fft.compute_for(signal)

        self.assertAlmostEqual(0., sut.get(1.),5)
        self.assertNotAlmostEqual(0., sut.get(12.),5)

class TestFFTWelch(unittest.TestCase):
    def test_fft_return_an_empty_dictionnary_when_no_signal_is_provided(self):
        fft = FftWelch(sampling_rate=100)
        signal = []

        sut = fft.compute_for(signal)

        self.assertEqual({}, sut)


    def test_fft_return_a_dictionnary_with_frequency_and_power(self):
        fft = FftWelch(sampling_rate=100)
        signal = [0.0, 1.0, 0.0, -1.0]

        sut = fft.compute_for(signal)

        self.assertAlmostEqual(0., sut.get(0.),5)
        self.assertNotAlmostEqual(0., sut.get(25.),5)

    def test_fft_return_a_dictionnary_with_frequency_and_power2(self):
        fft = FftWelch(sampling_rate=100)
        signal = generate_sinusoidal_signal(amplitude=5, frequency=12, sampling_rate=100, duration=1)

        sut = fft.compute_for(signal)

        self.assertAlmostEqual(0., sut.get(0.),5)
        self.assertNotAlmostEqual(0., sut.get(12.),5)
