import logging

from langchain.agents.self_ask_with_search.output_parser import SelfAskOutputParser
from langchain.tools import Tool, DuckDuckGoSearchRun

from promptfunction import *

search = DuckDuckGoSearchRun()

sample1 = f"""Question: Who lived longer, Muhammad Ali or Alan Turing?
Are follow up questions needed here: Yes.
Follow up: How old was Muhammad Ali when he died?
Intermediate answer: Muhammad Ali was 74 years old when he died.
Follow up: How old was Alan Turing when he died?
Intermediate answer: Alan Turing was 41 years old when he died.
So the final answer is: Muhammad Ali"""

search_tool = Tool(
    name="Intermediate Answer",
    func=search.run,
    coroutine=search.arun,
    description="Search",
)


@prompt_func()
def react_agent(input, agent_scratchpad=""):
    """
    Question: {{input}}
    Are follow up questions needed here:{{agent_scratchpad}}
    """
    # set_tool(search_tool)
    set_output_parse(SelfAskOutputParser())
    add_sample(sample1)

    set_stop("\nIntermediate answer:")


def test_react():
    debug_prompt(react_agent, "Who is Leo DiCaprio's girlfriend?")
    logging.info(react_agent("Who is Leo DiCaprio's girlfriend?"))
