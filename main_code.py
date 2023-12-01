# ... (código anterior)

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

    # Exibindo resultados e plotando gráficos
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

    # Plotar gráfico de histórico de preços
    st.write(f"\nHistórico de Preços para {ticker_interesse} (últimos {periodo_interesse}):")
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
