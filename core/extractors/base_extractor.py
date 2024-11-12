from abc import ABC, abstractmethod

from pydantic import BaseModel


class BaseExtractor(ABC):
    @abstractmethod
    async def string_to_pydantic_model(
        self, content: str, output_model: type[BaseModel]
    ) -> BaseModel:
        pass
