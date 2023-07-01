import json
import os

import openai
from langchainex.OpenAIWebLLM import OpenAIWebLLM

authData = json.load(open("../Auth.json"))

os.environ["OPENAI_API_KEY"] = authData['OPENAI_API_KEY']
os.environ['WEB_ACCESS_TOKEN'] = authData['WEB_ACCESS_TOKEN']
os.environ['PROXY'] = authData['PROXY']
openai.proxy = {
    "https": os.environ['PROXY']
}

webLLm = OpenAIWebLLM(**{'paid': True, 'model': 'gpt-3.5-turbo', 'chat_once': True})
