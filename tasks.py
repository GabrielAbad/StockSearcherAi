from crewai import Task
from textwrap import dedent

class StockAnalysisTasks():
  
  def extract_company_name(self, agent, user_input):
    return Task(description=dedent(f"""
        Extract the company name from the following user input:
        "{user_input}"

        Provide only the extracted company name as output.
      """),
      agent=agent
    )

  def fetch_stock_price(self, agent, extract_company_task):
    return Task(description=dedent(f"""
        Retrieve the latest stock price for the extracted company.
        Ensure accuracy and provide the output in a clear format.
      """),
      agent=agent,
      context=[extract_company_task]  # Aqui garantimos que o nome extraído é usado
    )

  def fetch_youtube_videos(self, agent, extract_company_task):
    return Task(description=dedent(f"""
        Search for the top 5 most relevant YouTube videos links about the extracted company.
        Focus on recent content discussing financial trends and expert opinions.
      """),
      agent=agent,
      context=[extract_company_task]  # Aqui também usamos o nome extraído
    )
  
  def build_final_response(self, agent, stock_price_task, youtube_videos_task):
    return Task(
        description=dedent(f"""
            Gather and structure the information retrieved by the other agents.
            
            - **Stock Price Information:** Use the results from the stock price task.
            - **YouTube Videos:** Use the results from the YouTube video task.
            
            Format the response clearly, ensuring that it provides useful insights in an easy-to-read format.
        """),
        agent=agent,
        context=[stock_price_task, youtube_videos_task]  # Usa os resultados das buscas
    )
