# Instagram Scraper for Python

<div align="center">

<img src="https://img.shields.io/badge/Thordata-Official-blue?style=for-the-badge" alt="Thordata Logo">

**Extract Instagram posts, profiles, reels, and comments at scale.**  
*Powered by Thordata's residential proxy network & Web Scraper API.*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Powered By](https://img.shields.io/badge/Powered%20By-Thordata-orange)](https://dashboard.thordata.com/?utm_source=github&utm_medium=readme&utm_campaign=instagram_scraper)

</div>

---

## ⚡ Features

- **📸 Posts**: Scrape posts by profile URL or post URL with date range filtering.
- **👤 Profiles**: Extract profile information by username or profile URL.
- **🎬 Reels**: Get reel details by URL or list all reels from a profile.
- **💬 Comments**: Extract comments from posts and reels.
- **🛡️ Anti-Bot Bypass**: Automatically handles CAPTCHAs, IP rotation, and headers.
- **📅 Date Filtering**: Filter posts/reels by start and end dates.
- **🔍 Post Type Filtering**: Filter by Post, Reel, or both.

## 🚀 Quick Start

### 1. Get Credentials

Get your **free** scraping token from the [Thordata Dashboard](https://dashboard.thordata.com/?utm_source=github&utm_medium=readme&utm_campaign=instagram_scraper).

### 2. Install

```bash
git clone https://github.com/Thordata/instagram-scraper-python.git
cd instagram-scraper-python
pip install -r requirements.txt
```

### 3. Configure

Copy `.env.example` to `.env` and fill in your tokens:

```ini
THORDATA_SCRAPER_TOKEN=your_token
THORDATA_PUBLIC_TOKEN=your_public
THORDATA_PUBLIC_KEY=your_key
```

### 4. Run Examples

**Get Posts by Profile:**
```bash
python main.py posts --profile "https://www.instagram.com/marcusfaberfdp" --limit 5 --start-date "01-01-2025" --end-date "03-01-2025"
```

**Get Post Details:**
```bash
python main.py post "https://www.instagram.com/p/Cuf4s0MNqNr"
```

**Get Reel Details:**
```bash
python main.py reel "https://www.instagram.com/reel/C4GLo_eLO2e/"
```

**Get Comments:**
```bash
python main.py comments "https://www.instagram.com/cats_of_instagram/reel/C4GLo_eLO2e/"
```

**Get Profile Info (by username):**
```bash
python main.py profile "username"
```

**Get Profile Info (by URL):**
```bash
python main.py profile "https://www.instagram.com/username"
```

**Get Reels from Profile:**
```bash
python main.py reels "https://www.instagram.com/username" --limit 10
```

**Get Reels List from Profile:**
```bash
python main.py reels-list "https://www.instagram.com/username" --limit 10 --start-date "01-28-2025" --end-date "01-28-2026"
```

All data is saved to `output/` in JSON format. If a task fails, error details are saved to `output/error_*.json`.

---

## 🏗️ How it Works

This scraper uses **Thordata's Web Scraper API (Hybrid Mode)**:
1.  **Task Creation**: Sends scraping parameters to Thordata's cloud cluster.
2.  **Auto-Polling**: The SDK (`run_task`) automatically polls for completion.
3.  **Result Retrieval**: Downloads the clean JSON data once ready.

This architecture ensures you **never get IP blocked** and don't need to maintain local headless browsers.

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
