from crewai import Crew
from textwrap import dedent

from agents import StockAnalysisAgents
from tasks import StockAnalysisTasks

from dotenv import load_dotenv
load_dotenv()

class FinancialCrew:
  def __init__(self, user_input):
    self.user_input = user_input

  def run(self):
    agents = StockAnalysisAgents()
    tasks = StockAnalysisTasks()

    # Criar todos os agentes
    entity_extractor_agent = agents.entity_extractor_agent()
    stock_price_agent = agents.stock_price_agent()
    youtube_video_agent = agents.youtube_video_agent()
    response_builder_agent = agents.response_builder_agent()

    # Criar a tarefa de extração do nome da empresa
    extract_company_task = tasks.extract_company_name(entity_extractor_agent, self.user_input)

    # As tarefas que dependem da extração
    stock_price_task = tasks.fetch_stock_price(stock_price_agent, extract_company_task)
    youtube_videos_task = tasks.fetch_youtube_videos(youtube_video_agent, extract_company_task)

    # Tarefa final que junta os resultados
    final_response_task = tasks.build_final_response(response_builder_agent, stock_price_task, youtube_videos_task)

    # Criar a crew com todos os agentes e tarefas
    crew = Crew(
        agents=[
            entity_extractor_agent,
            stock_price_agent,
            youtube_video_agent,
            response_builder_agent
        ],
        tasks=[
            extract_company_task,
            stock_price_task,
            youtube_videos_task,
            final_response_task
        ],
        verbose=True
    )

    result = crew.kickoff()
    return result

if __name__ == "__main__":
  print("## Welcome to Financial Analysis Crew")
  print('-------------------------------')
  user_input = input(
    dedent("""
      What do you want to know?
    """))
  
  financial_crew = FinancialCrew(user_input)
  result = financial_crew.run()
  print("\n\n########################")
  print("## Here is the Report")
  print("########################\n")
  print(result)
