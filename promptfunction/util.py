from promptfunction.base import PromptFunction


def debug_prompt(prompt_func:PromptFunction,kwargs:dict):
     return prompt_func(**kwargs,debug_prompt = True)

