import os
from google import genai

from kernel.result import Result
from kernel.tool import Tool


client = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))

def ask_llm(prompt: str) -> str:
    response = client.models.generate_content(
        model = "gemini-flash-latest",
        contents = prompt
    )

    return response.text

class LLMTool(Tool):

    def dry_run(self, **kwargs) -> Result:
        return Result(
            ok = True,
            output = {},
        )

    def run(self, **kwargs) -> Result:
        result = ask_llm(kwargs.get("text", ""))

        return Result(
            ok = True,
            output = {"answer": result},
        )
