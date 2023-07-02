import logging
import unittest

from langchain import SerpAPIWrapper
from langchain.agents.mrkl.output_parser import MRKLOutputParser
from langchain.tools import Tool, DuckDuckGoSearchRun
from langchain.utilities import serpapi

from promptfunction import prompt_func
from promptfunction.function import *
from promptfunction.util import debug_prompt
from tests.api_key import webLLm

logging.getLogger().setLevel(logging.INFO)
# Load the tool configs that are needed.



class MyTestCase(unittest.TestCase):
    def test_something(self):
        logging.info("a")






if __name__ == '__main__':
    unittest.main()
