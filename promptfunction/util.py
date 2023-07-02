import logging

from promptfunction.base import PromptFunction


def debug_prompt(prompt_func: PromptFunction, *args, **kwargs):
    prompt = prompt_func(*args, **kwargs, debug_prompt=True)

    logging.info(prompt)
    return prompt


def debug_template(prompt_func: PromptFunction):
    return prompt_func.template


