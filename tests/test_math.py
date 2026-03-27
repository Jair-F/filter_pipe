from src.pipeline.math_ops import Add, Divide, Multiply


def test_math_divide_no_spaces():
    pipe = Divide('/2')

    pipe.calc(10)

    assert pipe.last_calc_value_float() == 5

def test_math_divide_with_comma_no_spaces():
    pipe = Divide('/2.2')

    pipe.calc(22)

    assert pipe.last_calc_value_float() == 10

def test_math_divide_with_spaces_and_tabs():
    pipe = Divide('   \t /  \t2   \t  ')

    pipe.calc(10)

    assert pipe.last_calc_value_float() == 5

def test_math_multiply_no_spaces():
    pipe = Multiply('*2')
    pipe.calc(10)
    assert pipe.last_calc_value_float() == 20

def test_math_multiply_with_comma_no_spaces():
    pipe = Multiply('*2.2')
    pipe.calc(10)
    assert pipe.last_calc_value_float() == 22

def test_math_add_with_comma_no_spaces():
    pipe = Add('+2.2')

    pipe.calc(10)

    assert pipe.last_calc_value_float() == 12.2

def test_math_add_no_comma_no_spaces():
    pipe = Add('+234')

    pipe.calc(10)

    assert pipe.last_calc_value_float() == 244
