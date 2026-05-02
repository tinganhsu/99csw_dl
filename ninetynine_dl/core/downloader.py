import asyncio
import httpx
from typing import List, Optional
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn
from ..models import Book, Chapter, AppConfig
from .parser import NinetyNineParser

class NinetyNineDownloader:
    def __init__(self, config: AppConfig):
        self.config = config
        self.semaphore = asyncio.Semaphore(config.threads)
        self.client = httpx.AsyncClient(
            timeout=config.timeout,
            proxy=config.proxy,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "Referer": "https://read.99csw.com/"
            },
            follow_redirects=True
        )

    async def fetch_catalog(self, book_id: str) -> Book:
        url = f"https://read.99csw.com/book/{book_id}/"
        resp = await self.client.get(url)
        resp.raise_for_status()
        return NinetyNineParser.parse_catalog(book_id, resp.text)

    async def download_chapter(self, chapter: Chapter, is_epub: bool):
        async with self.semaphore:
            for attempt in range(3):  # 失敗重試 3 次
                try:
                    resp = await self.client.get(chapter.url)
                    resp.raise_for_status()
                    chapter.content = NinetyNineParser.parse_chapter_content(resp.text, is_epub)
                    return
                except Exception as e:
                    if attempt == 2:
                        chapter.content = f"下載失敗：{str(e)}"
                    await asyncio.sleep(1)

    async def download_book(self, book: Book):
        is_epub = self.config.output_format == "epub"
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
        ) as progress:
            task = progress.add_task(f"正在下載: {book.title}", total=len(book.chapters))
            
            tasks = []
            for chapter in book.chapters:
                coro = self.download_chapter(chapter, is_epub)
                tasks.append(self._wrap_task(coro, progress, task))
            
            await asyncio.gather(*tasks)

    async def _wrap_task(self, coro, progress, task_id):
        await coro
        progress.update(task_id, advance=1)

    async def close(self):
        await self.client.aclose()
