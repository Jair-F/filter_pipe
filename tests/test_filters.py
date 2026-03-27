
import pytest

from src.filters.filters import LowPass, MovingAverage


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
    input_values = [10, 20, 50, 86, 3, 23, 18]
    filter = LowPass(alpha=0.05)

    for value in input_values:
        filter.calc(value)
    
    assert filter.last_calc_value() == pytest.approx(9, rel=0.001)

def test_lowpass_big_alpha():
    input_values = [10, 20, 50, 86, 3, 23, 18]
    filter = LowPass(alpha=0.34)

    for value in input_values:
        filter.calc(value)
    
    assert filter.last_calc_value() == pytest.approx(24.5, rel=0.001)


