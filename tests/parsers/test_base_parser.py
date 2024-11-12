from unittest.mock import AsyncMock

import pytest
from pydantic import BaseModel

from src.pyrser.core.extractors.base_extractor import BaseExtractor
from src.pyrser.core.parsers.base_parser import BaseParser


class ParserTest(BaseParser):
    async def _get_html_content(self, url: str) -> str:
        return """<div>Hello</div><span as='b'>test</span><a></a><p style='display: none'>test</p>"""

class OutputModelTest(BaseModel):
    field: str

@pytest.fixture
def extractor_mock():
    return AsyncMock(BaseExtractor)

async def test_parse_should_call_string_to_pydantic_with_cleaned_html(extractor_mock):
    parser = ParserTest(extractor=extractor_mock)
    await parser.parse("http://test.com", OutputModelTest, tags_to_remove=["div"])

    extractor_mock.string_to_pydantic_model.assert_awaited_once_with("<html>\n <body>\n  <span>\n   test\n  </span>\n </body>\n</html>\n", OutputModelTest)

