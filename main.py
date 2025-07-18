import streamlit as st
import yfinance as yf
import pandas as pd

@st.cache_data
def carregar_dados(empresa):
    dados_acao = yf.Ticker(empresa)
    cotacoes_acao = dados_acao.history(start = "2010-01-01" , end = "2025-06-01")
    cotacoes_acao = cotacoes_acao[['Close']]
    return cotacoes_acao

dados = carregar_dados('BBAS3.SA')
print(dados)

st.write("""
# App Preços das Ações
Este aplicativo permite que você visualize os preços das ações de uma empresa específica.
""")

st.line_chart(dados)