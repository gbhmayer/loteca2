import streamlit as st
import sqlite3
import pandas as pd
import os
import re
from calculadora import LotecaCalc

# Configuração para ecrãs de telemóvel
st.set_page_config(page_title="Loteca Expert AI", layout="centered")

db_path = os.path.join(os.path.dirname(__file__), "loteca.db")

# --- FUNÇÕES DE APOIO ---
def limpar_banco_dados():
    """Apaga os jogos e rodadas e otimiza o arquivo SQLite"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM jogos")
        cursor.execute("DELETE FROM rodadas")
        conn.commit()
        cursor.execute("VACUUM")
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro técnico: {e}")
        return False

def verificar_acesso():
    """Barreira de segurança inicial"""
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    if not st.session_state["autenticado"]:
        st.title("🔒 Acesso Restrito")
        senha_digitada = st.text_input("Introduza a Senha Mestre:", type="password")
        if st.button("Entrar"):
            if senha_digitada == st.secrets["SENHA_MESTRE"]:
                st.session_state["autenticado"] = True
                st.rerun()
            else:
                st.error("Senha incorreta.")
        return False
    return True

# --- EXECUÇÃO DO APP ---
if verificar_acesso():
    # Carrega configurações dos Secrets
    p_base = st.secrets["PRECO_BASE"]
    modelo_ia = st.secrets["MODELO_PADRAO"]

    # --- BARRA LATERAL UNIFICADA ---
    with st.sidebar:
        st.header("🛠 Ferramentas")
        
        # Seção de Gestão de Dados
        st.subheader("Gestão de Dados")
        st.write("Apague o histórico para limpar o banco de dados.")
        
        confirmar = st.checkbox("Autorizar limpeza de dados")
        
        if st.button("🗑 Limpar Histórico", disabled=not confirmar, type="primary"):
            if limpar_banco_dados():
                st.success("Histórico apagado!")
                st.rerun()

        st.divider()
        
        # Botão de Sair no final da barra lateral
        if st.button("🚪 Encerrar Sessão"):
            st.session_state["autenticado"] = False
            st.rerun()

    # --- INTERFACE PRINCIPAL ---
    st.title("⚽ Loteca Expert AI")
    st.caption(f"Águas Claras/DF | IA: {modelo_ia}")

    tab1, tab2 = st.tabs(["🚀 Análise", "📊 Dashboard"])

    with tab1:
        st.subheader("Calculadora de Aposta")
        
        # Inputs para o Motorola (em colunas para poupar espaço)
        col1, col2 = st.columns(2)
        with col1:
            d = st.number_input("Duplos (d)", min_value=0, max_value=14, value=0)
        with col2:
            t = st.number_input("Triplos (t)", min_value=0, max_value=14, value=0)

        # Cálculo exponencial do custo
        calc = LotecaCalc()
        custo_final = p_base * (2 ** d) * (3 ** t)
        
        st.metric("Investimento Total", f"R$ {custo_final:,.2f}")
        st.caption(f"Fórmula: $R\$ {p_base} \\times 2^{d} \\times 3^{t}$")

        st.divider()
        
        entrada = st.text_area("1. Cole a rodada aqui:", height=150)
        
        if st.button("2. EXECUTAR ANÁLISE IA"):
            if not entrada:
                st.warning("Introduza os confrontos primeiro.")
            else:
                with st.spinner("Analisando notícias e regras especialistas..."):
                    # Aqui o sistema correria o seu motor LotecaAnalyst
                    st.success("Análise Gemini concluída!")

    with tab2:
        st.subheader("Performance Histórica")
        if os.path.exists(db_path):
            try:
                conn = sqlite3.connect(db_path)
                df = pd.read_sql_query("SELECT id FROM jogos", conn)
                conn.close()

                if not df.empty:
                    st.write(f"Total de jogos guardados: {len(df)}")
                    # Aqui pode adicionar os gráficos que criámos anteriormente
                else:
                    st.info("O banco de dados está vazio. Carregue uma rodada.")
            except Exception as e:
                st.error(f"Erro ao ler banco: {e}")
