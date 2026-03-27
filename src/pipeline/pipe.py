import abc
import re
import sys


class PipeChunk:
    @staticmethod
    def pipe_from_args() -> str:
        return F"pipe"

    def __init__(self):
        self._last_calc_value = 0

    def valid_pipe(self, pipe:str)->bool:
        matches = re.match(self.regex_match_str(), pipe)
        return matches is not None

    def _extract_argument_float(self, pipe_str:str, argument:str)->float:
        pipe_str = pipe_str.strip().replace(' ', '').replace('\t', '')

        start_pos = re.search(argument, pipe_str).end()
        argument = pipe_str[start_pos:]
        end_pos = re.search(r'[^\d.+-]', argument)
        if not end_pos:
            end_pos = len(argument)
        else:
            end_pos = end_pos.end() - 1

        argument = argument[:end_pos]
        return float(argument)

    def regex_match_str(self) -> str:
        return r'^pipe$' # https://regex101.com/

    def _init_from_pipe_str(self, pipe_str:str)->None:
        pipe_str = pipe_str.strip().replace(' ', '').replace('\t', '')
        if not self.valid_pipe(pipe_str):
            print(F"pipe: {pipe_str} does not match {self.regex_match_str()} - exiting", file=sys.stderr)
            sys.exit(-1)

    @abc.abstractmethod
    def calc(self, value:float) -> float:
        self._last_calc_value = value
        return value

    def last_calc_value_float(self) -> float:
        return self._last_calc_value
