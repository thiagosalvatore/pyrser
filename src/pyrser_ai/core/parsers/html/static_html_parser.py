from aiohttp import ClientSession

from pyrser_ai.core.extractors.base_extractor import BaseExtractor
from pyrser_ai.core.parsers.html.base_html_parser import BaseParser
from pyrser_ai.core.parsers.html.exceptions import StaticHTMLParserFailed


class StaticHTMLParser(BaseParser):
    def __init__(
        self, http_client: ClientSession, extractor: BaseExtractor | None = None
    ):
        super().__init__(extractor)
        self.__http_client = http_client

    async def _get_html_content(self, url: str) -> str:
        """
        Get the html content from the given url
        :param url: the url to get the html content from
        :return: the html content
        """
        async with self.__http_client.get(url) as resp:
            try:
                resp.raise_for_status()
                return await resp.text()
            except Exception as e:
                raise StaticHTMLParserFailed(
                    f"Failed to get html content from {url}. Details: {await resp.text()}"
                ) from e
