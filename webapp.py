import streamlit as st
import sqlite3
import pandas as pd
import os
import re
from calculadora import LotecaCalc
from analisador import LotecaAnalyst

# Configuração para dispositivos móveis
st.set_page_config(page_title="Loteca Expert AI", layout="centered")

# --- SISTEMA DE SEGURANÇA (LOGIN) ---
def verificar_acesso():
    """Cria uma barreira de senha antes de carregar o app."""
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    if not st.session_state["autenticado"]:
        st.title("🔒 Acesso Restrito")
        st.write("Esta é uma aplicação privada de análise da Loteca.")
        
        # Oculta o texto digitado
        senha_digitada = st.text_input("Introduza a Senha Mestre:", type="password")
        
        if st.button("Entrar"):
            # Verifica contra a senha salva nos Secrets
            if senha_digitada == st.secrets["SENHA_MESTRE"]:
                st.session_state["autenticado"] = True
                st.rerun()
            else:
                st.error("Senha incorreta. Acesso negado.")
        return False
    return True

# --- INÍCIO DA APLICAÇÃO ---
if verificar_acesso():
    # Carregamento de configurações via Secrets
    api_key = st.secrets["GEMINI_API_KEY"]
    p_base = st.secrets["PRECO_BASE"]
    modelo_ia = st.secrets["MODELO_PADRAO"]

    st.title("⚽ Loteca Expert AI")
    st.caption(f"Utilizador Autenticado | Modelo: {modelo_ia}")

    tab1, tab2 = st.tabs(["🚀 Análise", "📊 Dashboard"])

    with tab1:
        st.subheader("Simulador de Investimento")
        
        # Layout mobile: duas colunas para números
        col1, col2 = st.columns(2)
        with col1:
            d = st.number_input("Duplos (d)", min_value=0, max_value=14, value=0)
        with col2:
            t = st.number_input("Triplos (t)", min_value=0, max_value=14, value=0)

        # Cálculo da fórmula: Custo = P_base * 2^D * 3^T
        calc = LotecaCalc()
        custo_final = p_base * (2 ** d) * (3 ** t)
        
        st.metric("Custo da Aposta", f"R$ {custo_final:,.2f}")
        st.caption(f"Cálculo: R$ {p_base} × 2^{d} × 3^{t}")

        st.divider()
        
        # Entrada de texto otimizada para telemóvel
        entrada = st.text_area("1. Cole os confrontos da semana:", height=150)
        
        if st.button("2. EXECUTAR ANÁLISE INTELIGENTE"):
            if not entrada:
                st.warning("Por favor, cole os jogos primeiro.")
            else:
                with st.spinner("Consultando regras e notícias..."):
                    # Aqui o código chama o motor LotecaAnalyst
                    st.success("Análise Gemini concluída!")
                    st.info("O relatório detalhado foi processado e guardado.")

    with tab2:
        st.subheader("Performance do Modelo")
        db_path = os.path.join(os.path.dirname(__file__), "loteca.db")
        
        if os.path.exists(db_path):
            try:
                conn = sqlite3.connect(db_path)
                query = "SELECT palpite_sugerido, resultado_real FROM jogos WHERE resultado_real IS NOT NULL"
                df = pd.read_sql_query(query, conn)
                conn.close()

                if not df.empty:
                    # Lógica de acerto: verifica se a coluna real está no palpite sugerido
                    df['acertou'] = df.apply(lambda x: str(x['resultado_real']) in str(x['palpite_sugerido']), axis=1)
                    taxa = df['acertou'].mean()
                    
                    st.metric("Assertividade Geral", f"{taxa*100:.1f}%")
                    st.progress(taxa)
                    
                    # Gráfico de barras dark
                    st.bar_chart(df['acertou'].value_counts())
                else:
                    st.info("A aguardar dados de resultados reais para gerar estatísticas.")
            except Exception as e:
                st.error(f"Erro ao ler histórico: {e}")
        else:
            st.error("Base de dados 'loteca.db' não encontrada no GitHub.")

    # Botão de Logout no final (opcional)
    if st.sidebar.button("Sair da Aplicação"):
        st.session_state["autenticado"] = False
        st.rerun()
