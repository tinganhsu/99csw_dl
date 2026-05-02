from bs4 import BeautifulSoup
from urllib.parse import urljoin
from ..models import Book, Chapter
from .decoder import NinetyNineDecoder

class NinetyNineParser:
    BASE_URL = "https://read.99csw.com"

    @classmethod
    def parse_catalog(cls, book_id: str, html_content: str) -> Book:
        """解析書籍目錄頁面"""
        soup = BeautifulSoup(html_content, "lxml")
        
        # 提取書名
        title_tag = soup.select_one(".book_info h2") or soup.find("h2")
        title = title_tag.get_text().strip() if title_tag else "未知書名"
        
        # 提取作者
        author = "未知作者"
        # 尋找包含 "作者：" 的 div 內的 a 標籤
        author_link = soup.select_one(".book_info div:-soup-contains('作者：') a") or soup.select_one(".book_info div a[href*='/author/']")
        if author_link:
            author = author_link.get_text().strip()
        
        # 提取類別
        category = "小說"
        # 尋找包含 "類別：" 的 div 內的 a 標籤
        category_link = soup.select_one(".book_info div:-soup-contains('類別：') a") or soup.select_one(".book_info div a[href*='type=']")
        if category_link:
            category = category_link.get_text().strip()
        
        # 提取封面
        cover_tag = soup.select_one(".cover img") or soup.select_one("img")
        cover_url = ""
        if cover_tag:
            src = cover_tag.get("src")
            if src:
                cover_url = urljoin(cls.BASE_URL, src)
        
        # 提取目錄
        chapters = []
        catalog_box = soup.find(id="dir") or soup.select_one(".dir_box")
        if catalog_box:
            for link in catalog_box.find_all("a"):
                href = link.get("href")
                if href and "/book/" in href:
                    full_url = urljoin(cls.BASE_URL, href)
                    chapters.append(Chapter(
                        title=link.get_text().strip(),
                        url=full_url
                    ))
        
        return Book(
            book_id=book_id,
            title=title,
            author=author,
            category=category,
            cover_url=cover_url,
            chapters=chapters
        )

    @classmethod
    def parse_chapter_content(cls, html_content: str, is_epub: bool = True) -> str:
        """解析單章內容並呼叫解碼器"""
        soup = BeautifulSoup(html_content, "lxml")
        
        # 獲取密鑰
        meta_client = soup.find("meta", attrs={"name": "client"})
        client_key = meta_client.get("content") if meta_client else ""
        
        # 解碼內容
        return NinetyNineDecoder.decode_content(html_content, client_key, is_epub)
