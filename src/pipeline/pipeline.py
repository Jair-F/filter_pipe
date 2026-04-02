import inspect
import re
import sys

from src.pipeline import filters
from src.pipeline import math_ops
from src.pipeline.pipe import PipeChunk


class Pipeline:
    def __init__(self, pipeline_str: str):
        self._filters: dict[str, type[PipeChunk]] = self._find_pipe_chunk_classes(
            filters,
        )
        self._math_ops: dict[str, type[PipeChunk]] = self._find_pipe_chunk_classes(math_ops)
        self._pipeline: list[PipeChunk] = []
        self._last_calc_value: float = 0.0

        self._build_pipline(pipeline_str)

    def calc(self, value: float) -> float | str:
        result: float | str = value
        for pipe in self._pipeline:
            result = pipe.calc(float(result))
            self._last_calc_value = float(result)
        return result

    def last_calc_value_float(self) -> float:
        return self._last_calc_value

    def _build_pipe_chunk_from_pipe(self, single_pipe_chunk: str) -> PipeChunk | None:
        combined_lists = self._filters | self._math_ops

        for regex_filter_match, filter_type in combined_lists.items():
            if re.match(regex_filter_match, single_pipe_chunk):
                filter_obj: PipeChunk = filter_type(single_pipe_chunk)
                return filter_obj
        return None

    def _build_pipline(self, pipeline_str: str) -> None:
        pipeline_str = pipeline_str.strip().replace(' ', '').replace('\t', '')
        pipe_chunks = pipeline_str.split('|')

        for chunk in pipe_chunks:
            chunk = chunk.strip()
            filter_obj = self._build_pipe_chunk_from_pipe(chunk)
            if not filter_obj:
                print(
                    f'filter: "{pipeline_str}" does not match any filter!!',
                    file=sys.stderr,
                )
                sys.exit(-1)
            self._pipeline.append(filter_obj)

    def _find_pipe_chunk_classes(self, module: object) -> dict[str, type[PipeChunk]]:
        filter_classes: list[tuple[str, type[PipeChunk]]] = inspect.getmembers(
            module,
            inspect.isclass,
        )
        finder: dict[str, type[PipeChunk]] = {}
        for _, filter_type in filter_classes:
            filter_obj: PipeChunk = filter_type()
            finder[filter_obj.regex_match_str()] = filter_type
        return finder
