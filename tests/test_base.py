import logging
import unittest
from types import NoneType

from langchain import OpenAI

from promptfunction import prompt_func
from promptfunction.function import set_llm, set_variable, set_output_parse
from promptfunction.parse import NumberParse
from promptfunction.util import debug_prompt
from tests.api_key import *


class MyTestCase(unittest.TestCase):

    # print(base_usage(a=1, b=2))

    def test_static_prompt(self):
        @prompt_func()
        def hello_world():
            """
            hi,how are you?
            """

        hello_world()

    def test_setllm(self):
        @prompt_func()
        def hello_world():
            """
            hi,how are you?
            """

            set_llm(webLLm)

        self.assertIs(type(hello_world.context.llm), NoneType)
        self.assertIs(type(hello_world.llm_chain.llm), OpenAI)
        hello_world()
        self.assertIs(type(hello_world.llm_chain.llm), OpenAIWebLLM)

    def test_int(self):
        @prompt_func()
        def add_func(a, b) -> int:
            """
            {{a}} + {{b}} = ?
            """
            set_llm(webLLm)

        self.assertIs(type(add_func.context.output_parse), NumberParse)
        value = add_func(1, 2)
        self.assertIs(type(value), int)
        if value != 3:
            logging.warning(f"Warning: {value} != 3")

    def test_float(self):
        @prompt_func()
        def add_func(a, b) -> float:
            """
            {{a}} + {{b}} = ?
            """
            set_llm(webLLm)

        self.assertIs(type(add_func.context.output_parse), NumberParse)
        a = 1.34
        b = 2.45
        value = add_func(a, b)

        self.assertIs(type(value), float, msg=debug_prompt(add_func, a, b))
        if value != a + b:
            logging.warning(f"Warning: {value} != {a + b}")

    def test_variable(self):
        @prompt_func()
        def var_add_func(a) -> int:
            """
            {{a}} + {{b}} = ?
            """
            set_llm(webLLm)
            set_variable('b', a * a)

        a = 2
        value = var_add_func(a)
        self.assertIs(type(value), int)
        self.assertEqual(value, a + a * a)

    def test_number(self):
        @prompt_func()
        def output_number() -> int:
            """
             Tell me how population of world,give me a Probably number
            """
            set_llm(webLLm)

        print("==========Output Number=========")
        print(debug_prompt(output_number))
        age = output_number()
        self.assertIs(type(age), int)

    def test_doc_is_template(self):
        @prompt_func(template=None)
        def python_shell(shell):
            """
            You are a python shell and you need to execute every piece of python code and return the result.
            for example:
            shell:
            def Add(a,b)
                return a * b + 1
            a = 1
            b = 2
            print(add(a,b))
            console:
            3

            now,lets begin.
            shell:
            {{shell}}
            console:
            """
            set_llm(webLLm)

        print(debug_prompt(python_shell, """
                for i in range(10):
                    print(i)"""))
        print(python_shell("""
                for i in range(10):
                    print(i)
                """))

    # def test_custom_template(self):
    #
    #     @prompt_func(template="hi,how are you?")
    #     def hello_world():
    #         """
    #         hi,how are you?
    #         """
    #
    #     hello_world()
    #
    # def test_custom_parse(self):
    #     @prompt_func(parse=NumberParse)
    #     def output_number():
    #         """
    #          Tell me how population of world,give me a Probably number
    #         """
    #         set_llm(webLLm)
    #         set_output_parse(NumberParse)
    #
    #     age = output_number()
    #     self.assertIs(type(age), int)


if __name__ == '__main__':
    unittest.main()
