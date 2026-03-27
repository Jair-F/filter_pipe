from abc import abstractmethod
from typing import override
from collections import deque

import re


class Filter:
    def __init__(self):
        self._last_calc_value = 0

    def filter_matches(self, pipe:str)->bool:
        matches = re.match(self.regex_match_str(), pipe)
        return matches is not None

    def regex_match_str(self) -> str:
        return r"^filter\(n\=[0-9]+\)$" # https://regex101.com/

    def __repr__(self = None) -> str:
        return F"filter()"

    @abstractmethod
    def calc(self, value:float) -> float:
        self._last_calc_value = value
        return value
    
    def last_calc_value(self) -> float:
        return self._last_calc_value


class MovingAverage(Filter):
    def __init__(self, n = 10):
        super().__init__()
        self._n = n
        self._last_values = deque(maxlen=n)

    @override
    def regex_match_str(self) -> str:
        return r"^mavg\(n\=[0-9]+\)$"

    @override    
    def calc(self, value:float) -> float:
        self._last_values.append(value)
        result = sum(self._last_values) / len(self._last_values)
        super().calc(result)


class LowPass(Filter):
    def __init__(self, alpha=0.1):
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
    def __init__(self, alpha=0.1):
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
