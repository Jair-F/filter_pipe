from abc import abstractmethod
import sys
from typing import override
from collections import deque

import re


class Filter:
    def __init__(self):
        self._last_calc_value = 0

    def valid_pipe(self, pipe:str)->bool:
        matches = re.match(self.regex_match_str(), pipe)
        return matches is not None

    def regex_match_str(self) -> str:
        return r"^filter\(n\=[0-9]+\)$" # https://regex101.com/

    def __repr__(self = None) -> str:
        return F"filter()"

    def _init_from_pipe_str(self, pipe_str:str)->None:
        if not self.valid_pipe(pipe_str):
            print(F"pipe: {pipe_str} does not match {self.regex_match_str()} - exiting", file=sys.stderr)
            sys.exit(-1)

    @abstractmethod
    def calc(self, value:float) -> float:
        self._last_calc_value = value
        return value
    
    def last_calc_value(self) -> float:
        return self._last_calc_value


class MovingAverage(Filter):
    def __init__(self, pipe_str:str):
        super().__init__()
        self._init_from_pipe_str(pipe_str)
        self._last_values = deque(maxlen=self.n)

    def _init_from_pipe_str(self, pipe_str:str)->None:
        super()._init_from_pipe_str(pipe_str)

        pipe_str = pipe_str.split('(')[1]
        pipe_str = pipe_str.split(')')[0]
        
        n_start_pos = re.match(r'n=', pipe_str).end()
        self.n = int(pipe_str[n_start_pos:])

    @override
    def regex_match_str(self) -> str:
        return r"^mavg\(n\=[0-9]+\)$"

    @override    
    def calc(self, value:float) -> float:
        self._last_values.append(value)
        result = sum(self._last_values) / len(self._last_values)
        super().calc(result)
        return result


class LowPass(Filter):
    def __init__(self, alpha:float=0.1):
        super().__init__()
        self._alpha = alpha

    @override
    def regex_match_str(self) -> str:
        return r"^lpass\(alpha\=([0-9]*.?[0-9]+)\)$"
    
    @override    
    def calc(self, value:float) -> float:
        result = (1 - self._alpha) * self.last_calc_value() + self._alpha * value
        super().calc(result)
        return result

class HighPass(Filter):
    def __init__(self, alpha:float=0.1):
        super().__init__()
        self._low_pass = LowPass(alpha)

    @override
    def regex_match_str(self) -> str:
        return r"^hpass\(alpha\=([0-9]*.?[0-9]+)\)$"
    
    @override    
    def calc(self, value:float) -> float:
        lpf = self._low_pass.calc(value)
        result = value - lpf
        super().calc(result)
        return result

class BandPass(Filter):
    def __init__(self, low_alpha=0.1, high_alpha=0.5):
        super().__init__()
        self._low_pass = LowPass(low_alpha)
        self._high_pass = HighPass(high_alpha)

    @override
    def regex_match_str(self) -> str:
        return r"^bpass\(low_alpha\=([0-9]*.?[0-9]+), *high_alpha\=([0-9]*.?[0-9]+)\)$"
    
    @override    
    def calc(self, value:float) -> float:
        lpf = self._low_pass.calc(value)
        result = self._high_pass.calc(lpf)
        super().calc(result)
        return result

class Notch(Filter):
    def __init__(self, low_alpha=0.1, high_alpha=0.5):
        super().__init__()
        self._band_pass = BandPass(low_alpha=low_alpha, high_alpha=high_alpha)

    @override
    def regex_match_str(self) -> str:
        return r"^bpass\(low_alpha\=([0-9]*.?[0-9]+), *high_alpha\=([0-9]*.?[0-9]+)\)$"
    
    @override    
    def calc(self, value:float) -> float:
        band_to_remove = self._band_pass.calc(value)
        result = value - band_to_remove
        super().calc(result)
        return result

class HighCut(Filter):
    def __init__(self, cut_value = 0.1):
        super().__init__()
        self._cut_value = cut_value

    @override
    def regex_match_str(self) -> str:
        return r"^hcut\(cut\=([0-9]*.?[0-9]+)\)$"
    
    @override    
    def calc(self, value:float) -> float:
        result = min(self._cut_value, value)
        super().calc(result)
        return result

class LowCut(Filter):
    def __init__(self, cut_value = 0.1):
        super().__init__()
        self._cut_value = cut_value

    @override
    def regex_match_str(self) -> str:
        return r"^lcut\(cut\=([0-9]*.?[0-9]+)\)$"
    
    @override    
    def calc(self, value:float) -> float:
        result = max(self._cut_value, value)
        super().calc(result)
        return result
