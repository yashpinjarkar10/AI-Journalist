

# 🧠 AI-Journalist

**AI-Journalist** is an intelligent news aggregation and reporting tool that leverages artificial intelligence to **collect**, **analyze**, and **summarize** news from various sources, including Reddit and major news outlets. It also features **automated text-to-speech** capabilities for hands-free news consumption.

---

## ✨ Features

* 🔍 **Multi-source news scraping** (Reddit, news websites)
* 🧠 **AI-powered summarization** and analysis
* 🔊 **Text-to-speech** audio generation
* 🧩 **Modular backend** for easy extension and customization
* 💻 **Professional & user-friendly interface**

---

## ⚙️ Installation

1. **Clone the repository:**

   ```powershell
   git clone https://github.com/yashpinjarkar10/AI-Journalist.git
   cd AI-Journalist
   ```

2. **Create and activate a virtual environment:**

   ```powershell
   python -m venv .venv
   & .venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**

   ```powershell
   pip install -r requirements.txt
   ```

---

## 🚀 Usage

Run the main application:

```powershell
python main.py
```

---

## 🧰 Technologies Used

* **Python 3.10+** — Core programming language
* **BeautifulSoup & Requests** — Web scraping and data extraction
* **PRAW** — Reddit API integration
* **gTTS / pyttsx3** — Text-to-speech audio generation
* **FastAPI / Flask** — Backend API
* **More** — See `requirements.txt` for the full list

---

## 🔄 Workflow

1. **Scraping** — Collects news articles and Reddit posts via:

   * `news_scraper.py`
   * `reddit_scraper.py`

2. **Processing** — Cleans and summarizes content using AI utilities from `utils.py`

3. **Audio Generation** — Converts summaries into MP3 audio using a TTS engine

4. **Serving** — Serves content and audio files via API (`backend.py`)

5. **Orchestration** — Ties everything together through `main.py`

---

### 📊 Workflow Diagram

```
[Sources]
   | (news_scraper.py, reddit_scraper.py)
   v
[Raw News Data]
   | (utils.py)
   v
[Summarized Content]
   | (TTS Engine)
   v
[Audio Files]
   | (backend.py)
   v
[API / User Interface]
```

---

## 🧪 Example Output

* **Text Summary:**

  > "AI-Journalist aggregates the latest news and provides concise summaries for quick reading."

* **Audio File:**

  > Saved as: `audio/tts_YYYYMMDD_HHMMSS.mp3`

---

## 📁 Module Overview

| File                | Purpose                                                 |
| ------------------- | ------------------------------------------------------- |
| `main.py`           | Entry point, manages overall workflow and orchestration |
| `news_scraper.py`   | Scrapes news websites                                   |
| `reddit_scraper.py` | Scrapes Reddit posts via PRAW                           |
| `models.py`         | Data models for articles and summaries                  |
| `utils.py`          | Utility functions for cleaning, summarizing, formatting |
| `backend.py`        | FastAPI/Flask server for API access                     |

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

