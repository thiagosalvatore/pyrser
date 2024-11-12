from unittest.mock import AsyncMock

import aiohttp
import pytest
from pydantic import BaseModel

from src.pyrser_ai.core.extractors.base_extractor import BaseExtractor
from src.pyrser_ai.core.parsers.static_html_parser import StaticHTMLParser


class OutputModelTest(BaseModel):
    field: str

@pytest.fixture
def extractor_mock():
    return AsyncMock(BaseExtractor)



async def test_parse_should_call_string_to_pydantic_with_cleaned_html(extractor_mock, aresponses):
    aresponses.add("test.com", "/test", "GET", aresponses.Response(text="""<div>Hello</div><span as='b'>test</span><a></a><p style='display: none'>test</p>""", status=200))

    async with aiohttp.ClientSession() as session:
        parser = StaticHTMLParser(extractor=extractor_mock, http_client=session)
        await parser.parse("http://test.com/test", OutputModelTest, tags_to_remove=["div"])

        extractor_mock.string_to_pydantic_model.assert_awaited_once_with("<html>\n <body>\n  <span>\n   test\n  </span>\n </body>\n</html>\n", OutputModelTest)

