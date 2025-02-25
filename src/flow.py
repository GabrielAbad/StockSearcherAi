from crewai.flow.flow import Flow, listen, start
from src.tools.custom_tools import buscar_cotacao, buscar_videos_youtube

class StockAnalysisFlow(Flow):

    @start()
    def buscar_cotacao(self):
        """Obtém a cotação da ação e armazena no estado interno."""
        ticker = input("Digite o código da ação (ex: AAPL, TSLA, MSFT): ").upper()
        self.state["ticker"] = ticker  # Armazena o ticker no estado interno

        resultado = buscar_cotacao(ticker)
        self.state["cotacao"] = resultado  # Salva a cotação no estado interno

        print("\n📈 Cotação da Ação:")
        print(resultado)

    @listen(buscar_cotacao)
    def buscar_videos(self):
        """Obtém os vídeos sobre a ação e armazena no estado interno."""
        ticker = self.state["ticker"]
        resultado = buscar_videos_youtube(ticker)
        self.state["videos"] = resultado.split("\n")  # Lista de vídeos no estado interno

        print("\n🎥 Vídeos Relevantes sobre a Ação:")
        for link in self.state["videos"]:
            print(f"- {link}")

