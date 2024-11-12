from pathlib import Path

from llama_index.core.llms.function_calling import FunctionCallingLLM
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.llms.openai import OpenAI, AsyncOpenAI
from pydantic import BaseModel

from pyrser.core.extractors.base_extractor import BaseExtractor


class LlamaIndexExtractor(BaseExtractor):
    def __init__(
        self, model: str = "gpt-4o-mini", llm: FunctionCallingLLM | None = None
    ):
        if not llm and not model:
            raise ValueError("Either llm or model must be provided")

        self.__llm = llm or OpenAI(model=model, async_openai_client=AsyncOpenAI())

    async def string_to_pydantic_model(
        self, content: str, output_model: type[BaseModel]
    ) -> BaseModel:
        with open(self.__get_prompt_path(), "r") as file:
            prompt_template_str = file.read()
            program = LLMTextCompletionProgram.from_defaults(
                output_cls=output_model,
                prompt_template_str=prompt_template_str,
                verbose=True,
                llm=self.__llm,
            )

            result = await program.acall(content=content)

            return result

    @staticmethod
    def __get_prompt_path() -> Path:
        current_file_path = Path(__file__)

        return current_file_path.parent / "prompts" / "html_parser_prompt.txt"
