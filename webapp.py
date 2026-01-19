import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import re
from datetime import datetime
from analisador import LotecaAnalyst
from calculadora import LotecaCalc

# Configuração da Página para Mobile
st.set_page_config(page_title="Loteca AI Mobile", layout="centered")

def carregar_dados_dashboard():
    conn = sqlite3.connect("loteca.db")
    # Busca estatísticas de acertos por categoria na análise
    query = "SELECT analise_detalhada, palpite_sugerido, resultado_real FROM jogos WHERE resultado_real IS NOT NULL"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# --- INTERFACE SIDEBAR (Configurações) ---
with st.sidebar:
    st.header("⚙️ Configurações")
    api_key = st.text_input("Gemini API Key", type="password")
    modelo = st.selectbox("Modelo", ["gemini-1.5-pro", "gemini-3-pro", "gemini-1.5-flash"])
    preco_base = st.number_input("Preço da Aposta (R$)", value=3.00)

# --- ABA PRINCIPAL: ANÁLISE ---
st.title("⚽ Loteca Expert AI")

tab1, tab2 = st.tabs(["🚀 Nova Análise", "📊 Dashboard"])

with tab1:
    st.subheader("Entrada da Rodada")
    entrada_texto = st.text_area("Cole os confrontos aqui:", height=150, placeholder="Ex: Flamengo x Vasco")
    
    col1, col2 = st.columns(2)
    with col1:
        duplos = st.number_input("Duplos (d)", min_value=0, value=0)
    with col2:
        triplos = st.number_input("Triplos (t)", min_value=0, value=0)

    # Cálculo em Tempo Real
    calc = LotecaCalc()
    custo = calc.calcular_total(duplos, triplos)
    st.metric("Investimento Estimado", f"R$ {custo:,.2f}")

    if st.button("⚡ EXECUTAR ANÁLISE IA"):
        if not api_key or not entrada_texto:
            st.error("Por favor, configure a API Key e cole os jogos.")
        else:
            with st.spinner("IA processando notícias e regras especialistas..."):
                # Simulação da chamada do motor de IA
                analista = LotecaAnalyst()
                st.success("Análise finalizada!")
                st.info("Consulte o relatório detalhado abaixo ou no seu histórico.")

# --- ABA DASHBOARD: ASSERTIVIDADE ---
with tab2:
    st.subheader("Performance das Regras")
    df_stats = carregar_dados_dashboard()
    
    if df_stats.empty:
        st.warning("Aguardando resultados reais para gerar estatísticas.")
    else:
        # Lógica de processamento das regras (Exemplo: Riqueza e Rivalidade)
        acertos_riqueza = df_stats[df_stats['analise_detalhada'].str.contains('Riqueza', case=False)].shape[0]
        acertos_total = df_stats.shape[0]
        
        # Gráfico Simples
        chart_data = pd.DataFrame({
            'Regra': ['Riqueza', 'Rivalidade', 'Crise', 'Mando'],
            'Acertos (%)': [85, 72, 60, 55] # Valores de exemplo
        })
        st.bar_chart(chart_data.set_index('Regra'))
        st.write(f"Total de jogos analisados no banco: {acertos_total}")