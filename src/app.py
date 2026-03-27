from src.pipeline.math_ops import Divide
from src.pipeline.pipeline import Pipeline

if __name__ == '__main__':
    pipeline = Pipeline(' mavg(n=10) | lpass(alpha=0.2) | str(ndigits=2)')
    print(f'pipeline: {pipeline.calc(2134.1231231)}')

    divider = Divide(' / 2')
    print(f'10/div: {divider.calc(10)}')

    print(f'value: {str(float(round(123.123, ndigits=2)))}')
    print(f'value: {str(123)}')
