# importar as bibliotecas necessárias
import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import timedelta

# Função para carregar os dados das ações usando yfinance
@st.cache_data
def carregar_dados(empresas):
    # Baixa os preços de fechamento das ações do Yahoo Finance
    cotacoes_acao = yf.download(empresas, start="2015-01-01", end="2025-07-01")["Close"]
    return cotacoes_acao

# Função para carregar os tickers das ações do arquivo IBOV.csv
@st.cache_data
def carregar_tickers_acoes():
    # Lê o arquivo CSV com os códigos das ações
    base_tickers = pd.read_csv("IBOV.csv", sep=";")
    # Cria a lista de tickers no padrão da B3 para o Yahoo Finance
    tickers = list(base_tickers["Código"])
    tickers = [item + ".SA" for item in tickers]
    return tickers

# Carrega a lista de tickers
acoes = carregar_tickers_acoes()
# Carrega os dados das ações
dados = carregar_dados(acoes)

# Remove linhas do DataFrame onde o índice (data) é nulo
dados = dados[~dados.index.isnull()]

# Título e descrição do app
st.write("""
# App Preço de Ações
O gráfico abaixo representa a evolução do preço das ações ao longo dos anos
""") # markdown

# Cria a barra lateral de filtros
st.sidebar.header("Filtros")

# Filtro para seleção de ações
primeira_acao = dados.columns[0] if len(dados.columns) > 0 else None
lista_acoes = st.sidebar.multiselect(
    "Escolha as ações para visualizar",
    dados.columns,
    default=[primeira_acao] if primeira_acao else [] # Mostra só a primeira ação inicialmente
)
if lista_acoes:
    # Filtra o DataFrame para mostrar apenas as ações selecionadas
    dados = dados[lista_acoes]
    if len(lista_acoes) == 1:
        # Renomeia a coluna para "Close" se apenas uma ação for selecionada
        acao_unica = lista_acoes[0]
        dados = dados.rename(columns={acao_unica: "Close"})
        
# Filtro para seleção do período de datas
data_inicial = dados.index.min().to_pydatetime() # Data mínima disponível
data_final = dados.index.max().to_pydatetime()   # Data máxima disponível
intervalo_data = st.sidebar.slider(
    "Selecione o período", 
    min_value=data_inicial, 
    max_value=data_final,
    value=(data_inicial, data_final),
    step=timedelta(days=1)
)

# Filtra os dados pelo intervalo de datas selecionado
dados = dados.loc[intervalo_data[0]:intervalo_data[1]]

# Exibe o gráfico de linha com os dados filtrados
st.line_chart(dados)

# Inicializa o texto de performance dos ativos
texto_performance_ativos = ""

# Garante que lista_acoes sempre tenha as ações selecionadas
if len(lista_acoes)==0:
    lista_acoes = list(dados.columns)
elif len(lista_acoes)==1:
    dados = dados.rename(columns={"Close": acao_unica})

# Simula uma carteira com R$1000 em cada ativo selecionado
carteira = [1000 for acao in lista_acoes]
total_inicial_carteira = sum(carteira)

# Calcula a performance de cada ativo no período selecionado
for i, acao in enumerate(lista_acoes):
    performance_ativo = dados[acao].iloc[-1] / dados[acao].iloc[0] - 1
    performance_ativo = float(performance_ativo)

    # Atualiza o valor da carteira para cada ativo
    carteira[i] = carteira[i] * (1 + performance_ativo)

    # Monta o texto colorido de performance para cada ativo
    if performance_ativo > 0:
        texto_performance_ativos = texto_performance_ativos + f"  \n{acao}: :green[{performance_ativo:.1%}]"
    elif performance_ativo < 0:
        texto_performance_ativos = texto_performance_ativos + f"  \n{acao}: :red[{performance_ativo:.1%}]"
    else:
        texto_performance_ativos = texto_performance_ativos + f"  \n{acao}: {performance_ativo:.1%}"

# Calcula a performance total da carteira
total_final_carteira = sum(carteira)
performance_carteira = total_final_carteira / total_inicial_carteira - 1

# Monta o texto colorido de performance da carteira
if performance_carteira > 0:
    texto_performance_carteira = f"Performance da carteira com todos os ativos: :green[{performance_carteira:.1%}]"
elif performance_carteira < 0:
    texto_performance_carteira = f"Performance da carteira com todos os ativos: :red[{performance_carteira:.1%}]"
else:
    texto_performance_carteira = f"Performance da carteira com todos os ativos: {performance_carteira:.1%}"

# Exibe o texto de performance dos ativos e da carteira
st.write(f"""
### Performance dos Ativos
Essa foi a perfomance de cada ativo no período selecionado:

{texto_performance_ativos}

{texto_performance_carteira}
""")