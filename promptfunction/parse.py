from abc import ABC, abstractmethod
from typing import Any

from langchain.schema import BaseOutputParser, T

from promptfunction.magic_phrase import PHRASE_DONT_EXPLAIN


class ResponseTypeFormatter(BaseOutputParser, ABC):
    return_annotation: Any = None

    @classmethod
    @abstractmethod
    def check_response(cls, parameters, return_type):
        pass


def get_return_parser(return_type: Any) -> ResponseTypeFormatter:
    subclasses = ResponseTypeFormatter.__subclasses__()

    for subclass in list(subclasses):
        if subclass.check_response(return_type):
            return subclass(return_annotation=return_type)

    raise Exception(f"Could not find a return parser for type {return_type}")


class NumberParse(ResponseTypeFormatter):

    def parse(self, text: str) -> T:
        try:
            return self.return_annotation(text)
        except ValueError as e:
            raise Exception(f"Could not parse response as type. Response: '{text}'.  Error from parsing:"
                            f" '{repr(e)}'")

    def get_format_instructions(self) -> str:
        return f"Respond only with {self.return_annotation.__name__}. Never say anything else or add any punctuation.{PHRASE_DONT_EXPLAIN}.\n"

    @classmethod
    def check_response(cls, return_type):
        return isinstance(return_type, type) and issubclass(return_type, (int, float))
