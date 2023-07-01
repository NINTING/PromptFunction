import inspect
import string
from typing import Union, Set

from langchain import LLMChain, BasePromptTemplate, PromptTemplate, OpenAI
from langchain.prompts.base import _get_jinja2_variables_from_template

from promptfunction.PromptTemplate.doc_template import doc_prompt
from promptfunction.context import Context
from promptfunction.parse import get_return_parser
from promptfunction.resever_word import VAR_FORMAT_INSTRUCTION, VAR_DOC_STRING, with_brackets


# Todo: handle langchain buildin prompt template

class PromptFunction:
    context: Context = None
    raw_func: callable = None
    func_sig: inspect.Signature = None
    llm_chain: LLMChain = None
    template: BasePromptTemplate = None

    def __init__(self, fn: callable, template: Union[BasePromptTemplate, str]):
        self.doc_string = None
        self.context = Context()
        self.llm_chain = None
        self.raw_func = fn

        self.init_func(self.raw_func)

        self.init_template(template)

        self.llm_chain = LLMChain(llm=OpenAI(), prompt=self.template)

    def __call__(self, *args, debug_prompt=False, **kwargs):

        Context.begin_context(self.context)

        bound_args = self.func_sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        self.raw_func(*args, **kwargs)
        Context.end_context(None)

        if self.context.output_parse is not None:
            self.context[VAR_FORMAT_INSTRUCTION] = self.context.output_parse.get_format_instructions()

        for key, value in bound_args.arguments.items():
            if not self.context[key]:
                self.context[key] = value

        if debug_prompt:
            mid_prompt = self.template.format(**self.context.variables)
            return mid_prompt

        if self.context.llm is not None and self.llm_chain.llm != self.context.llm:
            self.llm_chain.llm = self.context.llm

        if len(self.context.variables) > 0:
            output = self.llm_chain.run(**self.context.variables)
        else:
            prompt: string = self.template.format(**self.context.variables)
            output = self.llm_chain.llm.predict(prompt)

        return self.parse_output(output)

    def init_func(self, func):
        doc_string_prompt: str = func.__doc__.strip()
        # self.context[VAR_DOC_STRING] = doc_string_prompt
        self.doc_string = doc_string_prompt
        self.func_sig = inspect.signature(func)

        self.init_parse()

    def init_template(self, template: Union[BasePromptTemplate, str]):
        if template is None:
            self.template = PromptTemplate.from_template(self.doc_string, template_format="jinja2")
            return

        init_render_values = {VAR_DOC_STRING: self.doc_string}
        if isinstance(template, str):
            func_template = template.replace(with_brackets(VAR_DOC_STRING), self.doc_string)
            self.template = PromptTemplate.from_template(func_template, template_format="jinja2")
        else:

            func_template = template.format(**init_render_values)
            if type(template) is PromptTemplate or issubclass(type(template), PromptTemplate):
                self.template = PromptTemplate.from_template(func_template, template_format="jinja2")
            else:
                func_vars: Set[str] = _get_jinja2_variables_from_template(func_template)
                func_vars.update(template.input_variables)
                self.template = type(template)(template=func_template, template_format="jinja2",
                                               input_variables=list(Set))

    def has_return(self):
        return self.func_sig.return_annotation != inspect.Signature.empty

    def return_is_string(self):
        return self.func_sig.return_annotation == str

    def init_parse(self):
        if not self.has_return() or self.return_is_string():
            return

        self.context.output_parse = get_return_parser(self.func_sig.return_annotation)

    # self.context[VAR_FORMAT_INSTRUCTION] = self.context.output_parse.get_format_instructions()

    def parse_output(self, output):
        if self.context.output_parse is not None:
            return self.context.output_parse.parse(output)
        else:
            return output


def prompt_func(template: Union[BasePromptTemplate, str] = doc_prompt):
    def wrapper(fn):
        return PromptFunction(fn, template)

    return wrapper
