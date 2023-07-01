from langchain import BasePromptTemplate
from langchain.llms.base import LLM
from langchain.schema import BaseOutputParser


class Context:
    llm: LLM = None
    output_parse: BaseOutputParser = None
    variables: dict = {}

    def __init__(self):
        self.variables = {}
        self.llm = None
        self.output_parse = None

    @staticmethod
    def begin_context(context):
        global internal_context
        internal_context = context

    @staticmethod
    def end_context(self):
        global internal_context
        internal_context = None

    @staticmethod
    def current_context():
        global internal_context
        if internal_context is None:
            raise Exception("Context Is None ,Don't Use Context Outside PromptFunction")
        return internal_context

    def __setitem__(self, key, value):
        self.variables[key] = value

    def __getitem__(self, key):
        return self.variables.get(key)

    def __contains__(self, key):
        return key in self.variables


internal_context: Context = None
