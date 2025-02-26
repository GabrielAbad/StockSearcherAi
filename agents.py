from crewai import Agent
from langchain_openai import ChatOpenAI

from tools.search_tools import SearchTools

class StockAnalysisAgents():
  def __init__(self):
    self.llm = ChatOpenAI(
      model="crewai-mistral",
      base_url="http://localhost:11434/v1",
      api_key="NA"
    )

  def entity_extractor_agent(self):
    return Agent(
      role='Entity Extractor',
      goal="Identify the company name from a user-provided request",
      backstory="An expert NLP model that extracts company names from text input.",
      verbose=True,
      llm=self.llm
    )
  
  def youtube_video_agent(self):
    return Agent(
      role='YouTube Video Finder',
      goal="Find YouTube videos about a given stock",
      backstory="Expert at fetching financial-related YouTube videos.",
      verbose=True,
      tools=[SearchTools.fetch_youtube_videos],
      llm=self.llm
    )

  def stock_price_agent(self):
    return Agent(
      role='Stock Price Fetcher',
      goal="Retrieve the latest stock price for a given company",
      backstory="Real-time stock price retriever using financial APIs.",
      verbose=True,
      tools=[SearchTools.fetch_stock_price],
      llm=self.llm
    )
  
  def response_builder_agent(self):
    return Agent(
        role='Final Response Builder',
        goal="Combine stock price and YouTube video links results into a structured response.",
        backstory="A financial assistant who consolidates multiple sources of data into a readable and insightful report.",
        verbose=True,
        llm=self.llm
    )
