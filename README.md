# 99dl (Python 3.14 重構版)

[![Python 3.14](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-green.svg)](https://opensource.org/licenses/GPL-3.0)

這是一個將 [99dl](https://github.com/zsakvo/99dl) 從 Node.js 重構為 Python 3.14 的工具，專為從 [read.99csw.com](https://read.99csw.com) 下載書籍並轉換為高品質 **EPUB** 或 **TXT** 格式而設計。

## ✨ 特色

- **現代化非同步架構**：使用 `httpx` 與 `asyncio` 實作高效的併發下載。
- **精準解碼引擎**：完美支援九九藏書的新版解密邏輯，自動還原被打亂的段落並清理干擾標籤。
- **豐富中繼資料**：自動抓取書名、作者與類別，並封裝至 EPUB 的 Metadata 中。
- **精美介面**：使用 `Rich` 庫提供即時下載進度條與彩色終端回饋。
- **安全性增強**：內建輸入驗證與檔名安全過濾，防止路徑遍歷攻擊。

## 🛠️ 安裝方式

1. **複製專案**：
   ```bash
   git clone https://github.com/your-username/99dl.git
   cd 99dl
   ```

2. **建立虛擬環境**：
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   # 或 .\venv\Scripts\activate (Windows)
   ```

3. **安裝依賴套件**：
   ```bash
   pip install .
   ```

## 🚀 使用說明

安裝完成後，您可以直接使用 `99dl` 指令進行操作。

### 下載書籍

您可以透過書籍 ID (URL 中的數字) 來下載書籍。

```bash
# 下載為 EPUB 格式 (預設)
99dl download 4842

# 下載為 TXT 格式
99dl download 288 --format txt

# 指定下載執行緒數量 (預設為 3)
99dl download 4842 --threads 5
```

### 參數說明

- `book_id`：書籍的唯一識別碼（例如 `https://read.99csw.com/book/4842/` 中的 `4842`）。
- `--format`, `-f`：輸出格式，可選 `epub` 或 `txt`。
- `--threads`, `-t`：並發下載的數量。

## 📂 輸出目錄

下載完成的書籍會儲存在專案根目錄下的 `downloads/` 資料夾中。

## ⚠️ 免責聲明

本工具僅供學術交流與個人閱讀習慣研究使用，請勿將下載內容用於任何商業用途。請尊重原作者版權。

## 📜 授權

GPL-3.0-or-later
