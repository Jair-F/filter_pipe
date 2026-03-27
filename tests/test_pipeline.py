

import pytest

from src.pipeline.pipeline import Pipeline


def test_pipeline_one_filter_moving_average():
    input_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    pipe = Pipeline('mavg(n=5)')

    for value in input_values:
        pipe.calc(value)

    assert pipe.last_calc_value_float() == 8

def test_pipeline_two_filters_moving_average_low_pass_single_input_value():
    pipe = Pipeline(' mavg(n=10) | lpass(alpha=0.2) ')

    pipe.calc(2134)

    assert pipe.last_calc_value_float() == 426.8

def test_pipeline_with_spaces_and_tabs():
    pipe = Pipeline(' \t  mavg(n=10)   |  \t  lpass(alpha=0.2) \t ')

    pipe.calc(2134)

    assert pipe.last_calc_value_float() == 426.8

def test_pipeline_without_any_space():
    pipe = Pipeline('mavg(n=10)|lpass(alpha=0.2)')

    pipe.calc(2134)

    assert pipe.last_calc_value_float() == 426.8

def test_pipeline_two_filters_moving_average_low_pass_multiple_input_values():
    input_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    pipe = Pipeline(' mavg(n=10) |    lpass(alpha=0.2) ')

    for value in input_values:
        pipe.calc(value)

    assert pipe.last_calc_value_float() == pytest.approx(3.6610612736000006)

def test_pipeline_with_math_divide_and_filters_combined():
    pipe = Pipeline('/2|hpass(alpha=10)|lpass(alpha=0.2)|bpass(low_alpha=0.2,high_alpha=0.3)')

    pipe.calc(2134)

    assert pipe.last_calc_value_float() == -268.884

def test_pipeline_with_math_multiply_and_filters_combined():
    pipe = Pipeline('/2|notch(low_alpha=0.25,high_alpha=0.1)')

    pipe.calc(2134)

    assert pipe.last_calc_value_float() == 826.925
