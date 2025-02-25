from src.flow import StockAnalysisFlow

if __name__ == "__main__":
    flow = StockAnalysisFlow()  # Não precisa mais de um estado inicial separado
    flow.kickoff()
