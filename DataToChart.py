from prompts import DATA2CHART_PROMPT
import json
from utils import CustomJSONEncoder


class Data2Chart:
    def __init__(self, cohere_client):
        self.llm = cohere_client

    def gen_chart(self, requirement: str, result: list, render_mode: str) -> str:
        """
        This Python function generates a chart based on a given requirement and result data using a
        specified rendering mode.
        
        :param requirement: The `requirement` parameter in the `gen_chart` method is a string that
        represents the requirement for generating a chart. It specifies the information or data that the
        chart should visualize
        :type requirement: str
        :param result: The `result` parameter in the `gen_chart` method is expected to be a list. This
        list will be converted to a JSON string using a custom JSON encoder (`CustomJSONEncoder`) when
        the `render_mode` is set to "Function". The JSON string will then be used in the prompt
        :type result: list
        :param render_mode: The `render_mode` parameter in the `gen_chart` method determines how the
        chart will be rendered. In this code snippet, if `render_mode` is set to "Function", the
        `result` list will be converted to a JSON string using a custom JSON encoder
        (`CustomJSONEncoder`). The
        :type render_mode: str
        :return: The `gen_chart` method returns the generated chart based on the input requirement,
        result data, and render mode specified. The chart is generated using the OpenAI language model
        with the provided parameters such as model type, prompt, max tokens, temperature, frequency
        penalty, and presence penalty. The generated chart is then returned as a string.
        """
        if render_mode == "Function":
            
            result = json.dumps(result, cls=CustomJSONEncoder)
            prompt = DATA2CHART_PROMPT.format(
                requirement=requirement, result=result
            )

        generated = self.llm.generate(
                model='command',
                prompt=prompt,
                max_tokens=5000,
                temperature=0.1,  # Slightly above 0 to allow for minimal creativity while staying accurate
                frequency_penalty=0,  # Ensures diversity in responses without unnecessary repetition
                presence_penalty=0,  # Avoids overly focusing on the same concepts repeatedly
                )
        return generated

