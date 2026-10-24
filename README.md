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

This architecture uses Thordata's Web Scraper API and proxy infrastructure, so the example does not require local browser automation.

---

## What This Example Does Not Collect

This repository is an example client for authorized Thordata Web Scraper API requests. It does not include Instagram login cookies, private account access, or browser session data.

The example does not grant rights to access, reuse, train on, or redistribute third-party content. Use it only for lawful and authorized data workflows.

Never place API keys, cookies, personal information, or private data in source files, logs, README files, or commits.

## Failure Behavior

An API request may fail because of invalid credentials, unsupported parameters, rate limits, endpoint restrictions, or temporary service errors.

When a request fails, treat the response as an error rather than valid Instagram data. Check the terminal output and returned API response for details. Exact error codes and limits depend on the account and endpoint.

## For Coding Assistants

When modifying or running this example:

- Read `.env.example` and keep credentials in environment variables.
- Check `src/config.py` before inventing scraper IDs or request parameters.
- Follow the existing README examples and preserve the current request flow.
- Never print or commit API keys, cookies, private URLs, or personal data.
- Review returned profile, post, reel, or comment data before sharing it.
- Treat returned Instagram data as third-party data subject to applicable terms and usage restrictions.

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
