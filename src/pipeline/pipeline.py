import inspect
import re

from src.filters import filters


class Pipeline:
    def __init__(self):
        self.filters:dict[str, filters.Filter] = self._build_filter_finder()

    def run(self):
        pass
    
    def is_valid_filter(self, pipe_chunk:str)->bool:
        pipe_chunk = pipe_chunk.strip()

        for filter in self.filters.values():
            if filter.filter_matches(pipe_chunk):
                return True
        return False

    def _build_filter_finder(self) -> dict[str, filters.Filter]:
        filter_classes = inspect.getmembers(filters, inspect.isclass)
        finder = {}
        for _, filter_type in filter_classes:
            filter_obj:filters.Filter = filter_type()
            finder[filter_obj.regex_match_str()] = filter_obj
        return finder

