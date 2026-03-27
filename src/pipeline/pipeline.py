import inspect
import re
import sys
from typing import Any

from src.filters import filters


class Pipeline:
    def __init__(self, pipeline_str:str):
        self._filters:dict[str, filters.Filter] = self._find_filter_classes()
        self._pipeline:list[filters.Filter] = []
        self._last_calc_value = 0

        self._build_pipline(pipeline_str)

    def calc(self, value:float) -> Any:
        result = value
        for pipe in self._pipeline:
            result = pipe.calc(result)
        return result

    def get_last_calc_value_float(self)->float:
        return self._last_calc_value

    def _is_valid_filter_pipe(self, pipe_chunk:str)->bool:
        pipe_chunk = pipe_chunk.strip()

        for filter in self._filters.values():
            if filter.valid_pipe(pipe_chunk):
                return True
        return False

    def _build_filter_from_pipe(self, single_pipe_chunk:str) -> filters.Filter:
        for regex_filter_match, filter_type in self._filters.items():
            if re.match(regex_filter_match, single_pipe_chunk):
                return filter_type(single_pipe_chunk)


    def _build_pipline(self, pipeline_str:str)->None:
        pipeline_str = pipeline_str.strip().replace(' ', '').replace('\t', '')
        pipe_chunks = pipeline_str.split('|')

        for chunk in pipe_chunks:
            chunk = chunk.strip()
            filter_obj = self._build_filter_from_pipe(chunk)
            if not filter_obj:
                print(F'filter: "{pipeline_str}" does not match any filter!!', file=sys.stderr)
                sys.exit(-1)
            self._pipeline.append(filter_obj)


    def _find_filter_classes(self) -> dict[str, filters.Filter]:
        filter_classes = inspect.getmembers(filters, inspect.isclass)
        finder = {}
        for _, filter_type in filter_classes:
            filter_obj:filters.Filter = filter_type()
            finder[filter_obj.regex_match_str()] = filter_type
        return finder
