import streamlit as st
import sqlite3
import pandas as pd
import os
from calculadora import LotecaCalc

# Configuração Mobile
st.set_page_config(page_title="Loteca Expert AI", layout="centered")

db_path = os.path.join(os.path.dirname(__file__), "loteca.db")

# --- FUNÇÕES DE BANCO DE DADOS ---
def limpar_historico_total():
    """Remove todos os jogos e rodadas e otimiza o espaço do arquivo."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM jogos")
        cursor.execute("DELETE FROM rodadas")
        conn.commit()
        cursor.execute("VACUUM") # Compacta o banco de dados
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro ao limpar: {e}")
        return False

# --- SISTEMA DE ACESSO ---
def verificar_acesso():
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    if not st.session_state["autenticado"]:
        st.title("🔒 Acesso Restrito")
        senha_digitada = st.text_input("Senha Mestre:", type="password")
        if st.button("Entrar"):
            if senha_digitada == st.secrets["SENHA_MESTRE"]:
                st.session_state["autenticado"] = True
                st.rerun()
            else:
                st.error("Acesso Negado.")
        return False
    return True

# --- INÍCIO DO APP ---
if verificar_acesso():
    # Parâmetros dos Secrets
    p_base = st.secrets["PRECO_BASE"]

    # --- BARRA LATERAL: GESTÃO ---
    with st.sidebar:
        st.header("🛠 Gestão de Dados")
        st.write("Cuidado: Estas ações são permanentes.")
        
        confirmar_limpeza = st.checkbox("Ativar botão de limpeza")
        
        if st.button("🗑 Limpar Tudo", disabled=not confirmar_limpeza, type="primary"):
            if limpar_historico_total():
                st.toast("Banco de dados resetado!", icon="🧹")
                st.rerun()

        st.divider()
        if st.button("🚪 Sair"):
            st.session_state["autenticado"] = False
            st.rerun()

    st.title("⚽ Loteca Expert AI")

    tab1, tab2 = st.tabs(["🚀 Análise", "📊 Dashboard"])

    with tab1:
        st.subheader("Calculadora de Investimento")
        col1, col2 = st.columns(2)
        with col1:
            d = st.number_input("Duplos (d)", min_value=0, value=0)
        with col2:
            t = st.number_input("Triplos (t)", min_value=0, value=0)

        custo_final = p_base * (2 ** d) * (3 ** t)
        st.metric("Custo Total", f"R$ {custo_final:,.2f}")

        st.divider()
        entrada = st.text_area("Cole a rodada aqui:", height=150)
        if st.button("EXECUTAR ANÁLISE"):
            with st.spinner("IA processando..."):
                st.success("Análise realizada!")

    with tab2:
        st.subheader("Dashboard")
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            df = pd.read_sql_query("SELECT id FROM jogos", conn)
            conn.close()
            
            if not df.empty:
                st.write(f"Total de jogos no banco: {len(df)}")
                # Aqui entraria o gráfico de barras que criamos anteriormente
            else:
                st.info("O histórico está vazio. Carregue uma nova rodada.")
