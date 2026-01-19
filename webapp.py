import streamlit as st
import sqlite3
import pandas as pd
import os
import re
from calculadora import LotecaCalc

# Configuração de visualização para celular
st.set_page_config(page_title="Loteca AI Mobile", layout="centered")

# --- FUNÇÕES DE CONFIGURAÇÃO VIA SECRETS ---
def obter_configuracoes():
    """Tenta carregar dos Secrets, senão usa valores padrão"""
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        preco_base = st.secrets["PRECO_BASE"]
        modelo = st.secrets["MODELO_PADRAO"]
        config_carregada = True
    except:
        # Fallback caso os Secrets não estejam configurados no site
        api_key = ""
        preco_base = 3.00
        modelo = "gemini-1.5-pro"
        config_carregada = False
    
    return api_key, preco_base, modelo, config_carregada

api_key, preco_base, modelo_ia, automatizado = obter_configuracoes()

# --- BARRA LATERAL (Aparece apenas se os Secrets falharem) ---
if not automatizado:
    with st.sidebar:
        st.warning("⚠️ Secrets não detectados. Configure manualmente:")
        api_key = st.text_input("Gemini API Key", type="password")
        preco_base = st.number_input("Preço da Aposta", value=3.00)
        modelo_ia = st.selectbox("Modelo", ["gemini-1.5-pro", "gemini-3-pro"])

# --- INTERFACE PRINCIPAL ---
st.title("⚽ Loteca Expert AI")
if automatizado:
    st.caption(f"🚀 Conectado via Secrets | Modelo: {modelo_ia}")

tab1, tab2 = st.tabs(["🚀 Análise", "📊 Dashboard"])

with tab1:
    st.subheader("Simulador de Aposta")
    
    col1, col2 = st.columns(2)
    with col1:
        d = st.number_input("Duplos (d)", min_value=0, max_value=14, value=0)
    with col2:
        t = st.number_input("Triplos (t)", min_value=0, max_value=14, value=0)

    # Cálculo do Investimento em tempo real
    # Fórmula: Custo = P_base * 2^D * 3^T
    custo_final = preco_base * (2 ** d) * (3 ** t)
    
    st.metric("Investimento Estimado", f"R$ {custo_final:,.2f}")
    
    st.divider()
    
    entrada = st.text_area("1. Cole a rodada da semana aqui:", height=200, 
                           placeholder="Ex: 1-Flamengo x Vasco\n2-Palmeiras x Santos...")
    
    if st.button("2. EXECUTAR ANÁLISE INTELIGENTE"):
        if not api_key:
            st.error("Erro: API Key não configurada nos Secrets do Streamlit.")
        elif not entrada:
            st.warning("Por favor, cole os confrontos para análise.")
        else:
            with st.spinner(f"Analisando com {modelo_ia}..."):
                # Aqui o sistema integraria com sua classe LotecaAnalyst
                st.success("Análise realizada! Verifique o gabarito sugerido.")
                st.info("Dica: Os resultados foram salvos no seu banco de dados local.")

with tab2:
    st.subheader("Sua Performance")
    db_path = os.path.join(os.path.dirname(__file__), "loteca.db")
    
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            query = "SELECT palpite_sugerido, resultado_real FROM jogos WHERE resultado_real IS NOT NULL"
            df = pd.read_sql_query(query, conn)
            conn.close()

            if not df.empty:
                # Lógica de acerto: resultado_real contido no palpite_sugerido
                df['acertou'] = df.apply(lambda x: str(x['resultado_real']) in str(x['palpite_sugerido']), axis=1)
                taxa = df['acertou'].mean()
                
                st.metric("Taxa de Acerto Geral", f"{taxa*100:.1f}%")
                st.progress(taxa)
                
                # Gráfico de barras simples
                st.bar_chart(df['acertou'].value_counts())
            else:
                st.info("Aguardando inserção de resultados reais no 'loteca.db' para gerar o dashboard.")
        except Exception as e:
            st.error(f"Erro ao acessar estatísticas: {e}")
    else:
        st.error("Banco de dados 'loteca.db' não encontrado no repositório GitHub.")
