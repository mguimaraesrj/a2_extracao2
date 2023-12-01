# Importações
import yfinance as yf
import pandas as pd
import numpy as np
from scipy.stats import norm
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from dataclasses import dataclass
import altair as alt
import streamlit as st
from GoogleNews import GoogleNews

@dataclass
class Ativo:
    ticker: str
    periodo_anterior: str = '1y'
    dias_a_frente: int = 30
    retorno_esperado: float = 0.05

    @staticmethod
    def obter_precos(ticker, periodo):
        ativo = yf.Ticker(ticker)
        historico_ativo = ativo.history(period=periodo)
        return historico_ativo['Close']

    @staticmethod
    def simular_precos(historico_ativo, dias_a_frente, retorno_esperado):
        # ... (código simular_precos continua o mesmo)

    @staticmethod
    def calcular_retorno_probabilidade(caminhos_precos, retorno_esperado):
        # ... (código calcular_retorno_probabilidade continua o mesmo)

    def probabilidade_retorno(self):
        # ... (código probabilidade_retorno continua o mesmo)


class AnalisadorDadosMercado(Ativo):
    # ... (código AnalisadorDadosMercado continua o mesmo)

# Exemplo de uso com Streamlit
st.title("Analisador de Ações")

ticker_interesse = st.text_input("Insira o ticker de interesse (ex: MGLU3):").upper()

# Botões para escolher o período desejado
periodo_opcoes = ["1 mo", "2 mo", "3 mo", "6 mo", "1y", "2y", "3y", "10y", "15y"]
periodo_interesse = st.radio("Escolha o período desejado:", periodo_opcoes + ["Outro"])

# Ajuste do layout para alinhar os botões horizontalmente
col1, col2, col3 = st.columns(3)

# Exibir botões em colunas
with col1:
    st.checkbox("1 mo", value=(periodo_interesse == "1 mo"), key="1mo")

with col2:
    st.checkbox("2 mo", value=(periodo_interesse == "2 mo"), key="2mo")

with col3:
    st.checkbox("3 mo", value=(periodo_interesse == "3 mo"), key="3mo")

# Repita o mesmo padrão para os outros períodos
with col1:
    st.checkbox("6 mo", value=(periodo_interesse == "6 mo"), key="6mo")

with col2:
    st.checkbox("1y", value=(periodo_interesse == "1y"), key="1y")

with col3:
    st.checkbox("2y", value=(periodo_interesse == "2y"), key="2y")

with col1:
    st.checkbox("3y", value=(periodo_interesse == "3y"), key="3y")

with col2:
    st.checkbox("10y", value=(periodo_interesse == "10y"), key="10y")

with col3:
    st.checkbox("15y", value=(periodo_interesse == "15y"), key="15y")

# Campo de entrada manual (exibido/oculto por botão)
if periodo_interesse == "Outro":
    show_manual_input = st.button("Inserir manualmente")
    if show_manual_input:
        periodo_interesse = st.text_input("Insira manualmente o período desejado (ex: 3mo):")

if st.button("Analisar"):
    # Criar instância do AnalisadorDadosMercado
    analisador = AnalisadorDadosMercado()

    # Obter dados
    precos, noticias = analisador.baixar_dados(ticker_interesse, periodo_interesse)

    # Simular preços futuros e calcular probabilidade de retorno
    caminhos_precos = analisador.simular_precos(precos)
    prob_retorno = analisador.calcular_retorno_probabilidade(caminhos_precos)

    # Exibindo resultados e plotando gráficos
    st.write(f"Histórico de Preços para {ticker_interesse} (últimos {periodo_interesse}):")
    st.write(precos.head())

    st.write(f"\nSimulação de Preços Futuros para {ticker_interesse} (dias à frente: {analisador.dias_a_frente}):")
    df_simulacao = pd.DataFrame(caminhos_precos.T, columns=[f'Dia {i+1}' for i in range(analisador.dias_a_frente)])
    st.write(df_simulacao.head())

    st.write(f"\nProbabilidade de Retorno ser maior ou igual a {analisador.retorno_esperado*100}%: {prob_retorno*100:.2f}%")

    st.write(f"\nÚltimas Notícias para {ticker_interesse} (Limitadas às últimas 10):")
    noticias = analisador.obter_noticias(ticker_interesse)
    if noticias:
        # Criar lista para exibir notícias
        for i, noticia in enumerate(noticias[:10]):
            st.write(f"\nNotícia {i + 1}")
            st.write(f"Título: {noticia['title']}")
            
            # Tornar o link clicável usando st.markdown
            st.markdown(f"Link: [{noticia['link']}]({noticia['link']})")
            
            st.write(f"Data: {noticia['date']}")
    else:
        st.write("Nenhuma notícia encontrada para o ticker fornecido.")

    # Plotar gráficos
    analisador.plotar_graficos(precos, caminhos_precos)
