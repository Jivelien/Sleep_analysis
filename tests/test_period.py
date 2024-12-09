import unittest

from signal_periodizer.error import PeriodOutOfBoundError
from signal_periodizer.periodizer import SignalPeriodizer




class TestSignalPeriodizer(unittest.TestCase):
    def test_periodize_return_number_of_point_define_in_init(self):
        periodizer = SignalPeriodizer(point_per_period=100)
        signal = [float(i) for i in range(1000)]

        sut = periodizer.period_for(signal=signal, n_of_period=0)

        self.assertEqual(100, len(sut))
        self.assertEqual(0, sut[0])
        self.assertEqual(99, sut[99])

    def test_periodizer_return_the_right_period(self):
        periodizer = SignalPeriodizer(point_per_period=100)
        signal = [float(i) for i in range(1000)]

        sut = periodizer.period_for(signal=signal, n_of_period=1)

        self.assertEqual(100, len(sut))
        self.assertEqual(100, sut[0])
        self.assertEqual(199, sut[99])

    def test_periodizer_can_tell_the_last_period_you_can_get_for_a_signal(self):
        periodizer = SignalPeriodizer(point_per_period=100)
        signal = [float(i) for i in range(1050)]

        sut = periodizer.last_period_for(signal=signal)

        self.assertEqual(9, sut)

        sut2 = periodizer.period_for(signal=signal, n_of_period=9)
        self.assertEqual(100, len(sut2))
        self.assertEqual(900, sut2[0])
        self.assertEqual(999, sut2[99])

    def test_periodizer_raise_error_when_period_is_out_of_bound(self):
        periodizer = SignalPeriodizer(point_per_period=100)
        signal = [float(i) for i in range(1050)]

        with self.assertRaises(PeriodOutOfBoundError):
            _ = periodizer.period_for(signal=signal, n_of_period=100)




















