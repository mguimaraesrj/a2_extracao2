## Melhorias -  Projeto 9
- Adicionamos um input que permite ao usuário selecionar a porcentagem utilizada como referência para o cálculo do Movimento Browniano Geométrico. Dessa forma, o usuário consegue saber se a probabilidade retorno será maior ou igual do que a sua própria expectativa. Por exemplo, ele pode escolher se  a referência de retorno será 2%, 10% ou qualquer outra.

- Após a exibição do resultado do cálculo da probabilidade do MBG, adicionar uma explicação sobre o MBG e o seu processo. Ampliando a compreensão do usuário sobre as ferramentas disponibilizadas para a análise. Além disso, também adicionamos uma caixa de informação explicação ao usuário o que é um ticker.

- Aprimoramos a seção de filtro da tabela. Se o usuário não digitar nada no espaço de filtro por nome da empresa (caso ele já saiba o ticker da companhia), a tabela não será mostrada, facilitando a visualização e organização da restante das informações. Caso ele insira um filtro, verá apenas o dataframe filtrado por seu interesse. Além disso, também removemos o espaço de filtrar a tabela por ticker. Não estava fazendo sentido filtrar por ticker já que o objetivo é exatamente descobrir o ticker.


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
