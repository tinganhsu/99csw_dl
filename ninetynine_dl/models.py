from pydantic import BaseModel, Field
from typing import List, Optional

class Chapter(BaseModel):
    title: str
    url: str
    content: Optional[str] = None

class Book(BaseModel):
    book_id: str
    title: str
    author: str
    category: str = "小說"
    cover_url: str
    chapters: List[Chapter] = []

class AppConfig(BaseModel):
    download_dir: str = "./downloads"
    threads: int = 3
    timeout: int = 10
    proxy: Optional[str] = None
    output_format: str = "epub"  # epub or txt
