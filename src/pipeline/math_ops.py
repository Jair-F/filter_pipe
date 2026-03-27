from typing import override

from src.pipeline.pipe import PipeChunk


class Divide(PipeChunk):
    @staticmethod
    def pipe_from_args(divider: float = 1.0) -> str:
        return f'/{divider}'

    def __init__(self, pipe_str: str = pipe_from_args()):
        super().__init__()
        self._init_from_pipe_str(pipe_str)

    def _init_from_pipe_str(self, pipe_str: str) -> None:
        super()._init_from_pipe_str(pipe_str)
        self._divider = self._extract_argument_float(pipe_str, r'\/')

    @override
    def regex_match_str(self) -> str:
        return r'^\/[+-]*(\d*.?\d+)$'

    @override
    def calc(self, value: float) -> float:
        result = value / self._divider
        super().calc(result)
        return result


class Multiply(PipeChunk):
    @staticmethod
    def pipe_from_args(multiplier: float = 1.0) -> str:
        return f'*{multiplier}'

    def __init__(self, pipe_str: str = pipe_from_args()):
        super().__init__()
        self._init_from_pipe_str(pipe_str)

    def _init_from_pipe_str(self, pipe_str: str) -> None:
        super()._init_from_pipe_str(pipe_str)
        self._multiplier = self._extract_argument_float(pipe_str, r'\*')

    @override
    def regex_match_str(self) -> str:
        return r'^\*[+-]*(\d*.?\d+)$'

    @override
    def calc(self, value: float) -> float:
        result = value * self._multiplier
        super().calc(result)
        return result


class Add(PipeChunk):
    @staticmethod
    def pipe_from_args(add: float = 0.0) -> str:
        return f'+{add}'

    def __init__(self, pipe_str: str = pipe_from_args()):
        super().__init__()
        self._init_from_pipe_str(pipe_str)

    def _init_from_pipe_str(self, pipe_str: str) -> None:
        super()._init_from_pipe_str(pipe_str)
        self._add = self._extract_argument_float(pipe_str, r'\+')

    @override
    def regex_match_str(self) -> str:
        return r'^\+(\d*.?\d+)$'

    @override
    def calc(self, value: float) -> float:
        result = value + self._add
        super().calc(result)
        return result


class Subtract(PipeChunk):
    @staticmethod
    def pipe_from_args(subtract: float = 0.0) -> str:
        return f'-{subtract}'

    def __init__(self, pipe_str: str = pipe_from_args()):
        super().__init__()
        self._init_from_pipe_str(pipe_str)

    def _init_from_pipe_str(self, pipe_str: str) -> None:
        super()._init_from_pipe_str(pipe_str)
        self._subtract = self._extract_argument_float(pipe_str, r'\-')

    @override
    def regex_match_str(self) -> str:
        return r'^\-(\d*.?\d+)$'

    @override
    def calc(self, value: float) -> float:
        result = value - self._subtract
        super().calc(result)
        return result
