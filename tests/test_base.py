import json
import os
import sys
import unittest

from langchain.llms import openai
from langchainex.OpenAIWebLLM import OpenAIWebLLM

from promptfunction import prompt_func
from promptfunction.PromptTemplate import test1_template
from promptfunction.function import set_llm
from promptfunction.util import debug_prompt

authData = json.load(open("../Auth.json"))

os.environ["OPENAI_API_KEY"] = authData['OPENAI_API_KEY']
os.environ['WEB_ACCESS_TOKEN'] = authData['WEB_ACCESS_TOKEN']
os.environ['PROXY'] = authData['PROXY']
openai.proxy = {
    "https": os.environ['PROXY']
}

webLLm = OpenAIWebLLM(**{'paid': True, 'model': 'gpt-3.5-turbo', 'chat_once': False})

class MyTestCase(unittest.TestCase):

    def test_setllm(self):

        @prompt_func(template=test1_template)
        def A(say):
            """
            {{say}}
            """

            set_llm(webLLm)

        print(A('hello'))


    def test_debug_prompt(self):
        @prompt_func(template=test1_template)
        def A(say):
            """
            {{say}}
            """
            set_llm(webLLm)
        print(debug_prompt(A,{'say':'hello'}))

    def test_sandbox(self):
        def get_local_vars(func, *args, **kwargs):
            func_globals = func.__globals__.copy()
            func_locals = {}

            def tracer(frame, event, arg):
                nonlocal func_locals
                if event == 'return':
                    func_locals = frame.f_locals.copy()

            sys.settrace(tracer)
            result = func(*args, **kwargs)
            sys.settrace(None)
            return func_locals

        def A(v):
            v = 4
            return v

        locals_in_A = get_local_vars(A, 5)
        print("v = ", locals_in_A['v'])


if __name__ == '__main__':
    unittest.main()
