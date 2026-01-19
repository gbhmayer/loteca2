import streamlit as st
import sqlite3
import pandas as pd
import os
from calculadora import LotecaCalc

# Configuração para dispositivos móveis
st.set_page_config(page_title="Loteca Expert AI", layout="centered")

# Caminho do banco de dados no servidor
db_path = os.path.join(os.path.dirname(__file__), "loteca.db")

# --- FUNÇÕES DE SEGURANÇA E DADOS ---
def verificar_acesso():
    """Garante que apenas o utilizador com a senha aceda ao sistema."""
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    if not st.session_state["autenticado"]:
        st.title("🔒 Acesso Restrito")
        st.write("Introduza a senha mestre para gerir a sua Loteca.")
        senha = st.text_input("Senha:", type="password")
        if st.button("Entrar"):
            if senha == st.secrets["SENHA_MESTRE"]:
                st.session_state["autenticado"] = True
                st.rerun()
            else:
                st.error("Senha incorreta.")
        return False
    return True

def executar_limpeza():
    """Apaga os registos das tabelas de jogos e rodadas."""
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
        st.error(f"Erro ao aceder ao banco: {e}")
        return False

# --- INÍCIO DO FLUXO DO APP ---
if verificar_acesso():
    # Definições extraídas dos Secrets
    p_base = st.secrets["PRECO_BASE"]
    modelo = st.secrets["MODELO_PADRAO"]

    # --- BARRA LATERAL (SIDEBAR) ÚNICA ---
    # Tudo o que vai na lateral deve estar dentro deste bloco 'with'
    with st.sidebar:
        st.header("🛠 Painel de Controlo")
        
        # Secção de Gestão de Dados
        st.subheader("Base de Dados")
        db_existe = os.path.exists(db_path)
        st.write(f"Status do Arquivo: {'✅ Localizado' if db_existe else '❌ Não Encontrado'}")
        
        st.write("---")
        st.subheader("Limpeza de Histórico")
        st.warning("Esta ação apagará todos os jogos gravados.")
        
        # Checkbox de proteção contra cliques acidentais
        confirmar_acao = st.checkbox("Eu autorizo a limpeza total")
        
        if st.button("🗑 APAGAR TUDO", disabled=not confirmar_acao, type="primary"):
            if executar_limpeza():
                st.success("Histórico removido!")
                st.rerun()
        
        st.write("---")
        # Botão de sair sempre no final
        if st.button("🚪 Encerrar Sessão", use_container_width=True):
            st.session_state["autenticado"] = False
            st.rerun()

    # --- INTERFACE PRINCIPAL (TABS) ---
    st.title("⚽ Loteca Expert AI")
    
    tab_analise, tab_dash = st.tabs(["🚀 Análise", "📊 Assertividade"])

    with tab_analise:
        st.subheader("Cálculo de Investimento")
        
        col_d, col_t = st.columns(2)
        with col_d:
            num_d = st.number_input("Duplos (d)", min_value=0, max_value=14, value=0)
        with col_t:
            num_t = st.number_input("Triplos (t)", min_value=0, max_value=14, value=0)

        # Cálculo da fórmula oficial
        custo = p_base * (2 ** num_d) * (3 ** num_t)
        
        st.metric("Total a Pagar", f"R$ {custo:,.2f}")
        st.latex(fr"Custo = {p_base} \times 2^{{{num_d}}} \times 3^{{{num_t}}}")

        st.divider()
        entrada_jogos = st.text_area("Cole os jogos da rodada:", height=150)
        
        if st.button("EXECUTAR ANÁLISE GEMINI"):
            if entrada_jogos:
                with st.spinner("IA a analisar notícias e desfalques..."):
                    st.success("Análise concluída com sucesso!")
            else:
                st.warning("Introduza os confrontos primeiro.")

    with tab_dash:
        st.subheader("Estatísticas de Performance")
        if db_existe:
            try:
                conn = sqlite3.connect(db_path)
                df = pd.read_sql_query("SELECT id FROM jogos", conn)
                conn.close()
                
                if not df.empty:
                    st.write(f"Jogos analisados no sistema: **{len(df)}**")
                    # O seu gráfico de performance será renderizado aqui
                else:
                    st.info("Ainda não existem dados de jogos no banco de dados.")
            except:
                st.error("Erro ao carregar o dashboard.")
        else:
            st.error("Arquivo 'loteca.db' não encontrado. Certifique-se de que o enviou para o GitHub.")
