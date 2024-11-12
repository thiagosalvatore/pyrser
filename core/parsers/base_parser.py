from abc import ABC, abstractmethod

from bs4 import BeautifulSoup, Tag, Comment
from pydantic import BaseModel

from core.extractors.base_extractor import BaseExtractor
from core.extractors.llama_index_extractor import LlamaIndexExtractor

TAGS_TO_REMOVE = [
    "img",
    "head",
    "button",
    "svg",
    "style",
    "iframe",
    "header",
    "aside",
    "footer",
    "nav",
    "form",
    "link",
    "noscript",
    "input",
    "textarea",
    "menu",
    "track",
    "canvas",
    "video",
    "audio",
    "source",
]


class BaseParser(ABC):
    def __init__(self, extractor: BaseExtractor | None = None):
        self.__extractor = extractor or LlamaIndexExtractor()

    async def parse(
        self,
        url: str,
        output_model: type[BaseModel],
        tags_to_remove: list[str] | None = None,
    ) -> BaseModel:
        """
        Parse the html content from the given url and output it following the pydantic model
        :param url: The url to parse
        :param tags_to_remove: The tags to remove from the html content
        :param output_model: The pydantic model to output the parsed content to
        :return: The parsed content as a pydantic model
        """
        tags_to_remove = tags_to_remove or TAGS_TO_REMOVE

        content = await self._get_html_content(url)
        processed_content = self.__process_html_content(content, tags_to_remove)
        return await self.__extractor.string_to_pydantic_model(
            processed_content, output_model
        )

    @abstractmethod
    async def _get_html_content(self, url: str) -> str:
        """
        Get the html content from the given url
        :param url: the url to get the html content from
        :return: the html content
        """
        pass

    def __process_html_content(self, content: str, tags_to_remove: list[str]) -> str:
        soup: BeautifulSoup = BeautifulSoup(content, features="lxml")

        self.__remove_tags_from_soup(soup, tags_to_remove)
        self.__remove_invisible_tags(soup)
        self.__remove_comments_from_soup(soup)
        self.__remove_empty_tags_from_soup(soup)

        return soup.prettify()

    @staticmethod
    def __remove_tags_from_soup(
        soup: BeautifulSoup, tags_to_exclude: list[str]
    ) -> None:
        for tag in tags_to_exclude:
            for node in soup.find_all(tag):
                node.decompose()

    def __remove_empty_tags_from_soup(self, soup: BeautifulSoup) -> None:
        tags = soup.find_all()
        for tag in reversed(tags):  # Process tags from bottom to top
            tag.attrs = {}
            if self.is_empty_tag(tag):
                tag.decompose()

    @staticmethod
    def __remove_comments_from_soup(soup: BeautifulSoup) -> None:
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment.extract()

    @staticmethod
    def __remove_invisible_tags(soup: BeautifulSoup) -> None:
        for tag in soup.find_all(
            style=lambda value: value and "display:none" in value.replace(" ", "")  # pyright: ignore [reportArgumentType, reportOptionalCall]
        ):
            tag.decompose()

    @classmethod
    def is_empty_tag(cls, tag: Tag) -> bool:
        # A tag is empty if it has no contents or if all its contents are empty or empty tags
        if tag.string:
            return not tag.string.strip()
        return all(
            (cls.is_empty_tag(child) if isinstance(child, Tag) else not child.strip())
            for child in tag.contents
        )
