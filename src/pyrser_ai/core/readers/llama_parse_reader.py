import io

from llama_parse import LlamaParse, ResultType
from llama_parse.utils import Language

from pyrser_ai.core.readers.base_reader import BaseReader
from pyrser_ai.core.readers.exceptions import DocumentReadFailed


class LLamaParseReader(BaseReader):
    def __init__(self, language: Language = Language.ENGLISH):
        self.__parser = LlamaParse(
            result_type=ResultType.MD,
            num_workers=4,
            language=language,
        )
    async def get_content(self, document: io.BytesIO, file_name: str) -> str:
        extra_info = {"file_name": file_name}
        documents = await self.__parser.aload_data(document, extra_info=extra_info)

        if not documents:
            raise DocumentReadFailed(f"Failed to read the document {file_name}")

        return documents[0].get_content()

