# pyrser

Transform any HTML page into a Pydantic-based schema using pyrser. This tool allows you to easily extract data from HTML
pages, including both static and dynamic content, and map it to structured Pydantic models.

## Installation

By default, pyrser installs only the necessary libraries for parsing static HTML pages (those not requiring JavaScript
execution). To parse dynamic pages (those that rely on JavaScript), additional dependencies are required.

### Installation for Static HTML Only

```bash
pip install pyrser-ai
```

### Installation for Both Static and Dynamic HTML

```bash
pip install pyrser-ai[full]
playwright install
```

## Usage

pyrser leverages LlamaIndex under the hood to parse HTML content and automatically generate schemas. By default, it uses
OpenAI’s gpt-4o-mini model, but you can customize the model by passing the model parameter to the extractor or
configuring your own LlamaIndex instance.

You can also define HTML tags to exclude from parsing by providing a list via the tags_to_remove parameter in the parse
function. If no list is specified, the default set of tags will be ignored.

### Default Tags Excluded

```python
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
```

### Example Usages

#### Parsing Static HTML with the default configuration

```python
import aiohttp

from pyrser_ai.core.parsers.static_html_parser import StaticHTMLParser
from pyrser_ai.core.extractors.llama_index_extractor import LlamaIndexExtractor
from pydantic import BaseModel


class MyModel(BaseModel):
    title: str
    description: str


async def main():
    async with aiohttp.ClientSession() as session:
        extractor = LlamaIndexExtractor()
        parser = StaticHTMLParser(extractor=extractor, http_client=session)

        output_model = await parser.parse("https://www.example.com", MyModel)
```

#### Parsing Static HTML with a Custom Model

```python
import aiohttp

from pyrser_ai.core.parsers.static_html_parser import StaticHTMLParser
from pyrser_ai.core.extractors.llama_index_extractor import LlamaIndexExtractor
from pydantic import BaseModel


class MyModel(BaseModel):
    title: str
    description: str


async def main():
    async with aiohttp.ClientSession() as session:
        extractor = LlamaIndexExtractor(model="gpt-3.5-turbo")
        parser = StaticHTMLParser(extractor=extractor, http_client=session)

        output_model = await parser.parse("https://www.example.com", MyModel)
```

#### Parsing Static HTML with a Custom LLM Instance

```python
import aiohttp

from pyrser_ai.core.parsers.static_html_parser import StaticHTMLParser
from pyrser_ai.core.extractors.llama_index_extractor import LlamaIndexExtractor
from pydantic import BaseModel
from llama_index.llms.anthropic import Anthropic


class MyModel(BaseModel):
    title: str
    description: str


async def main():
    llm = Anthropic(model="claude-3-sonnet-20240229")

    async with aiohttp.ClientSession() as session:
        extractor = LlamaIndexExtractor(llm=llm)
        parser = StaticHTMLParser(extractor=extractor, http_client=session)

        output_model = await parser.parse("https://www.example.com", MyModel)
```

#### Parsing Dynamic HTML with a Custom Model

```python
from pyrser_ai.core.parsers.dynamic_html_parser import DynamicHTMLParser
from pyrser_ai.core.extractors.llama_index_extractor import LlamaIndexExtractor
from pydantic import BaseModel


class MyModel(BaseModel):
    title: str
    description: str


async def main():
    extractor = LlamaIndexExtractor(model="gpt-3.5-turbo")
    parser = DynamicHTMLParser(extractor=extractor)

    output_model = await parser.parse("https://www.example.com", MyModel)
```

### Additional Information

- Model Customization: You can specify any supported LLM model in LlamaIndexExtractor by passing the model name to the
  model parameter.
- Excluded Tags: To change the HTML tags excluded during parsing, provide a custom tags_to_remove list. By default,
  common non-content tags (e.g., img, button, style) are excluded.