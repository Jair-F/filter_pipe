import inspect

from src.filters import filters


class Pipeline:
    def __init__(self, pipeline_str:str):
        self._filters:dict[str, filters.Filter] = self._build_filter_finder()
        self._pipeline = []

    def run(self):
        pass
    
    def is_valid_filter(self, pipe_chunk:str)->bool:
        pipe_chunk = pipe_chunk.strip()

        for filter in self._filters.values():
            if filter.valid_pipe(pipe_chunk):
                return True
        return False

    def _parse_and_build_pipline(self, pipeline_str:str)->None:
        pipeline_str = pipeline_str.strip().replace(' ', '').replace('\t', '')
        pipe_chunks = pipeline_str.split('|')

    def _build_filter_finder(self) -> dict[str, filters.Filter]:
        filter_classes = inspect.getmembers(filters, inspect.isclass)
        finder = {}
        for _, filter_type in filter_classes:
            filter_obj:filters.Filter = filter_type()
            finder[filter_obj.regex_match_str()] = filter_obj
        return finder

