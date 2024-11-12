from fake_useragent import UserAgent
from playwright.async_api import async_playwright

from pyrser_ai.core.parsers.base_parser import BaseParser


class DynamicHTMLParser(BaseParser):
    async def _get_html_content(self, url: str) -> str:
        async with async_playwright() as p:
            ua = UserAgent()
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent=ua.chrome)

            page = await context.new_page()
            await page.goto(url)
            await page.wait_for_load_state("load")
            html_content = await page.content()
            await browser.close()
            return html_content

