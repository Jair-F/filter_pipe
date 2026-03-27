
import pytest

from src.filters.filters import BandPass, HighPass, LowPass, MovingAverage


def test_moving_average_filter_length():
    input_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    filter = MovingAverage(n=5)

    for value in input_values:
        filter.calc(value)
    
    assert filter.last_calc_value() == 8

def test_moving_average_filter():
    input_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    filter = MovingAverage(n=11)

    for value in input_values:
        filter.calc(value)
    
    assert filter.last_calc_value() == 5.5

def test_lowpass():
    input_values = [10, 13, 50, 86, 3, 7, 18]
    filter = LowPass(alpha=0.05)

    for value in input_values:
        filter.calc(value)
    
    assert filter.last_calc_value() == pytest.approx(8, rel=0.01)

def test_lowpass_big_alpha():
    input_values = [10, 13, 50, 86, 3, 7, 18]
    filter = LowPass(alpha=0.34)

    for value in input_values:
        filter.calc(value)
    
    assert filter.last_calc_value() == pytest.approx(20.6, rel=0.001)

def test_highpass():
    input_values = [10, 13, 50, 86, 3, 7, 18]
    filter = HighPass(alpha=0.05)

    for value in input_values:
        filter.calc(value)
    
    assert filter.last_calc_value() == pytest.approx(10.03, rel=0.001)

def test_highpass_big_alpha_minus_output():
    input_values = [10, 13, 50, 86, 3, 7, 18]
    filter = HighPass(alpha=0.34)

    for value in input_values:
        filter.calc(value)
    
    assert filter.last_calc_value() == pytest.approx(-2.6, rel=0.001)

def test_highpass_big_alpha_plus_output():
    input_values = [110, 13, 50, 20, 3, 7, 49]
    filter = HighPass(alpha=0.34)

    for value in input_values:
        filter.calc(value)
    
    assert filter.last_calc_value() == pytest.approx(21.5, rel=0.001)

def test_bandpass():
    input_values = [10, 13, 50, 86, 3, 7, 18]
    filter = BandPass(low_alpha=0.08, high_alpha=0.33)

    for value in input_values:
        filter.calc(value)
    
    assert filter.last_calc_value() == pytest.approx(1.955, rel=0.01)

def test_bandpass_big_alphas():
    input_values = [10, 13, 50, 86, 3, 7, 18]
    filter = BandPass(low_alpha=0.001, high_alpha=0.89)

    for value in input_values:
        filter.calc(value)
    
    assert filter.last_calc_value() == pytest.approx(0.00206, rel=0.01)
