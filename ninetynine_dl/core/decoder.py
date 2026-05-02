import base64
import re
from bs4 import BeautifulSoup
from typing import List

class NinetyNineDecoder:
    @staticmethod
    def decode_content(html_content: str, client_key: str = None, is_epub: bool = True) -> str:
        """
        還原內容，支援加密重排與直接提取兩種模式
        """
        soup = BeautifulSoup(html_content, "lxml")
        # 新版使用 article#content, 舊版使用 div#content
        content_box = soup.find(id="content")
        if not content_box:
            return ""

        # 1. 移除所有干擾標籤
        junk_tags = "strike,acronym,bdo,big,site,code,dfn,kbd,q,s,samp,tt,u,var,cite,details,figure"
        for tag in soup.select(junk_tags):
            tag.decompose()

        # 2. 如果有密鑰，進行重排邏輯
        if client_key:
            try:
                decoded_key = base64.b64decode(client_key).decode("utf-8")
                indices_raw = re.split(r"[A-Z]+%", decoded_key)
                indices = [int(i) for i in indices_raw if i]

                children = content_box.find_all(recursive=False)
                # 過濾掉 h2 標題
                content_nodes = [c for c in children if c.name != "h2"]
                
                # 如果節點數量與索引匹配，進行重排
                if len(content_nodes) >= len(indices):
                    result_nodes = [""] * len(indices)
                    j = 0
                    for i, idx_val in enumerate(indices):
                        target_idx = idx_val if idx_val < 3 else idx_val - j
                        if idx_val < 3: j += 1
                        else: j += 2
                        
                        if target_idx < len(indices) and i < len(content_nodes):
                            result_nodes[target_idx] = content_nodes[i].get_text().strip()
                    
                    if is_epub:
                        return "".join(f"<p>{node}</p>" for node in result_nodes if node)
                    else:
                        return "\n".join(node for node in result_nodes if node)
            except Exception:
                pass # 如果重排失敗，回退到直接提取

        # 3. 直接提取模式 (無密鑰或重排失敗)
        paragraphs = []
        for child in content_box.find_all(recursive=False):
            if child.name in ["p", "div", "section"] and child.name != "h2":
                text = child.get_text().strip()
                if text:
                    paragraphs.append(text)
        
        if is_epub:
            return "".join(f"<p>{p}</p>" for p in paragraphs)
        else:
            return "\n".join(paragraphs)
