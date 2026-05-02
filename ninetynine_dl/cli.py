import asyncio
import typer
import os
import re
from rich import print
from rich.console import Console
from .models import AppConfig
from .core.downloader import NinetyNineDownloader
from .utils.epub_builder import EpubBuilder

app = typer.Typer(help="99dl Python 3.14 重構版 - 從 read.99csw.com 下載書籍")
console = Console()

def sanitize_filename(filename: str) -> str:
    """過濾掉檔名中的危險字元，防止路徑遍歷攻擊"""
    return re.sub(r'[\\/*?:"<>|]', "", filename).replace("..", "").strip()

async def download_task(book_id: str, format: str, threads: int):
    # 驗證 book_id 是否為純數字，防止注入
    if not book_id.isdigit():
        print(f"[bold red]❌ 錯誤：書籍 ID 必須為純數字。[/bold red]")
        return

    config = AppConfig(output_format=format, threads=threads)
    downloader = NinetyNineDownloader(config)
    
    try:
        # 1. 抓取目錄
        print(f"[bold blue]正在抓取書籍 ID: {book_id} 的資訊...[/bold blue]")
        book = await downloader.fetch_catalog(book_id)
        
        # 安全處理書名
        safe_title = sanitize_filename(book.title)
        print(f"[bold green]找到書籍：{safe_title} (作者: {book.author})，共 {len(book.chapters)} 章[/bold green]")
        
        # 2. 下載內容
        await downloader.download_book(book)
        
        # 3. 匯出
        output_filename = f"{safe_title}.{format}"
        output_path = os.path.join(config.download_dir, output_filename)
        
        if format == "epub":
            EpubBuilder.build(book, output_path)
        else:
            # TXT 輸出
            os.makedirs(config.download_dir, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                for chap in book.chapters:
                    f.write(f"{chap.title}\n\n{chap.content}\n\n\n")
        
        print(f"\n[bold green]✨ 下載完成！檔案已儲存至: {output_path}[/bold green]")
        
    except Exception as e:
        print(f"[bold red]❌ 發生錯誤：{str(e)}[/bold red]")
    finally:
        await downloader.close()

@app.command()
def download(
    book_id: str = typer.Argument(..., help="書籍 ID (例如 288)"),
    format: str = typer.Option("epub", "--format", "-f", help="輸出格式: epub 或 txt"),
    threads: int = typer.Option(3, "--threads", "-t", help="並發下載執行緒數")
):
    """下載指定 ID 的書籍"""
    asyncio.run(download_task(book_id, format, threads))

if __name__ == "__main__":
    app()
