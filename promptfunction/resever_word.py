import string

VAR_DOC_STRING = "doc_string"
VAR_RAW_DOC_STRING = "raw_doc_string"

VAR_FORMAT_INSTRUCTION = "format_instruction"


def with_brackets(keyword: string):
    return "{{" + keyword + "}}"
