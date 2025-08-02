import base64
from fastapi import FastAPI, HTTPException, File, Response
from dotenv import load_dotenv
from models import NewsRequest
from reddit_scraper import scrape_reddit_topics
from news_scraper import NewsScraper
from utils import *
import os

app = FastAPI()
load_dotenv()

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "FastAPI server is running"}
 
@app.post("/generate-news-audio")
async def generate_news_audio(request: NewsRequest):
    print(f"Received request: topics={request.topics}, source_type={request.source_type}")
    try:
        results = {}

        # Scrape the data
        if request.source_type in ["both", "news"]:
            # scrape news articles
            news_scraper = NewsScraper()
            results["news"] = await news_scraper.scrape_news(request.topics)

        if request.source_type in ["both", "reddit"]:
            results["reddit"] = await scrape_reddit_topics(request.topics)


        news_data = results.get("news", {})
        reddit_data = results.get("reddit", {})


        # LLM To Do Summary
        news_summary = generate_broadcast_news(
            api_key=os.getenv("GEMINI_API_KEY"),
            news_data = news_data,
            reddit_data= reddit_data,
            topics= request.topics
            )
        
        # Convert Summary to Audio

        audio_path = tts_to_audio(
            text=news_summary,
            language='en'
        )

        if audio_path:
            with open(audio_path, "rb") as f:
                audio_bytes = f.read()
            
            return {
                "summary": news_summary,
                "audio": base64.b64encode(audio_bytes).decode("utf-8")
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to generate audio file")
        

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend:app",
        host="0.0.0.0",
        port=1234,
        reload=True
    )