from src.pipeline.math import Divide
from src.pipeline.pipeline import Pipeline


if __name__ == '__main__':
    pipeline = Pipeline(' mavg(n=10) | lpass(alpha=0.2) ')
    print(F"pipeline: {pipeline.calc(2134)}")

    divider = Divide(' / 2')
    print(F"10/div: {divider.calc(10)}")
