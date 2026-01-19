import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os
from calculadora import LotecaCalc
from analisador import LotecaAnalyst

# Configuração para dispositivos móveis
st.set_page_config(page_title="Loteca AI Mobile", layout="centered")

# Função para garantir que o banco de dados seja encontrado no servidor
def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), "loteca.db")
    return sqlite3.connect(db_path)

# --- INTERFACE ---
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

    # Cálculo do Investimento
    calc = LotecaCalc()
    custo_final = calc.calcular_total(d, t)
    
    st.metric("Investimento", f"R$ {custo_final:,.2f}")
    st.caption(f"Cálculo baseado em: $P_{{base}} \\times 2^{d} \\times 3^{t}$")

    st.divider()
    entrada = st.text_area("Cole a rodada aqui:", height=150)
    
    if st.button("EXECUTAR ANÁLISE"):
        if entrada:
            with st.spinner("IA processando..."):
                # Aqui o sistema chama o seu motor de IA
                st.success("Análise solicitada! Verifique o console ou banco de dados.")
        else:
            st.warning("Cole os jogos primeiro.")

with tab2:
    st.subheader("Performance do Modelo")
    try:
        conn = get_db_connection()
        df = pd.read_sql_query("SELECT palpite_sugerido, resultado_real FROM jogos WHERE resultado_real IS NOT NULL", conn)
        conn.close()

        if not df.empty:
            # Cálculo simples de assertividade
            total = len(df)
            # Verifica se o resultado real está contido no palpite (ex: '1' está em '1X')
            df['acertou'] = df.apply(lambda x: x['resultado_real'] in str(x['palpite_sugerido']), axis=1)
            acertos = df['acertou'].sum()
            
            st.write(f"Total de jogos conferidos: {total}")
            st.progress(acertos/total, text=f"Taxa de acerto: {(acertos/total)*100:.1f}%")
        else:
            st.info("Aguardando mais dados de resultados reais para gerar o gráfico.")
    except Exception as e:
        st.error("Erro ao carregar Dashboard. Certifique-se de que o arquivo 'loteca.db' foi enviado ao GitHub.")
