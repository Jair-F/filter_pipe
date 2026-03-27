from src.pipeline.math_ops import Divide
from src.pipeline.pipeline import Pipeline


if __name__ == '__main__':
    pipeline = Pipeline(' mavg(n=10) | lpass(alpha=0.2) | str(ndigits=2)')
    print(F"pipeline: {pipeline.calc(2134.1231231)}")

    divider = Divide(' / 2')
    print(F"10/div: {divider.calc(10)}")

    print(F"value: {str(float(round(123.123, ndigits=2)))}")
    print(F"value: {str(123)}")
