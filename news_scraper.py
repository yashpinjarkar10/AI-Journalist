import asyncio
import os
from typing import Dict, List
from dotenv import load_dotenv

from aiolimiter import AsyncLimiter
from tenacity import retry, stop_after_attempt, wait_exponential

from utils import *



load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import (
    create_async_playwright_browser,  # A synchronous browser is available, though it isn't compatible with jupyter.\n",	  },
)

async def extract_news_urls_to_scrape(topics: List[str]) -> Dict[str, str]:
    """
    Generate a dictionary of Google News search URLs for each topic.
    
    Args:
        topics: List of topics to generate URLs for
        
    Returns:
        Dict[str, str]: Dictionary mapping topic to News search URL
    """
    async_browser = create_async_playwright_browser()
    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
    tools = toolkit.get_tools()
    tools_by_name = {tool.name: tool for tool in tools}
    navigate_tool = tools_by_name["navigate_browser"]
    get_elements_tool = tools_by_name["get_elements"]

    for url in generate_valid_news_url(topics):
        await navigate_tool.arun(
            {"url": url}
        )
    

    from langchain_google_genai import ChatGoogleGenerativeAI
    from langgraph.prebuilt import create_react_agent

    llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            api_key=api_key,temperature=0
        )  # or any other LLM, e.g., ChatOpenAI(), OpenAI()

    agent_chain = create_react_agent(model=llm, tools=tools)
    result = await agent_chain.ainvoke(
    {"messages": [("user", "What are the headers on langchain.com?")]}
)
print(result)






class NewsScraper:
    _rate_limiter = AsyncLimiter(5, 1)  # 5 requests/second

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def scrape_news(self, topics: List[str]) -> Dict[str, str]:
        """Scrape and analyze news articles"""
        results = {}
        
        for topic in topics:
            async with self._rate_limiter:
                try:
                    urls = generate_news_urls_to_scrape([topic])
                    search_html = scrape_with_brightdata(urls[topic])
                    clean_text = clean_html_to_text(search_html)
                    headlines = extract_headlines(clean_text)
                    summary = summarize_with_gemini_news_script(
                        api_key=os.getenv("GEMINI_API_KEY"),
                        headlines=headlines
                    )
                    results[topic] = summary
                except Exception as e:
                    results[topic] = f"Error: {str(e)}"
                await asyncio.sleep(1)  # Avoid overwhelming news sites

        return {"news_analysis" : results}