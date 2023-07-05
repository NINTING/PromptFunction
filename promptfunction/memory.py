from typing import NamedTuple, List, Callable, TypeVar, Dict, Any, Union

from langchain.schema import BaseMemory

T = TypeVar('T', bound=NamedTuple)

M = TypeVar("M", bound=Union[str, list[str], list[tuple[str, type]]])


class MemoryModel:
    scheme: T
    formatter: Callable[[T], str]

    def __init__(self, fields: M, formatter):
        self.scheme = NamedTuple("scheme", fields)
        self.formatter = formatter

    def variable_names(self) -> tuple[str]:
        print('aaa')
        return self.scheme._fields


class WorkMemory(BaseMemory):
    model: MemoryModel = None
    _data: List[T] = []
    _load_memory_callback: Callable[[List[T]], str] = None
    model_variables: List[str] = None

    @classmethod
    def create_by_fields(cls, fields: M, formatter: Callable[[T], str], load_memory: Callable[[], None] = None):
        model = MemoryModel(fields=fields, formatter=formatter)
        return cls(model=model, _load_memory_callback=load_memory)

    @classmethod
    def create_by_model(cls, model: MemoryModel, load_memory: Callable[[], None] = None):
        return cls(model=model, _load_memory_callback=load_memory)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_variables = self.model.variable_names()

    def default_load_memory(self) -> Dict[str, Any]:
        ret_prompt = ""
        for data in self._data:
            ret_prompt += self.model.formatter(data) + '\n'
        return ret_prompt

    def load_memory(self)->str:
        if self._load_memory_callback:
            self._load_memory_callback(self._data, self.model)
        else:
            return self.default_load_memory()
    @property
    def memory_variables(self) -> List[str]:
        return self.model_variables

    def validate(self, data: Dict[str, Any]) -> bool:
        return set(data.keys()) == set(self.model_variables)

    def load_memory_variables(self, inputs: T = None, **kwargs) -> Dict[str, Any]:
        if inputs is None and kwargs is None:
            return self.load_memory()
        if inputs is not None and kwargs is not None:
            raise ValueError("Only one of inputs or kwargs should be passed")

        if inputs:
            return {"model_prompt": self.model.formatter(inputs)}
        elif kwargs:
            if self.validate(kwargs):
                return {"model_prompt": self.model.formatter(self.model.scheme(**kwargs))}
        raise ValueError("Invalid inputs")

    def save_context(self, inputs: List[Union[Dict[str, Any], T]]) -> None:
        pass

    def add(self, **kwargs):
        self._data.append(T(**kwargs))

    def clear(self) -> None:
        pass
