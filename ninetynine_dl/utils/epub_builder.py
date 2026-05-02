import os
from ebooklib import epub
from ..models import Book

class EpubBuilder:
    @staticmethod
    def build(book: Book, output_path: str):
        epub_book = epub.EpubBook()
        
        # 設定中繼資料
        epub_book.set_identifier(f"99csw-{book.book_id}")
        epub_book.set_title(book.title)
        epub_book.set_language("zh-TW")
        epub_book.add_author(book.author)
        epub_book.add_metadata('DC', 'subject', book.category)
        
        # 建立章節
        spine = ["nav"]
        toc = []
        
        for i, chapter in enumerate(book.chapters):
            c = epub.EpubHtml(
                title=chapter.title,
                file_name=f"chap_{i}.xhtml",
                content=f"<h1>{chapter.title}</h1>{chapter.content}"
            )
            epub_book.add_item(c)
            toc.append(c)
            spine.append(c)
        
        epub_book.toc = tuple(toc)
        epub_book.spine = spine
        epub_book.add_item(epub.EpubNav())
        
        # 確保目錄存在
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        # 寫入檔案
        epub.write_epub(output_path, epub_book)
