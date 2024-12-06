import io

from pydantic import BaseModel

from pyrser_ai.core.extractors.base_extractor import BaseExtractor
from pyrser_ai.core.extractors.llama_index_extractor import LlamaIndexExtractor
from pyrser_ai.core.readers.base_reader import BaseReader
from pyrser_ai.core.readers.llama_parse_reader import LLamaParseReader


class FileParser:
    def __init__(self, extractor: BaseExtractor | None = None, reader: BaseReader | None = None):
        self.__extractor = extractor or LlamaIndexExtractor()
        self.__reader = reader or LLamaParseReader()

    async def parse_document(
        self,
        document: io.BytesIO,
        file_name: str,
        output_model: type[BaseModel],
    ) -> BaseModel:
        """
        Parse the html content from the given url and output it following the pydantic model
        :param document: The document to parse
        :param file_name: The name of the document
        :param output_model: The pydantic model to output the parsed content to
        :return: The parsed content as a pydantic model
        """

        content = await self.__reader.get_content(document, file_name)

        return await self.__extractor.string_to_pydantic_model(
            content, output_model
        )

