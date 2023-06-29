import string

from langchain import BasePromptTemplate
from langchain.llms.base import LLM




class Context:
    llm: LLM = None
    template: BasePromptTemplate = None
    variables: dict = {}
    @staticmethod
    def switch_context(context):
        global internal_context
        internal_context = context

    @staticmethod
    def current_context():
        global internal_context
        return internal_context

    def set_var(self,key:string,value):
        self.variables[key] = value

    def get_var(self, key):
        return self.variables.get(key)

    def has_key(self,key):
        return key in self.variables

internal_context: Context = None
