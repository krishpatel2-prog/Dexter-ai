from pydantic import BaseModel, Field
import httpx
from bs4 import BeautifulSoup
from src.agent.tools.base import BaseTool

class WebScrapeInput(BaseModel):
    url: str = Field(..., description="The full URL of the website to scrape (e.g. 'https://example.com').")

class WebScrapeTool(BaseTool):
    name = "web_scrape"
    description = "Scrape and extract the main content from a website."
    input_schema = WebScrapeInput
    
    async def execute(self, url: str) -> str:
        from urllib.parse import urlparse
        import socket
        import ipaddress

        url = url.strip()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            raise ValueError(f"Invalid URL scheme: {parsed.scheme}")

        try:
            ip = socket.gethostbyname(parsed.hostname)
            if ipaddress.ip_address(ip).is_private or ipaddress.ip_address(ip).is_loopback:
                raise ValueError("Access to private/internal networks is forbidden.")
        except Exception as e:
            if "forbidden" in str(e):
                raise
            # If resolution fails, let the client handle the error.

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        try:
            async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
                resp = await client.get(url, headers=headers)
                resp.raise_for_status()
                html = resp.text
        except Exception as e:
            raise Exception(f"Failed to scrape {url}: {str(e)}")

        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
            tag.decompose()

        content = soup.get_text(separator="\n", strip=True)
        if len(content) > 15000:
            content = content[:15000] + "\n...[Content truncated for length]..."

        return f"Source: {url}\n\n{content}"

