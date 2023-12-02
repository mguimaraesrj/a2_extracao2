## Descrição do Código
Importações
O código inicia importando bibliotecas necessárias para a execução do projeto. As principais bibliotecas utilizadas são yfinance para obter dados financeiros, pandas para manipulação de dados, numpy para operações numéricas, scipy.stats para estatísticas, statsmodels.tsa.holtwinters para modelagem de séries temporais, dataclasses para criação de classes de dados, altair para visualização de dados, streamlit para a criação de aplicativos web interativos, e GoogleNews para obter notícias do Google.

## Breve Descrição sobre o Projeto
O código começa apresentando uma breve descrição do projeto usando o streamlit para criar uma interface interativa. Ele oferece aos usuários a capacidade de consultar informações relacionadas a uma empresa específica por meio do ticker.

## Tabela de Dados
Uma tabela de dados inicial é criada com um único exemplo de ativo (Magazine Luiza - MGLU3). Uma barra lateral é adicionada para permitir que o usuário filtre os dados com base no nome da empresa e no ticker.

## Simulação de Preços de Ativos
A classe Ativo é definida como uma dataclass que contém métodos estáticos para obter preços históricos, simular preços futuros e calcular a probabilidade de retorno com base em uma distribuição normal.

## Analisador de Dados de Mercado
A classe AnalisadorDadosMercado herda da classe Ativo e adiciona métodos específicos para obter preços históricos, notícias e dados financeiros de uma empresa.

## Exemplo de Uso com Streamlit
A última parte do código mostra um exemplo de uso do streamlit para criar uma interface interativa. Ele permite que o usuário insira o ticker de interesse, escolha o período do histórico de preços e o número de dias, meses ou anos. A classe AnalisadorDadosMercado é então usada para baixar dados, simular preços futuros e calcular a probabilidade de retorno. O resultado é exibido na interface, incluindo um gráfico de histórico de preços, uma tabela de dados, e as últimas notícias relacionadas ao ativo.
