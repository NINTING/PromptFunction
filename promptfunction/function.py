from typing import Sequence

from langchain.llms.base import LLM
from langchain.schema import BaseOutputParser
from langchain.tools import BaseTool

from promptfunction.context import Context
from promptfunction.resever_word import *


def set_llm(llm: LLM):
    """Set the LLMChain."""
    context = Context.current_context()
    if  llm is not None:
        context.llm = llm


def set_variable(key: str, value):
    """Set the variable."""
    context = Context.current_context()
    context[key] = value


def set_output_parse(parse: BaseOutputParser):
    """Set the output parse."""
    context = Context.current_context()
    context.output_parse = parse


def set_stop(stop):
    """Set the stop."""
    context = Context.current_context()
    context.stop = stop


def set_prefix(prefix):
    """Set the prefix."""
    context = Context.current_context()
    context[VAR_PREFIX] = prefix


def set_tools(tools: Sequence[BaseTool]):
    """Set the tools."""
    context = Context.current_context()
    context[VAR_TOOLS] = tools


def add_tool(tools: Sequence[BaseTool]):
    """Set the tools."""
    context = Context.current_context()
    if not context[VAR_TOOLS]:
        context[VAR_TOOLS] = [tools]
    else:
        context[VAR_TOOLS].append(tools)


def set_samples(samples: Sequence[str]):
    """Set the samples."""
    context = Context.current_context()
    context[VAR_SAMPLES] = samples


def add_sample(sample: str):
    """Set the sample."""
    context = Context.current_context()
    if not context[VAR_SAMPLES]:
        context[VAR_SAMPLES] = [sample]
    else:
        context[VAR_SAMPLES].append(sample)
