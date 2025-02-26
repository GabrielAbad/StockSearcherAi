import os

from langchain.tools import tool

from yahooquery import Ticker
from googleapiclient.discovery import build


class SearchTools():

  @tool("Stock Price Quote")
  def fetch_stock_price(ticker: str) -> str:
    """Fetch the latest stock price for a given ticker symbol."""
    try:
        stock = Ticker(ticker)
        stock_data = stock.price.get(ticker, {})

        if not isinstance(stock_data, dict):
            return f"Error fetching stock price: {stock_data}"

        price = stock_data.get("regularMarketPrice")

        if price is None:
            return f"Could not fetch stock price for {ticker}."

        return f"The stock {ticker} is currently priced at {price:.2f} USD."
    except Exception as e:
        return f"Error fetching stock price for {ticker}: {str(e)}"

  @tool("Search YouTube Videos")
  def fetch_youtube_videos(query: str) -> str:
    """Fetch 5 relevant YouTube videos for the given query and return only links."""
    api_key = os.environ["YOUTUBE_API_KEY"]
    if not api_key:
        return "Error: API key not found."

    try:
        youtube = build("youtube", "v3", developerKey=api_key)

        request = youtube.search().list(
            q=query,
            part="snippet",
            maxResults=5,
            type="video"
        )
        response = request.execute()

        video_links = []
        for item in response["items"]:
            video_id = item["id"]["videoId"]
            video_links.append(f"https://www.youtube.com/watch?v={video_id}")

        return "\n".join(video_links) if video_links else "No videos found."
    except Exception as e:
        return f"Error fetching videos: {str(e)}"