import inspect
from typing import Union

from jinja2 import Template
from langchain import LLMChain, BasePromptTemplate
from langchain.prompts.base import _get_jinja2_variables_from_template

from promptfunction.PromptTemplate import default_template
from promptfunction.context import Context
from promptfunction.resever_word import rw_raw_doc_string, rw_doc_string


class PromptFunction:
    context: Context = None
    raw_func: callable = None
    func_sig: inspect.Signature = None
    llm_chain: LLMChain = None
    template: BasePromptTemplate = None

    def __init__(self, fn: callable, template: Union[BasePromptTemplate, str]):
        self.context = Context()
        self.llm_chain = None
        self.raw_func = fn
        self.template = template

        self.handle_func(self.raw_func)

    def __call__(self, *args, debug_prompt=False, **kwargs):
        Context.switch_context(self.context)

        bound_args = self.func_sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        self.raw_func(*args, **kwargs)

        for key, value in bound_args.arguments.items():
            if not self.context.has_key(key):
                self.context.set_var(key, value)

        doc_string_variables = _get_jinja2_variables_from_template(self.context.get_var(rw_raw_doc_string))
        if len(doc_string_variables) > 0:
            doc_template = Template(self.context.get_var(rw_raw_doc_string))
            self.context.set_var(rw_doc_string, doc_template.render(**self.context.variables))

        if debug_prompt==True:
            mid_prompt = self.template.format(**self.context.variables)
            return mid_prompt

        if self.llm_chain == None:
            self.llm_chain = LLMChain(llm=self.context.llm, prompt=self.template)
        else:
            self.llm_chain.llm = self.context.llm

        return self.llm_chain.run(self.context.variables)

    def handle_func(self, func):
        doc_string_prompt: str = func.__doc__.strip()
        self.context.set_var(rw_raw_doc_string, doc_string_prompt)

        self.func_sig = inspect.signature(func)

    def output_promt(self):
        pass


def prompt_func(*, template: Union[BasePromptTemplate, str] = default_template):
    def wrapper(fn):
        return PromptFunction(fn, template)

    return wrapper
