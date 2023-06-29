from langchain.llms.base import LLM

from promptfunction.context import Context


def set_llm(llm: LLM):
    """Set the LLMChain."""
    context = Context.current_context()
    context.llm = llm
