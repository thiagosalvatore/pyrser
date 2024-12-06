import io
from abc import ABC, abstractmethod


class BaseReader(ABC):
    @abstractmethod
    async def get_content(self, document: io.BytesIO, file_name: str) -> str:
        """
        Get the content from the given document
        :param document: The document to get the content from
        :return: The content of the document
        """
        pass