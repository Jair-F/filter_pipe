import pytest

from src.pipeline.pipeline import Pipeline


def test_pipeline_math_divide_no_spaces():
    pipe = Pipeline('/2')
    pipe.calc(10)
    assert pipe.last_calc_value_float() == 5


def test_pipeline_math_divide__minus_comma():
    pipe = Pipeline('/-2.5')
    pipe.calc(10)
    assert pipe.last_calc_value_float() == -4


def test_pipeline_math_divide_with_comma_no_spaces():
    pipe = Pipeline('/2.2')
    pipe.calc(22)
    assert pipe.last_calc_value_float() == 10


def test_pipeline_math_multiply_no_spaces():
    pipe = Pipeline('*2')
    pipe.calc(10)
    assert pipe.last_calc_value_float() == 20


def test_pipeline_math_multiply_minus_comma():
    pipe = Pipeline('*-2.5')
    pipe.calc(10)
    assert pipe.last_calc_value_float() == -25


def test_pipeline_math_multiply_with_comma_no_spaces():
    pipe = Pipeline('*2.2')
    pipe.calc(10)
    assert pipe.last_calc_value_float() == 22


def test_pipeline_math_add_with_comma_no_spaces():
    pipe = Pipeline('+2.2')
    pipe.calc(10)
    assert pipe.last_calc_value_float() == 12.2


def test_pipeline_math_add_no_comma_no_spaces():
    pipe = Pipeline('+234')
    pipe.calc(10)
    assert pipe.last_calc_value_float() == 244


def test_pipeline_math_subtract_with_comma_no_spaces():
    pipe = Pipeline('-2.2')
    pipe.calc(10)
    assert pipe.last_calc_value_float() == 7.8


def test_pipeline_math_subtract_no_comma_no_spaces():
    pipe = Pipeline('-234')
    pipe.calc(10)
    assert pipe.last_calc_value_float() == -224


def test_pipeline_math_divide_with_spaces_and_tabs():
    pipe = Pipeline('   \t /  \t2   \t  ')
    pipe.calc(10)
    assert pipe.last_calc_value_float() == 5


def test_pipeline_with_spaces_and_tabs():
    pipe = Pipeline(' \t  lpass(alpha=0.2)   |  \t  lpass(alpha=0.2) \t ')

    pipe.calc(100)

    assert pipe.last_calc_value_float() == 4


def test_pipeline_without_any_space():
    pipe = Pipeline('hpass(alpha=0.8)|lpass(alpha=0.2)')

    pipe.calc(2134)

    assert pipe.last_calc_value_float() == 85.36


def test_pipeline_two_filters_moving_average_low_pass_multiple_input_values():
    input_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    pipe = Pipeline(' mavg(n=10) |    lpass(alpha=0.2) ')

    for value in input_values:
        pipe.calc(value)

    assert pipe.last_calc_value_float() == pytest.approx(3.6610612736000006)


def test_pipeline_with_math_divide_and_filters_combined():
    pipe = Pipeline(
        '/2|hpass(alpha=10)|lpass(alpha=0.2)|bpass(low_alpha=0.2,high_alpha=0.3)',
    )

    pipe.calc(2134)

    assert pipe.last_calc_value_float() == -268.884


def test_pipeline_with_math_multiply_and_filters_combined():
    pipe = Pipeline('/2|notch(low_alpha=0.25,high_alpha=0.1)')

    pipe.calc(2134)

    assert pipe.last_calc_value_float() == 826.925


def test_pipeline_with_math_with_filters_combined():
    pipe = Pipeline('+2.3 | -4.3 | *-12.5 | / -2 | lcut(cut=-123)')
    pipe.calc(-124)
    assert pipe.last_calc_value_float() == -123


def test_pipeline_with_math_with_filters_combined_converting_to_str():
    pipe = Pipeline('+2.3 | -4.3 | *-12.5 | / -2 | hcut(cut=-123.345) | str(ndigits=2)')
    result = pipe.calc(50.123)
    assert result == '-123.34'
    assert pipe.last_calc_value_float() == -123.34
