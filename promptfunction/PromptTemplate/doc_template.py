from langchain import PromptTemplate

from promptfunction.resever_word import VAR_DOC_STRING, VAR_FORMAT_INSTRUCTION, with_brackets

doc_prompt = f'''
{{% if {VAR_FORMAT_INSTRUCTION} -%}}
#FORMATE INSTURCTION
{with_brackets(VAR_FORMAT_INSTRUCTION)}
{{% endif -%}}
#CONTENT
{with_brackets(VAR_DOC_STRING)}'''

# doc_template = PromptTemplate(template=test1,template_format="jinja2",input_variables=["doc_string"],)

