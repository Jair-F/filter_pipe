from src.pipeline.pipeline import Pipeline


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
    pipe = Pipeline(' mavg(n=10) |    mavg(n=5) ')

    for value in input_values:
        pipe.calc(value)

    assert pipe.last_calc_value_float() == 4.5


def test_pipeline_with_math_divide_and_filter_combined():
    pipe = Pipeline('/2|hpass(alpha=10)')

    pipe.calc(2134)

    assert pipe.last_calc_value_float() == -9603


def test_pipeline_with_math_with_filters_combined():
    pipe = Pipeline('+2.3 | -4.3 | *-12.5 | / -2 | lcut(cut=-123)')
    pipe.calc(-124)
    assert pipe.last_calc_value_float() == -123


def test_pipeline_with_math_with_filters_combined_converting_to_str():
    pipe = Pipeline('+2.3 | -4.3 | *-12.5 | / -2 | hcut(cut=-123.345) | str(ndigits=2)')
    result = pipe.calc(50.123)
    assert result == '-123.34'
    assert pipe.last_calc_value_float() == -123.34
