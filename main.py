import streamlit as st
import yfinance as yf
import pandas as pd

@st.cache_data
def carregar_dados(empresas):
    texto_tickers = " ".join(empresas)
    dados_acao = yf.Tickers(texto_tickers)
    cotacoes_acao = dados_acao.history(period="10y", end = "2025-07-01")
    cotacoes_acao = cotacoes_acao["Close"]
    return cotacoes_acao

acoes = ['ITUB4.SA', 'PETR4.SA', 'MGLU3.SA', 'VALE3.SA','ABEV3.SA', 'GGBR4.SA']
dados = carregar_dados(acoes)

st.write("""
# App Preços das Ações
Este aplicativo permite que você visualize os preços das ações de uma empresa específica.
""")

lista_acoes = st.multiselect("Escolha as ações para visualizar", dados.columns)
print(lista_acoes)

if lista_acoes:
    dados = dados[lista_acoes]
    if len(lista_acoes) == 1:
        acao_unica = lista_acoes[0]
        dados = dados.rename(columns={acao_unica: "Close"})       
st.line_chart(dados)