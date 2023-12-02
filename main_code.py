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
st.sidebar.title("Start Investor")  # Adiciona título à barra lateral

# Adiciona os inputs na barra lateral
ticker_interesse = st.sidebar.text_input("Insira o ticker de interesse (ex: MGLU3):").upper()
periodo_interesse = st.sidebar.text_input("Insira o período desejado para o histórico de preços (ex: 3mo):")

if st.sidebar.button("Analisar"):
    # Criar instância do AnalisadorDadosMercado
    analisador = AnalisadorDadosMercado()

    # Obter dados
    precos, noticias = analisador.baixar_dados(ticker_interesse, periodo_interesse)

    # Simular preços futuros e calcular probabilidade de retorno
    caminhos_precos = analisador.simular_precos(precos)
    prob_retorno = analisador.calcular_retorno_probabilidade(caminhos_precos)

# Plotar gráfico de histórico de preços
st.write(f"\nHistórico de Preços para {ticker_interesse} (últimos {periodo_interesse}):")

try:
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

    # Botão para exibir as últimas notícias
    if st.button("Ver Últimas Notícias"):
        # Obter notícias
        noticias = analisador.obter_noticias(ticker_interesse)

        # Exibir notícias
        st.write(f"\nÚltimas Notícias para {ticker_interesse}")
        if noticias:
            # Criar lista para exibir notícias
            for i, noticia in enumerate(noticias[:10]):
                st.write(f"\nNotícia {i + 1}")
                st.write(f"Título: {noticia['title']}")
                
                # Tornar o link clicável usando st.markdown
                st.markdown(f"Link: [{noticia['link']}]({noticia['link']})")
                
                st.write(f"Data: {noticia['date']}")
except Exception as e:
    st.error(f"Erro ao processar dados: {str(e)}")
