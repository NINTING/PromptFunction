from typing import Union, List, Dict, Any

from langchain.agents.self_ask_with_search.output_parser import SelfAskOutputParser
from langchain.llms import FakeListLLM
from langchain.schema import AgentAction, AgentFinish
from langchain.tools import Tool, DuckDuckGoSearchRun

from promptfunction import *
from promptfunction.memory import MemoryModel, WorkMemory
from tests.api_key import *

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





def model_formatter(model) -> str:
    ##return f"follow up: {model.question}\nIntermediate answer: {model.intermedia_answer}\n"
    return f"{model.log}\nIntermediate answer: {model.answer}\n"

SearchPlaneScheme: MemoryModel = MemoryModel([("question", str), ("answer", str), ("log", str)], model_formatter)


def load_memory_callback(dates: List[type(SearchPlaneScheme)], scheme: MemoryModel) -> Dict[str, Any]:
    ret_prompt = ""
    for data in dates:
        ret_prompt += scheme.formatter(data)
    return ret_prompt


@prompt_func()
def react_plane(input, agent_scratchpad="", llm=None):
    """
    Question: {{input}}
    Are follow up questions needed here:{{agent_scratchpad}}
    """
    # set_tool(search_tool)
    set_output_parse(SelfAskOutputParser())
    add_sample(sample1)
    set_llm(llm)
    set_stop("\nIntermediate answer:")

class react_agent():


def test_react():
    work_memory = WorkMemory.create_by_model(SearchPlaneScheme,
                                             load_memory=load_memory_callback)

    # debug_prompt(react_agent, "Who is Leo DiCaprio's girlfriend?")
    # logging.info(react_agent("Who is Leo DiCaprio's girlfriend?"))
    #
    answer = ""
    step = 0
    agent_scratchpad = ""
    responses = ["Yes\nFollow up: How old was Muhammad Ali when he died?",
                 "Follow up: How old was Alan Turing when he died?", "So the final answer is: Muhammad Ali"]
    fake_llm = FakeListLLM(responses=responses)

    while True:
        if step > 5:
            logging.warning(f"Too many steps {step}")
            break
        step += 1
        logging.info(f"================Step{step}=====================")
        debug_prompt(react_plane, "Who is Leo DiCaprio's girlfriend?", work_memory.load_memory())
        action: Union[AgentAction, AgentFinish] = react_plane("Who is Leo DiCaprio's girlfriend?",
                                                              agent_scratchpad=work_memory.load_memory())
        logging.info(action.log)
        if type(action) is AgentAction:
            intermediate_answer = search_tool.run(action.tool_input)
            logging.info(f"intermediate_answer: {intermediate_answer}")
        else:
            debug_prompt(react_plane, "Who is Leo DiCaprio's girlfriend?", agent_scratchpad)
            answer = action.return_values["output"]
            break
        work_memory.add(question=action.tool_input, answer=intermediate_answer, log=action.log)

    logging.info(f"Answer: {answer}")
