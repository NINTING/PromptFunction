from langchain import PromptTemplate

test1 = '''
{{doc_string}}

'''

test1_template = PromptTemplate(template=test1,template_format="jinja2",input_variables=["doc_string"],)

