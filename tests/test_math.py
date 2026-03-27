from src.pipeline.math_ops import Divide, Multiply


def test_math_divide_no_spaces():
    pipe = Divide('/2')

    pipe.calc(10)

    assert pipe.last_calc_value_float() == 5

def test_math_divide_with_spaces_and_tabs():
    pipe = Divide('   \t /  \t2   \t  ')

    pipe.calc(10)

    assert pipe.last_calc_value_float() == 5

def test_math_multiply_no_spaces():
    pipe = Multiply('*2')

    pipe.calc(10)

    assert pipe.last_calc_value_float() == 20
