from langchain import PromptTemplate

template = '''
{% if demand and demand.isHead -%}
{{demand.content}}
{% endif -%}

{%if actor -%}
你是一名{{actor.work}}.
{%if actor.description -%}
{{actor.description}}
{% endif -%}
{% endif -%}
{% if inputActions -%}
{% for action in inputActions -%}
{% for item in action.items -%}
{{item.id}}. {{ item.value }}
{% endfor -%}
{% if action.data -%}
{{action.data.key}}: 
```
{{action.data.content}}
```
{% endif -%}
{% endfor -%}
{% endif -%}
{% if outputRequires -%}
# 回复要求
你需要遵守以下要求: 
{% for require in outputRequires -%}
## {{ require.context }}
{% for item in require.items -%}
{{item.id}}. {{ item.value }}
{% endfor -%}
{% endfor -%}
{% endif -%}
{% if interpretations -%}
# 额外的必要信息
一些额外的信息，你需了解并应用:
{% for interpretation in interpretations -%}
{{ interpretation.key }}:
```
{{ interpretation.description }}
```
{% endfor -%}
{% endif -%}
{% if demand and demand.isHead == false -%}
{{demand.content}}
{% endif -%}
'''

default_template = PromptTemplate(template=template, template_format="jinja2",
                                  input_variables=["actor", "inputActions", "outputRequires", "interpretations",
                                                   "demand"])
