import collections
import re
import typing

from src.pipeline.pipe import PipeChunk


class Filter(PipeChunk):
    @staticmethod
    def pipe_from_args() -> str:
        return 'filter()'

    @typing.override
    def _extract_argument_float(self, pipe_str: str, argument: str) -> float:
        argument += r'\='

        tmp_match: re.Match[str] | None = re.search(argument, pipe_str)
        start_pos = tmp_match.end() if tmp_match else None

        argument = pipe_str[start_pos:]
        tmp_match = re.search(r'[\,\)]{1}', argument)
        end_pos = tmp_match.end() - 1 if tmp_match else None

        argument = argument[:end_pos]
        return float(argument)

    @typing.override
    def regex_match_str(self) -> str:
        return r'^filter\(\)$'


class ToString(Filter):
    @staticmethod
    def pipe_from_args(ndigits: int = 1) -> str:
        return f'str(ndigits={ndigits})'

    def __init__(self, pipe_str: str = pipe_from_args()):
        super().__init__()
        self._init_from_pipe_str(pipe_str)

    @typing.override
    def _init_from_pipe_str(self, pipe_str: str) -> None:
        super()._init_from_pipe_str(pipe_str)
        if pipe_str.find('ndigits') > 0:
            self._ndigits = int(self._extract_argument_float(pipe_str, r'ndigits'))
        else:
            self._ndigits = 0

    @typing.override
    def regex_match_str(self) -> str:
        return r'^str\((ndigits=\d+)?\)$'

    @typing.override
    def calc(self, value: float) -> str:
        self._last_calc_value = round(value, ndigits=self._ndigits)
        if self._last_calc_value.is_integer():
            return str(int(self._last_calc_value))
        return str(self._last_calc_value)


class MovingAverage(Filter):
    @staticmethod
    def pipe_from_args(n: int = 10) -> str:
        return f'mavg(n={n})'

    def __init__(self, pipe_str: str = pipe_from_args()):
        super().__init__()
        self._init_from_pipe_str(pipe_str)
        self._last_values: collections.deque[float] = collections.deque(maxlen=self._n)

    @typing.override
    def _init_from_pipe_str(self, pipe_str: str) -> None:
        super()._init_from_pipe_str(pipe_str)
        self._n = int(self._extract_argument_float(pipe_str, r'n'))

    @typing.override
    def regex_match_str(self) -> str:
        return r'^mavg\(n\=\d+\)$'

    @typing.override
    def calc(self, value: float) -> float:
        self._last_values.append(value)
        result = sum(self._last_values) / len(self._last_values)
        super().calc(result)
        return result


class LowPass(Filter):
    @staticmethod
    def pipe_from_args(alpha: float = 0.1) -> str:
        return f'lpass(alpha={alpha})'

    def __init__(self, pipe_str: str = pipe_from_args()):
        super().__init__()
        self._init_from_pipe_str(pipe_str)

    @typing.override
    def _init_from_pipe_str(self, pipe_str: str) -> None:
        super()._init_from_pipe_str(pipe_str)
        self._alpha = self._extract_argument_float(pipe_str, r'alpha')

    @typing.override
    def regex_match_str(self) -> str:
        return r'^lpass\(alpha\=(\d*.?\d+)\)$'

    @typing.override
    def calc(self, value: float) -> float:
        result = (1 - self._alpha) * self.last_calc_value_float() + self._alpha * value
        super().calc(result)
        return result


class HighPass(Filter):
    @staticmethod
    def pipe_from_args(alpha: float = 0.1) -> str:
        return f'hpass(alpha={alpha})'

    def __init__(self, pipe_str: str = pipe_from_args()):
        super().__init__()
        alpha = self._init_from_pipe_str(pipe_str)
        self._low_pass = LowPass(LowPass.pipe_from_args(alpha=alpha))

    @typing.override
    def _init_from_pipe_str(self, pipe_str: str) -> float:
        super()._init_from_pipe_str(pipe_str)
        return self._extract_argument_float(pipe_str, r'alpha')

    @typing.override
    def regex_match_str(self) -> str:
        return r'^hpass\(alpha\=(\d*.?\d+)\)$'

    @typing.override
    def calc(self, value: float) -> float:
        lpf = self._low_pass.calc(value)
        result = value - lpf
        super().calc(result)
        return result


