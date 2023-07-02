from typing import Dict, Any

from langchain import LLMChain


class PromptFunctionChain(LLMChain):
    def _validate_inputs(self, inputs: Dict[str, Any]) -> None:
        """Check that all inputs are present."""
        # TODO: more detail check validation.
        # TODO: user make variable that need to be input.
        pass
