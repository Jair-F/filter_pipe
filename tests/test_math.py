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
