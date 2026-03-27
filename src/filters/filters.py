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
        return r"^lpass\(n\=[0-9]+\)$"
    
    @override    
    def calc(self, value:float) -> float:
        result = (1 - self._alpha) * self.last_calc_value() + self._alpha * value
        super().calc(result)
