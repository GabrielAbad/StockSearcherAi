import os
from yahooquery import Ticker
from langchain.tools import tool
from googleapiclient.discovery import build
from dotenv import load_dotenv  # ✅ Biblioteca para carregar o .env

# Carregar variáveis de ambiente do .env
load_dotenv()

@tool("cotacao_acao")
def buscar_cotacao(ticker: str) -> str:
    """Retorna a cotação atual da ação informada."""
    try:
        acao = Ticker(ticker)
        dados_acao = acao.price.get(ticker, {})

        if not isinstance(dados_acao, dict):  # Verifica se o retorno é válido
            return f"Erro ao obter cotação: {dados_acao}"  # Exibe o erro retornado pela API

        preco = dados_acao.get("regularMarketPrice")

        if preco is None:
            return f"Não foi possível obter a cotação para {ticker}."

        return f"A ação {ticker} está cotada a {preco:.2f} USD."
    except Exception as e:
        return f"Erro ao buscar cotação da ação {ticker}: {str(e)}"

@tool("buscar_videos")
def buscar_videos_youtube(query: str) -> str:
    """Busca 5 vídeos relevantes no YouTube sobre a ação informada e retorna apenas os links."""
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        return "Erro: Chave da API não encontrada."

    try:
        # Cria o serviço da API do YouTube
        youtube = build("youtube", "v3", developerKey=api_key)

        # Faz a requisição de busca
        request = youtube.search().list(
            q=query,  # Termo de busca
            part="snippet",  # Parte da resposta que queremos
            maxResults=5,  # Número máximo de resultados
            type="video"  # Tipo de resultado (somente vídeos)
        )
        response = request.execute()

        # Extrai os links dos vídeos
        video_links = []
        for item in response["items"]:
            video_id = item["id"]["videoId"]
            video_links.append(f"https://www.youtube.com/watch?v={video_id}")

        return "\n".join(video_links) if video_links else "Nenhum vídeo encontrado."
    except Exception as e:
        return f"Erro ao buscar vídeos: {str(e)}"
