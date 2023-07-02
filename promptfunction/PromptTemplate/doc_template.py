from langchain import PromptTemplate
from langchain.prompts import PipelinePromptTemplate

from promptfunction.resever_word import *

# doc_prompt = f'''
# {{% if {VAR_FORMAT_INSTRUCTION} -%}}
# #FORMATE INSTURCTION
# {with_brackets(VAR_FORMAT_INSTRUCTION)}
# {{% endif -%}}
# #CONTENT
# {with_brackets(VAR_DOC_STRING)}'''




_VAR_DOC_STRING_TEMPLATE = as_variable(as_template(VAR_DOC_STRING))
_VAR_FORMAT_INSTRUCTION_TEMPLATE = as_variable(as_template(VAR_FORMAT_INSTRUCTION))
_VAR_PREFIX_TEMPLATE = as_variable(as_template(VAR_PREFIX))
_VAR_DATA_TEMPLATE = as_variable(as_template(VAR_DATA))
_VAR_ACTOR_TEMPLATE = as_variable(as_template(VAR_ACTOR))
_VAR_SAMPLES_TEMPLATE = as_variable(as_template(VAR_SAMPLES))
_VAR_OUTPUT_REQUIREMENTS_TEMPLATE = as_variable(as_template(VAR_OUTPUT_REQUIREMENTS))
_VAR_INTERPRETATION_TEMPLATE = as_variable(as_template(VAR_INTERPRETATION))
_VAR_TOOLS_TEMPLATE = as_variable(TOOLS_TEMPLATE)

# default_full_template = f"""
# {{% if {PREFIX_TEMPLATE} -%}}
# {_VAR_PREFIX_TEMPLATE}
# {{%- endif %}}
# {{% if {ACTOR_TEMPLATE} -%}}
# {_VAR_ACTOR_TEMPLATE}
# {{%- endif %}}
# {{% if {DATA_TEMPLATE} -%}}
# {_VAR_DATA_TEMPLATE}
# {{%- endif %}}
# {{% if {SAMPLES_TEMPLATE} -%}}
# {_VAR_SAMPLES_TEMPLATE}
# {{%- endif %}}
# {{% if {OUTPUT_REQUIREMENTS_TEMPLATE} -%}}
# {_VAR_OUTPUT_REQUIREMENTS_TEMPLATE}
# {{%- endif %}}
# {{% if {INTERPRETATION_TEMPLATE} -%}}
# {_VAR_INTERPRETATION_TEMPLATE}
# {{%- endif %}}
# {{% if {FORMAT_INSTRUCTION_TEMPLATE} -%}}
# {_VAR_FORMAT_INSTRUCTION_TEMPLATE}
# {{%- endif %}}
# {{% if {DOC_STRING_TEMPLATE} -%}}
# {_VAR_DOC_STRING_TEMPLATE}
# {{%- endif %}}
# """

default_full_template = f"""
{_VAR_PREFIX_TEMPLATE}
{_VAR_ACTOR_TEMPLATE}
{_VAR_DATA_TEMPLATE}
{_VAR_SAMPLES_TEMPLATE}
{_VAR_OUTPUT_REQUIREMENTS_TEMPLATE}
{_VAR_INTERPRETATION_TEMPLATE}
{_VAR_FORMAT_INSTRUCTION_TEMPLATE}
{_VAR_TOOLS_TEMPLATE}
{_VAR_DOC_STRING_TEMPLATE}
"""
full_prompt = PromptTemplate.from_template(template=default_full_template, template_format="jinja2")

prefix_string = \
f"""{{% if {VAR_PREFIX} -%}}
{as_variable_line(VAR_PREFIX)}

{{% endif -%}}
"""
prefix_template = PromptTemplate.from_template(template=prefix_string, template_format="jinja2")

actor_string = \
f"""{{% if {VAR_ACTOR} -%}}
{as_variable_line(VAR_ACTOR)}
{{% endif -%}}"""
actor_template = PromptTemplate.from_template(template=actor_string, template_format="jinja2")

data_string = \
f"""{{% if {VAR_DATA} -%}}
{as_variable_line(VAR_DATA)}
{{% endif -%}}"""
data_template = PromptTemplate.from_template(template=data_string, template_format="jinja2")

samples_string = \
f"""{{% if {VAR_SAMPLES} -%}}
{{% for sample in {VAR_SAMPLES} -%}}
{as_variable_line("sample")}

{{% endfor -%}}
{{% endif -%}}"""
samples_template = PromptTemplate.from_template(template=samples_string, template_format="jinja2")

output_requirements_string = \
f"""{{% if {VAR_OUTPUT_REQUIREMENTS} -%}}
{as_variable_line(VAR_OUTPUT_REQUIREMENTS)}
{{% endif -%}}
"""
output_requirements_template = PromptTemplate.from_template(template=output_requirements_string,
                                                            template_format="jinja2")

interpretation_string = \
f"""{{% if {VAR_INTERPRETATION} -%}}
{as_variable_line(VAR_INTERPRETATION)}

{{% endif -%}}
"""
interpretation_template = PromptTemplate.from_template(template=interpretation_string, template_format="jinja2")

format_instruction_string = \
f"""{{% if {VAR_FORMAT_INSTRUCTION} -%}}
{as_variable_line(VAR_FORMAT_INSTRUCTION)}

{{% endif -%}}"""
format_instruction_template = PromptTemplate.from_template(template=format_instruction_string,
                                                           template_format="jinja2")

tool_string = \
f"""
{{%- if {VAR_TOOLS} -%}}
For better complete task,You have access to the following tools:
```
{{% for tool in {VAR_TOOLS} -%}}
{{
'name':{as_variable_line("tool.name")}
'description':{as_variable_line("tool.description")}
}}
{{% endfor -%}}
```
{{% endif -%}}"""

tool_template = PromptTemplate.from_template(template=tool_string, template_format="jinja2")


doc_string_string = \
f"""{{% if {VAR_DOC_STRING} -%}}
{as_variable(VAR_DOC_STRING)}
{{% endif -%}}"""
doc_string_template = PromptTemplate.from_template(template=doc_string_string, template_format="jinja2")



input_prompts = [
    (PREFIX_TEMPLATE, prefix_template),
    (ACTOR_TEMPLATE, actor_template),
    (DATA_TEMPLATE, data_template),
    (SAMPLES_TEMPLATE, samples_template),
    (OUTPUT_REQUIREMENTS_TEMPLATE, output_requirements_template),
    (INTERPRETATION_TEMPLATE, interpretation_template),
    (FORMAT_INSTRUCTION_TEMPLATE, format_instruction_template),
    (TOOLS_TEMPLATE, tool_template),
    (DOC_STRING_TEMPLATE, doc_string_template),
]

pipeline_prompt = PipelinePromptTemplate(final_prompt=full_prompt, pipeline_prompts=input_prompts, template_format="jinja2")
