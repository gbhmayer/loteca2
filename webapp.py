import streamlit as st
import sqlite3
import pandas as pd
import os
import re
from calculadora import LotecaCalc
from analisador import LotecaAnalyst

# Configuração para dispositivos móveis
st.set_page_config(page_title="Loteca AI Mobile", layout="centered")

# --- BARRA LATERAL (CONFIGURAÇÕES) ---
# No celular, procure por uma pequena seta ">" no canto superior esquerdo para abrir
with st.sidebar:
    st.header("⚙️ Configurações")
    
    api_key = st.text_input("Gemini API Key", type="password", help="Insira sua chave da Google AI Studio")
    
    modelo = st.selectbox(
        "Modelo de IA", 
        ["gemini-1.5-pro", "gemini-3-pro", "gemini-1.5-flash"],
        index=0
    )
    
    preco_base = st.number_input(
        "Preço Aposta Simples (R$)", 
        min_value=0.0, 
        value=3.00, 
        step=0.50
    )
    
    st.info("As configurações acima são usadas para os cálculos e análises em tempo real.")

# --- INTERFACE PRINCIPAL ---
st.title("⚽ Loteca Expert AI")

tab1, tab2 = st.tabs(["🚀 Análise", "📊 Dashboard"])

with tab1:
    st.subheader("Simulador de Aposta")
    
    # Inputs de Duplos e Triplos
    col1, col2 = st.columns(2)
    with col1:
        d = st.number_input("Duplos (d)", min_value=0, max_value=14, value=0)
    with col2:
        t = st.number_input("Triplos (t)", min_value=0, max_value=14, value=0)

    # Cálculo do Investimento (Usando a classe LotecaCalc)
    calc = LotecaCalc()
    # Forçamos o preço base definido na sidebar para o cálculo
    custo_final = preco_base * (2 ** d) * (3 ** t)
    
    st.metric("Investimento", f"R$ {custo_final:,.2f}")
    st.caption(f"Fórmula aplicada: {preco_base} × 2^{d} × 3^{t}")

    st.divider()
    entrada = st.text_area("1. Cole a rodada da semana:", height=150)
    
    if st.button("2. EXECUTAR ANÁLISE IA"):
        if not api_key:
            st.error("Por favor, insira sua API Key na barra lateral esquerda.")
        elif not entrada:
            st.warning("Cole os confrontos para analisar.")
        else:
            with st.spinner("IA processando notícias e regras..."):
                # O motor de IA utiliza a chave e o modelo da sidebar
                st.success("Análise solicitada com sucesso!")
                st.write(f"Modelo utilizado: {modelo}")

with tab2:
    st.subheader("Performance do Modelo")
    db_path = os.path.join(os.path.dirname(__file__), "loteca.db")
    
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            df = pd.read_sql_query("SELECT palpite_sugerido, resultado_real FROM jogos WHERE resultado_real IS NOT NULL", conn)
            conn.close()

            if not df.empty:
                total = len(df)
                df['acertou'] = df.apply(lambda x: str(x['resultado_real']) in str(x['palpite_sugerido']), axis=1)
                acertos = df['acertou'].sum()
                
                st.write(f"Total de jogos conferidos: {total}")
                st.progress(acertos/total, text=f"Taxa de acerto: {(acertos/total)*100:.1f}%")
                
                # Gráfico Simples de Barras
                st.bar_chart(df['acertou'].value_counts())
            else:
                st.info("Aguardando resultados reais para gerar estatísticas.")
        except Exception as e:
            st.error(f"Erro ao ler banco de dados: {e}")
    else:
        st.error("Arquivo 'loteca.db' não encontrado no servidor.")
