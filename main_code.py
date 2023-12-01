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

    def plotar_graficos(self, precos, caminhos_precos):
        # Gráfico do Histórico de Preços
        df_precos = pd.DataFrame({'Data': precos.index, 'Preço de Fechamento': precos.values})
        chart_precos = alt.Chart(df_precos).mark_line().encode(
            x='Data:T',
            y='Preço de Fechamento:Q'
        ).properties(
            width=600,
            height=400,
            title=f'Histórico de Preços para {self.ticker}'
        )

        # Gráfico da Simulação de Preços Futuros
        df_simulacao = pd.DataFrame(caminhos_precos.T, columns=[f'Dia {i + 1}' for i in range(self.dias_a_frente)])
        df_simulacao['Data'] = precos.index[-1] + pd.to_timedelta(df_simulacao.index, unit='D')
        df_simulacao = pd.melt(df_simulacao, id_vars=['Data'], var_name='Dia', value_name='Preço de Fechamento Simulado')
        chart_simulacao = alt.Chart(df_simulacao).mark_line(opacity=0.1, color='blue').encode(
            x='Data:T',
            y='Preço de Fechamento Simulado:Q',
            detail='Dia:N'
        ).properties(
            width=600,
            height=400,
            title=f'Simulação de Preços Futuros para {self.ticker}'
        )

        # Gráfico da Distribuição dos Retornos Simulados
        retornos_simulados = (caminhos_precos[-1] / caminhos_precos[0, 0]) - 1
        df_retornos_simulados = pd.DataFrame({'Retorno Simulado': retornos_simulados})
        chart_retornos_simulados = alt.Chart(df_retornos_simulados).mark_bar(
            color='green',
            opacity=0.7
        ).encode(
            alt.X('Retorno Simulado:Q', bin=alt.Bin(maxbins=30)),
            alt.Y('count():Q')
        ).properties(
            width=600,
            height=400,
            title='Distribuição dos Retornos Simulados'
        )

        # Exibir os gráficos
        st.altair_chart(chart_precos)
        st.altair_chart(chart_simulacao)
        st.altair_chart(chart_retornos_simulados)


# Exemplo de uso com Streamlit
st.title("Analisador de Ações")

ticker_interesse = st.text_input("Insira o ticker de interesse (ex: MGLU3):").upper()

periodo_opcoes = ["1 mo", "2 mo", "3 mo", "6 mo", "1y", "2y", "3y", "10y", "15y"]
periodo_interesse = st.radio("Escolha o período desejado:", periodo_opcoes + ["Outro"])

# Campo de entrada manual (exibido/oculto por botão)
if periodo_interesse == "Outro":
    periodo_interesse = st.text_input("Insira manualmente o período desejado (ex: 3mo):")
else:
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

# Adicionando a opção "Outro" na barra lateral
periodo_interesse = st.sidebar.radio("Escolha o período desejado:", periodo_opcoes + ["Outro"])

# Campo de entrada manual (exibido/oculto por botão)
if periodo_interesse == "Outro":
    periodo_interesse = st.sidebar.text_input("Insira manualmente o período desejado (ex: 3mo):")

if st.button("Analisar"):
    # Restante do código...

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
