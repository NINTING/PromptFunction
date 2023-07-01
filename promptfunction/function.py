from langchain.llms.base import LLM
from langchain.schema import BaseOutputParser

from promptfunction.context import Context


def set_llm(llm: LLM):
    """Set the LLMChain."""
    context = Context.current_context()
    context.llm = llm

def set_variable(key: str, value):
    """Set the variable."""
    context = Context.current_context()
    context[key] = value


def set_output_parse(parse:BaseOutputParser):
    """Set the output parse."""
    context = Context.current_context()
    context.output_parse = parse