from promptfunction.base import PromptFunction


def debug_prompt(prompt_func: PromptFunction, *args, **kwargs):
    return prompt_func(*args, **kwargs, debug_prompt=True)


def debug_template(prompt_func: PromptFunction):
    return prompt_func.template
