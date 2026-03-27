
import pytest

from src.pipeline.filters import BandPass, HighCut, HighPass, LowCut, LowPass, MovingAverage, Notch


def test_moving_average_filter_length():
    input_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    filter = MovingAverage('mavg(n=5)')

    for value in input_values:
        filter.calc(value)

    assert filter.last_calc_value() == 8

def test_moving_average_filter():
    input_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    filter = MovingAverage('mavg(n=11)')

    for value in input_values:
        filter.calc(value)

    assert filter.last_calc_value() == 5.5

def test_lowpass():
    input_values = [10, 13, 50, 86, 3, 7, 18]
    filter = LowPass('lpass(alpha=0.05)')

    for value in input_values:
        filter.calc(value)

    assert filter.last_calc_value() == pytest.approx(8, rel=0.01)

def test_lowpass_big_alpha():
    input_values = [10, 13, 50, 86, 3, 7, 18]
    filter = LowPass('lpass(alpha=0.34)')

    for value in input_values:
        filter.calc(value)

    assert filter.last_calc_value() == pytest.approx(20.6, rel=0.001)

def test_highpass():
    input_values = [10, 13, 50, 86, 3, 7, 18]
    filter = HighPass('hpass(alpha=0.05)')

    for value in input_values:
        filter.calc(value)

    assert filter.last_calc_value() == pytest.approx(10.03, rel=0.001)

def test_highpass_big_alpha_minus_output():
    input_values = [10, 13, 50, 86, 3, 7, 18]
    filter = HighPass('hpass(alpha=0.34)')

    for value in input_values:
        filter.calc(value)

    assert filter.last_calc_value() == pytest.approx(-2.6, rel=0.001)

def test_highpass_big_alpha_plus_output():
    input_values = [110, 13, 50, 20, 3, 7, 49]
    filter = HighPass('hpass(alpha=0.34)')

    for value in input_values:
        filter.calc(value)

    assert filter.last_calc_value() == pytest.approx(21.5, rel=0.001)

def test_bandpass():
    input_values = [10, 13, 50, 86, 3, 7, 18]
    filter = BandPass('bpass(low_alpha=0.08, high_alpha=0.33)')

    for value in input_values:
        filter.calc(value)

    assert filter.last_calc_value() == pytest.approx(1.955, rel=0.01)

def test_bandpass_big_alphas():
    input_values = [10, 13, 50, 86, 3, 7, 18]
    filter = BandPass('bpass(low_alpha=0.001, high_alpha=0.89)')

    for value in input_values:
        filter.calc(value)

    assert filter.last_calc_value() == pytest.approx(0.00206, rel=0.01)

def test_notch():
    input_values = [10, 13, 50, 86, 3, 7, 18]
    filter = Notch('notch(low_alpha=0.08, high_alpha=0.33)')

    for value in input_values:
        filter.calc(value)

    assert filter.last_calc_value() == pytest.approx(16.04, rel=0.01)

def test_notch_big_alphas():
    input_values = [10, 13, 50, 86, 3, 7, 18]
    filter = Notch('notch(low_alpha=0.001, high_alpha=0.89)')

    for value in input_values:
        filter.calc(value)

    assert filter.last_calc_value() == pytest.approx(18, rel=0.01)

def test_highcut_cutting():
    value = 35
    filter = HighCut('hcut(cut=20)')

    assert filter.calc(value) == 20

def test_highcut_not_cutting():
    value = 16
    filter = HighCut('hcut(cut=20)')

    assert filter.calc(value) == value

def test_lowcut_cutting():
    value = 16
    filter = LowCut('lcut(cut=20)')

    assert filter.calc(value) == 20

def test_lowcut_not_cutting():
    value = 35
    filter = LowCut('lcut(cut=20)')

    assert filter.calc(value) == value