class BandPass(Filter):
    @staticmethod
    def pipe_from_args(low_alpha: float = 0.1, high_alpha: float = 0.5) -> str:
        return f'bpass(low_alpha={low_alpha},high_alpha={high_alpha})'

    def __init__(self, pipe_str: str = pipe_from_args()):
        super().__init__()
        low_alpha, high_alpha = self._init_from_pipe_str(pipe_str)
        self._low_pass = LowPass(LowPass.pipe_from_args(low_alpha))
        self._high_pass = HighPass(HighPass.pipe_from_args(high_alpha))

    @typing.override
    def _init_from_pipe_str(self, pipe_str: str) -> tuple[float, float]:
        super()._init_from_pipe_str(pipe_str)
        low_alpha = self._extract_argument_float(pipe_str, r'low_alpha')
        high_alpha = self._extract_argument_float(pipe_str, r'high_alpha')
        return low_alpha, high_alpha

    @typing.override
    def regex_match_str(self) -> str:
        return r'^bpass\(low_alpha\=(\d*.?\d+), *high_alpha\=(\d*.?\d+)\)$'

    @typing.override
    def calc(self, value: float) -> float:
        lpf = self._low_pass.calc(value)
        result = self._high_pass.calc(lpf)
        super().calc(result)
        return result


class Notch(Filter):
    @staticmethod
    def pipe_from_args(low_alpha: float = 0.1, high_alpha: float = 0.5) -> str:
        return f'notch(low_alpha={low_alpha},high_alpha={high_alpha})'

    def __init__(self, pipe_str: str = pipe_from_args()):
        super().__init__()
        low_alpha, high_alpha = self._init_from_pipe_str(pipe_str)
        self._band_pass = BandPass(
            BandPass.pipe_from_args(low_alpha=low_alpha, high_alpha=high_alpha),
        )

    @typing.override
    def _init_from_pipe_str(self, pipe_str: str) -> tuple[float, float]:
        super()._init_from_pipe_str(pipe_str)
        low_alpha = self._extract_argument_float(pipe_str, r'low_alpha')
        high_alpha = self._extract_argument_float(pipe_str, r'high_alpha')
        return low_alpha, high_alpha

    @typing.override
    def regex_match_str(self) -> str:
        return r'^notch\(low_alpha\=(\d*.?\d+), *high_alpha\=(\d*.?\d+)\)$'

    @typing.override
    def calc(self, value: float) -> float:
        band_to_remove = self._band_pass.calc(value)
        result = value - band_to_remove
        super().calc(result)
        return result


class HighCut(Filter):
    @staticmethod
    def pipe_from_args(cut: float = 0.1) -> str:
        return f'hcut(cut={cut})'

    def __init__(self, pipe_str: str = pipe_from_args()):
        super().__init__()
        self._init_from_pipe_str(pipe_str)

    @typing.override
    def _init_from_pipe_str(self, pipe_str: str) -> None:
        super()._init_from_pipe_str(pipe_str)
        self._cut_value = self._extract_argument_float(pipe_str, r'cut')

    @typing.override
    def regex_match_str(self) -> str:
        return r'^hcut\(cut\=([+-]?\d*.?\d+)\)$'

    @typing.override
    def calc(self, value: float) -> float:
        result = min(self._cut_value, value)
        super().calc(result)
        return result


class LowCut(Filter):
    @staticmethod
    def pipe_from_args(cut: float = 0.1) -> str:
        return f'lcut(cut={cut})'

    def __init__(self, pipe_str: str = pipe_from_args()):
        super().__init__()
        self._init_from_pipe_str(pipe_str)

    @typing.override
    def _init_from_pipe_str(self, pipe_str: str) -> None:
        super()._init_from_pipe_str(pipe_str)
        self._cut_value = self._extract_argument_float(pipe_str, r'cut')

    @typing.override
    def regex_match_str(self) -> str:
        return r'^lcut\(cut\=([+-]?\d*.?\d+)\)$'

    @typing.override
    def calc(self, value: float) -> float:
        result = max(self._cut_value, value)
        super().calc(result)
        return result
