# pyrser

Transform any HTML page or Document into a Pydantic-based schema using pyrser. This tool allows you to easily extract data from a HTML, PDF, DOC, DOCX, TXT, etc
pages, including both static and dynamic content, and map it to structured Pydantic models.

## Installation

By default, pyrser installs only the necessary libraries for parsing static HTML pages (those not requiring JavaScript
execution) and documents. To parse dynamic pages (those that rely on JavaScript), additional dependencies are required.

### Installation for Static HTML Only

```bash
pip install pyrser-ai
```

### Installation for Both Static and Dynamic HTML

```bash
pip install pyrser-ai[full]
playwright install
```

## Requirements
To use the default configuration make sure that you have a OpenAI account and a LlamaParse account.
- Create your LlamaParse account at https://cloud.llamaindex.ai/api-key (free up to 1000 pages/day - used for documents only)
- Create your OpenAI account at https://platform.openai.com/signup 

## Usage

pyrser leverages LlamaIndex and LlamaParse under the hood to parse documents and HTML content and automatically generate schemas. By default, it uses
OpenAI’s gpt-4o-mini model, but you can customize the model by passing the model parameter to the extractor or
configuring your own LlamaIndex instance.

You can also define HTML tags to exclude from parsing by providing a list via the tags_to_remove parameter in the parse
function. If no list is specified, the default set of tags will be ignored.

### Default HTML Tags Excluded

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

#### Parsing a PDF Document with the default configuration
```python
from pydantic import BaseModel, Field
from datetime import datetime
import io
from pyrser_ai.core.parsers.file.file_parser import FileParser

class MyModel(BaseModel):
    cnpj: str = Field(description="The CNPJ of the company")
    due_date: datetime = Field(description="The due date of the document")
    total: float = Field(description="The total value of the document")
    

async def main():
  with open("doc_pdf.pdf", "rb") as f:
      f_bytes = io.BytesIO(f.read())
      f_bytes.seek(0)
  
      result = await FileParser().parse_document(document=f_bytes, file_name="impostos.pdf", output_model=MyModel)
      print(result)

```
#### Parsing Static HTML with the default configuration

```python
import aiohttp

from pyrser_ai.core.parsers.html.static_html_parser import StaticHTMLParser
from pydantic import BaseModel


class MyModel(BaseModel):
  title: str
  description: str


async def main():
  async with aiohttp.ClientSession() as session:
    parser = StaticHTMLParser(http_client=session)

    output_model = await parser.parse("https://www.example.com", MyModel)
```

#### Parsing Static HTML with a Custom Model

```python
import aiohttp

from pyrser_ai.core.parsers.html.static_html_parser import StaticHTMLParser
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

from pyrser_ai.core.parsers.html.static_html_parser import StaticHTMLParser
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
from pyrser_ai.core.parsers.html.dynamic_html_parser import DynamicHTMLParser
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
- Some environment variables are needed in order to use the default configuration
  - OPENAI_API_KEY=
  - LLAMA_CLOUD_API_KEY=
- Model Customization: You can specify any supported LLM model in LlamaIndexExtractor by passing the model name to the
  model parameter.
- Excluded Tags: To change the HTML tags excluded during parsing, provide a custom tags_to_remove list. By default,
  common non-content tags (e.g., img, button, style) are excluded.