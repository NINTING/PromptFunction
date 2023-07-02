import string

def as_variable(keyword: string):
    return "{{ " + keyword + " -}}"

def as_variable_line(keyword: string):
    return "{{ " + keyword + " }}"

def as_template(keyword: string):
    return  keyword + "_template"


VAR_DOC_STRING = "doc_string"
VAR_FORMAT_INSTRUCTION = "format_instruction"
VAR_PREFIX = "prefix"
VAR_SAMPLES = "samples"
VAR_OUTPUT_REQUIREMENTS = "output_requirements"
VAR_DATA = "data"
VAR_ACTOR = "actor"
VAR_INTERPRETATION = "interpretation"
VAR_TOOLS = "tools"

DOC_STRING_TEMPLATE = as_template(VAR_DOC_STRING)
FORMAT_INSTRUCTION_TEMPLATE = as_template(VAR_FORMAT_INSTRUCTION)
PREFIX_TEMPLATE = as_template(VAR_PREFIX)
DATA_TEMPLATE = as_template(VAR_DATA)
ACTOR_TEMPLATE = as_template(VAR_ACTOR)
OUTPUT_REQUIREMENTS_TEMPLATE = as_template(VAR_OUTPUT_REQUIREMENTS)
SAMPLES_TEMPLATE = as_template(VAR_SAMPLES)
INTERPRETATION_TEMPLATE = as_template(VAR_INTERPRETATION)
TOOLS_TEMPLATE = as_template(VAR_TOOLS)

