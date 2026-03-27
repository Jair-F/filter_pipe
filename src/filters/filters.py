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

    @staticmethod
    def pipe_from_args() -> str:
        return F"filter()"

    def _extract_argument_float(self, pipe_str:str, argument:str)->float:
        argument += '='
        
        start_pos = re.search(argument, pipe_str).end()
        argument = pipe_str[start_pos:]
        end_pos = re.search(r'[,)]{1}', argument).end() - 1

        argument = argument[:end_pos]
        return float(argument)

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
        self._last_values = deque(maxlen=self._n)

    @staticmethod
    def pipe_from_args(n:int = 10) -> str:
        return F"mavg(n={n})"

    def _init_from_pipe_str(self, pipe_str:str)->None:
        super()._init_from_pipe_str(pipe_str)
        self._n = int(self._extract_argument_float(pipe_str, r'n'))

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
    def __init__(self, pipe_str:str):
        super().__init__()
        self._init_from_pipe_str(pipe_str)

    @staticmethod
    def pipe_from_args(alpha:float = 0.1) -> str:
        return F"lpass(alpha={alpha})"
    
    def _init_from_pipe_str(self, pipe_str:str)->None:
        super()._init_from_pipe_str(pipe_str)
        self._alpha = self._extract_argument_float(pipe_str, r'alpha')

    @override
    def regex_match_str(self) -> str:
        return r"^lpass\(alpha\=([0-9]*.?[0-9]+)\)$"
    
    @override    
    def calc(self, value:float) -> float:
        result = (1 - self._alpha) * self.last_calc_value() + self._alpha * value
        super().calc(result)
        return result

class HighPass(Filter):
    def __init__(self, pipe_str:str):
        super().__init__()
        alpha = self._init_from_pipe_str(pipe_str)
        self._low_pass = LowPass(LowPass.pipe_from_args(alpha=alpha))

    @staticmethod
    def pipe_from_args(alpha:float = 0.1) -> str:
        return F"hpass(alpha={alpha})"

    def _init_from_pipe_str(self, pipe_str:str)-> float:
        super()._init_from_pipe_str(pipe_str)
        return self._extract_argument_float(pipe_str, r'alpha')

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
    def __init__(self, pipe_str:str):
        super().__init__()
        low_alpha, high_alpha = self._init_from_pipe_str(pipe_str)
        self._low_pass = LowPass(LowPass.pipe_from_args(low_alpha))
        self._high_pass = HighPass(HighPass.pipe_from_args(high_alpha))

    @staticmethod
    def pipe_from_args(low_alpha:float = 0.1, high_alpha:float = 0.5) -> str:
        return F"bpass(low_alpha={low_alpha},high_alpha={high_alpha})"

    def _init_from_pipe_str(self, pipe_str:str)-> tuple[float, float]:
        super()._init_from_pipe_str(pipe_str)
        low_alpha = self._extract_argument_float(pipe_str, r'low_alpha')
        high_alpha = self._extract_argument_float(pipe_str, r'high_alpha')
        return low_alpha, high_alpha

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
    def __init__(self, pipe_str:str):
        super().__init__()
        low_alpha, high_alpha = self._init_from_pipe_str(pipe_str)
        self._band_pass = BandPass(BandPass.pipe_from_args(low_alpha=low_alpha, high_alpha=high_alpha))

    @staticmethod
    def pipe_from_args(low_alpha:float = 0.1, high_alpha:float = 0.5) -> str:
        return F"notch(low_alpha={low_alpha},high_alpha={high_alpha})"

    def _init_from_pipe_str(self, pipe_str:str)-> tuple[float, float]:
        super()._init_from_pipe_str(pipe_str)
        low_alpha = self._extract_argument_float(pipe_str, r'low_alpha')
        high_alpha = self._extract_argument_float(pipe_str, r'high_alpha')
        return low_alpha, high_alpha

    @override
    def regex_match_str(self) -> str:
        return r"^notch\(low_alpha\=([0-9]*.?[0-9]+), *high_alpha\=([0-9]*.?[0-9]+)\)$"
    
    @override    
    def calc(self, value:float) -> float:
        band_to_remove = self._band_pass.calc(value)
        result = value - band_to_remove
        super().calc(result)
        return result

class HighCut(Filter):
    def __init__(self, pipe_str:str):
        super().__init__()
        self._init_from_pipe_str(pipe_str)

    @staticmethod
    def pipe_from_args(cut:float = 0.1) -> str:
        return F"hcut(cut={cut})"

    def _init_from_pipe_str(self, pipe_str:str)-> None:
        super()._init_from_pipe_str(pipe_str)
        self._cut_value = self._extract_argument_float(pipe_str, r'cut')

    @override
    def regex_match_str(self) -> str:
        return r"^hcut\(cut\=([0-9]*.?[0-9]+)\)$"
    
    @override    
    def calc(self, value:float) -> float:
        result = min(self._cut_value, value)
        super().calc(result)
        return result

class LowCut(Filter):
    def __init__(self, pipe_str:str):
        super().__init__()
        self._init_from_pipe_str(pipe_str)

    @staticmethod
    def pipe_from_args(cut:float = 0.1) -> str:
        return F"lcut(cut={cut})"

    def _init_from_pipe_str(self, pipe_str:str)-> None:
        super()._init_from_pipe_str(pipe_str)
        self._cut_value = self._extract_argument_float(pipe_str, r'cut')


    @override
    def regex_match_str(self) -> str:
        return r"^lcut\(cut\=([0-9]*.?[0-9]+)\)$"
    
    @override    
    def calc(self, value:float) -> float:
        result = max(self._cut_value, value)
        super().calc(result)
        return result
