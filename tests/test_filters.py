
from src.filters.filters import MovingAverage


def test_moving_average_filter_length():
    input_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    filter = MovingAverage(n=5)

    for value in input_values:
        filter.calc(value)
    
    assert filter.last_calc_value() == 8

def test_moving_average_filter_length():
    input_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    filter = MovingAverage(n=11)

    for value in input_values:
        filter.calc(value)
    
    assert filter.last_calc_value() == 5.5

