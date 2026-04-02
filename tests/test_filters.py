import pytest  # pylint: disable=import-error

from src.pipeline.pipeline import Pipeline


def test_to_string_ndigits_eight():
    pipe = Pipeline('str(ndigits=8)')

    result = pipe.calc(123.123123123123123123)

    assert result == '123.12312312'
    assert pipe.last_calc_value_float() == 123.12312312


def test_to_string_ndigits_zero():
    pipe = Pipeline('str(ndigits=0)')

    result = pipe.calc(123.123123123123123123)

    assert result == '123'
    assert pipe.last_calc_value_float() == 123


def test_to_string_no_ndigits_parameter():
    pipe = Pipeline('str()')

    result = pipe.calc(123.123123123123123123)

    assert result == '123'
    assert pipe.last_calc_value_float() == 123


def test_to_string_ndigits_two():
    pipe = Pipeline('str(ndigits=2)')

    result = pipe.calc(123.123)

    assert result == '123.12'
    assert pipe.last_calc_value_float() == 123.12


def test_moving_average_filter_length():
    input_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    filter = Pipeline('mavg(n=5)')

    for value in input_values:
        filter.calc(value)

    assert filter.last_calc_value_float() == 8


def test_moving_average_filter():
    input_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    filter = Pipeline('mavg(n=11)')

    for value in input_values:
        filter.calc(value)

    assert filter.last_calc_value_float() == 5.5


def test_lowpass():
    input_values = [100, 1000]
    filter = Pipeline('lpass(alpha=0.1)')

    for value in input_values:
        filter.calc(value)

    assert filter.last_calc_value_float() == 109


def test_lowpass_big_alpha():
    input_values = [100, 1000]
    filter = Pipeline('lpass(alpha=0.4)')

    for value in input_values:
        filter.calc(value)

    assert filter.last_calc_value_float() == 424


def test_highpass():
    input_values = [100, 1000]
    filter = Pipeline('hpass(alpha=0.1)')

    for value in input_values:
        filter.calc(value)

    assert filter.last_calc_value_float() == 891


def test_highpass_big_alpha_minus_output():
    input_values = [100, -1000]
    filter = Pipeline('hpass(alpha=0.4)')

    for value in input_values:
        filter.calc(value)

    assert filter.last_calc_value_float() == -624


def test_highpass_big_alpha_plus_output():
    input_values = [100, 1000]
    filter = Pipeline('hpass(alpha=0.4)')

    for value in input_values:
        filter.calc(value)

    assert filter.last_calc_value_float() == 576


def test_bandpass():
    input_values = [10, 10000, 10]
    filter = Pipeline('bpass(low_alpha=0.05, high_alpha=0.2)')

    for value in input_values:
        filter.calc(value)

    assert filter.last_calc_value_float() == pytest.approx(300.6, rel=0.01)


def test_bandpass_big_alphas():
    input_values = [10, 10000, 10]
    filter = Pipeline('bpass(low_alpha=0.001, high_alpha=0.89)')

    for value in input_values:
        filter.calc(value)

    assert filter.last_calc_value_float() == pytest.approx(0.121, rel=0.01)


def test_notch():
    input_values = [10, 1000, 10]
    filter = Pipeline('notch(low_alpha=0.1, high_alpha=0.2)')

    for value in input_values:
        filter.calc(value)

    assert filter.last_calc_value_float() == -47.176


def test_notch_big_alphas():
    input_values = [10, 1000, 10]
    filter = Pipeline('notch(low_alpha=0.01, high_alpha=0.9)')

    for value in input_values:
        filter.calc(value)

    assert filter.last_calc_value_float() == pytest.approx(9.9, rel=0.01)


def test_highcut_cutting():
    value = 35
    filter = Pipeline('hcut(cut=20)')

    assert filter.calc(value) == 20


def test_highcut_cutting_minus():
    filter = Pipeline('hcut(cut=-888)')

    assert filter.calc(-800) == -888


def test_highcut_not_cutting():
    value = 16
    filter = Pipeline('hcut(cut=20)')

    assert filter.calc(value) == value


def test_highcut_cutting_minus_with_comma():
    value = 15
    filter = Pipeline('hcut(cut=-20.1)')

    assert filter.calc(value) == -20.1


def test_lowcut_cutting():
    value = 16
    filter = Pipeline('lcut(cut=20)')

    assert filter.calc(value) == 20


def test_lowcut_cutting_minus_with_comma():
    value = -50.3
    filter = Pipeline('lcut(cut=-20.1234)')

    assert filter.calc(value) == -20.1234


def test_lowcut_not_cutting():
    value = 35
    filter = Pipeline('lcut(cut=20)')

    assert filter.calc(value) == value


def test_lowcut_cutting_minus():
    filter = Pipeline('lcut(cut=-20)')

    assert filter.calc(-22) == -20
