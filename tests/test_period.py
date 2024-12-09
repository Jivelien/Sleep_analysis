import unittest

from signal_periodizer.periodizer import SignalPeriodizer


class TestSignalPeriodizer(unittest.TestCase):
    def test_periodize_return_number_of_point_define_in_init(self):
        periodizer = SignalPeriodizer(point_per_period=100)
        signal = [float(i) for i in range(1000)]

        sut = periodizer.period_for(signal=signal, n_of_period=0)

        self.assertEqual(100, len(sut))
        self.assertEqual(0, sut[0])
        self.assertEqual(99, sut[99])

