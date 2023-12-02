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

# Breve descrição sobre o projeto
st.write("## Bem-vindo ao Start Investor")
st.write("###### Faça a sua consulta para otimizar seu tempo e aprimorar seu processo de análise.")

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
        retornos_log = np.log(1 + historico_ativo.pct_change())
        media_retornos = retornos_log.mean()
        variancia_retornos = retornos_log.var()
        drift = media_retornos - (0.5 * variancia_retornos)
        desvio_padrao = retornos_log.std()

        retornos_diarios = np.exp(drift + desvio_padrao * norm.ppf(np.random.rand(dias_a_frente, dias_a_frente)))

        caminhos_precos = np.zeros((dias_a_frente, dias_a_frente))
        caminhos_precos[0] = historico_ativo.iloc[-1]

        for t in range(1, dias_a_frente):
            caminhos_precos[t] = caminhos_precos[t - 1] * retornos_diarios[t]

        return caminhos_precos

    @staticmethod
    def calcular_retorno_probabilidade(caminhos_precos, retorno_esperado):
        previsto = caminhos_precos[-1]
        lista_prevista = list(previsto)
        atual = caminhos_precos[0, 0]
        maiores_ou_iguais = [i / atual for i in lista_prevista if 1 - (i / atual) >= retorno_esperado]
        probabilidade = len(maiores_ou_iguais) / len(lista_prevista)
        return probabilidade * 100

    def probabilidade_retorno(self):
        historico_ativo = self.obter_precos(self.ticker, self.periodo_anterior)
        caminhos_precos = self.simular_precos(historico_ativo, self.dias_a_frente, self.retorno_esperado)
        return self.calcular_retorno_probabilidade(caminhos_precos, self.retorno_esperado)


class AnalisadorDadosMercado(Ativo):
    def __init__(self, days_ahead=30, return_expected=0.02):
        super().__init__('')  # Inicializa a classe Ativo com um ticker fictício
        self.dias_a_frente = days_ahead
        self.retorno_esperado = return_expected

    def obter_preco(self, ticker, periodo='2mo'):
        ticker = ticker.upper()
        if not ticker.endswith('.SA'):
            ticker += '.SA'

        ativo = yf.Ticker(ticker)
        precos = ativo.history(period=periodo)
        return precos['Close']

    def obter_noticias(self, ticker, num_noticias=10):
        googlenews = GoogleNews(lang='ptbr', region='BR', period='7d')
        googlenews.get_news(ticker)
        results = googlenews.results()
        return results[:num_noticias]

    def baixar_dados(self, ticker, periodo='2mo'):
        precos = self.obter_preco(ticker, periodo)
        noticias = self.obter_noticias(ticker)
        return precos, noticias

    def simular_precos(self, historico_ativo):
        retornos_log = np.log(1 + historico_ativo.pct_change())
        mu = retornos_log.mean()
        var = retornos_log.var()
        drift = mu - (0.5 * var)
        stdev = retornos_log.std()

        daily_returns = np.exp(drift + stdev * norm.ppf(np.random.rand(self.dias_a_frente, self.dias_a_frente)))

        price_paths = np.zeros((self.dias_a_frente, self.dias_a_frente))
        price_paths[0] = historico_ativo.iloc[-1]

        for t in range(1, self.dias_a_frente):
            price_paths[t] = price_paths[t - 1] * daily_returns[t]

        return price_paths

    def calcular_retorno_probabilidade(self, price_paths):
        actual = price_paths[0, 0]
        over = (price_paths[-1] / actual) >= (1 + self.retorno_esperado)
        prob = np.mean(over)
        return prob


# Exemplo de uso com Streamlit
st.sidebar.markdown("# Start Investor 📈")  # Adiciona título à barra lateral

# Adiciona os inputs na barra lateral
nome_empresa = st.sidebar.text_input("Insira o nome da empresa (ex: Apple):").title()
periodo_interesse = st.sidebar.text_input("Insira o período desejado para o histórico de preços (ex: 3mo):")

# Adiciona exemplo de nome de empresa e período para orientar o usuário
st.sidebar.write("Exemplo de nome de empresa: Apple Inc.")
st.sidebar.write("Exemplo de período: 3mo")

# Converte o nome da empresa em um ticker usando yfinance
ticker_interesse = None
if st.sidebar.button("Analisar"):
    try:
        # Obtém o ticker correspondente ao nome da empresa
        ticker_info = yf.Ticker(nome_empresa).info
        if not ticker_info:
            raise ValueError("Ticker não encontrado para a empresa especificada.")
        ticker_interesse = ticker_info['symbol']
    except ValueError as e:
        st.sidebar.error(str(e))
        st.stop()

    # Restante do código permanece inalterado
    analisador = AnalisadorDadosMercado()
    precos, noticias = analisador.baixar_dados(ticker_interesse, periodo_interesse)
    caminhos_precos = analisador.simular_precos(precos)
    prob_retorno = analisador.calcular_retorno_probabilidade(caminhos_precos)

    # Restante do código permanece inalterado
    df_precos = pd.DataFrame({'Data': precos.index, 'Preço de Fechamento': precos.values})
    chart_precos = alt.Chart(df_precos).mark_line().encode(
        x='Data:T',
        y='Preço de Fechamento:Q'
    ).properties(
        width=600,
        height=400,
        title=f'Histórico de Preços para {ticker_interesse}'
    )
    st.altair_chart(chart_precos)

    st.sidebar.markdown(f"\nProbabilidade de Retorno ser maior ou igual a {analisador.retorno_esperado*100}%: {prob_retorno*100:.2f}%, segundo o Movimento Browniano Geométrico.")

    st.markdown(f"\nÚltimas Notícias para {ticker_interesse}")
    if noticias:
        for noticia in noticias:
            link_parts = noticia['link'].split('/~/+/')
            link = link_parts[1] if len(link_parts) > 1 else noticia['link']
            st.markdown(f"- [{noticia['title']}]({link})", unsafe_allow_html=True)
