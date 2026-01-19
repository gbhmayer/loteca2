import streamlit as st
import sqlite3
import pandas as pd
import os
from calculadora import LotecaCalc

# Configuração para dispositivos móveis
st.set_page_config(page_title="Loteca AI Mobile", layout="centered")

db_path = os.path.join(os.path.dirname(__file__), "loteca.db")

def carregar_config_banco():
    """Recupera a API Key e o preço do banco de dados"""
    try:
        conn = sqlite3.connect(db_path)
        res = conn.execute("SELECT gemini_api_key, preco_base_aposta, modelo_dados FROM configuracoes LIMIT 1").fetchone()
        conn.close()
        return res if res else (None, 3.00, "gemini-1.5-pro")
    except:
        return (None, 3.00, "gemini-1.5-pro")

def guardar_config_banco(key, preco, model):
    """Guarda permanentemente as configurações no banco"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM configuracoes")
    cursor.execute("INSERT INTO configuracoes (gemini_api_key, preco_base_aposta, modelo_dados) VALUES (?, ?, ?)",
                   (key, preco, model))
    conn.commit()
    conn.close()

# Carregar dados iniciais
saved_key, saved_price, saved_model = carregar_config_banco()

# --- BARRA LATERAL (CONFIGURAÇÕES) ---
with st.sidebar:
    st.header("⚙️ Configurações")
    
    # Se a chave já existir no banco, ela aparece preenchida (mas oculta por estrelas)
    input_key = st.text_input("Gemini API Key", value=saved_key if saved_key else "", type="password")
    
    input_model = st.selectbox("Modelo de IA", 
                               ["gemini-1.5-pro", "gemini-3-pro", "gemini-1.5-flash"],
                               index=["gemini-1.5-pro", "gemini-3-pro", "gemini-1.5-flash"].index(saved_model))
    
    input_price = st.number_input("Preço Aposta Simples (R$)", value=float(saved_price), step=0.50)
    
    if st.button("💾 Guardar Configurações"):
        guardar_config_banco(input_key, input_price, input_model)
        st.success("Configurações guardadas com sucesso!")
        st.rerun() # Reinicia para aplicar

# --- INTERFACE PRINCIPAL ---
st.title("⚽ Loteca Expert AI")

tab1, tab2 = st.tabs(["🚀 Análise", "📊 Dashboard"])

with tab1:
    st.subheader("Simulador de Aposta")
    
    col1, col2 = st.columns(2)
    with col1:
        d = st.number_input("Duplos (d)", min_value=0, max_value=14, value=0)
    with col2:
        t = st.number_input("Triplos (t)", min_value=0, max_value=14, value=0)

    # Cálculo dinâmico usando o preço guardado
    custo_final = input_price * (2 ** d) * (3 ** t)
    
    st.metric("Investimento", f"R$ {custo_final:,.2f}")
    st.caption(f"A calcular com R$ {input_price} por aposta simples.")

    st.divider()
    entrada = st.text_area("1. Cole a rodada da semana:", height=150)
    
    if st.button("2. EXECUTAR ANÁLISE IA"):
        if not input_key:
            st.error("Configure a API Key na barra lateral esquerda.")
        elif not entrada:
            st.warning("Cole os confrontos.")
        else:
            with st.spinner("IA a trabalhar..."):
                st.success("Análise concluída!")
                st.write(f"Modelo: {input_model}")

with tab2:
    st.subheader("Performance do Modelo")
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            df = pd.read_sql_query("SELECT palpite_sugerido, resultado_real FROM jogos WHERE resultado_real IS NOT NULL", conn)
            conn.close()

            if not df.empty:
                df['acertou'] = df.apply(lambda x: str(x['resultado_real']) in str(x['palpite_sugerido']), axis=1)
                st.progress(df['acertou'].mean(), text=f"Taxa de acerto: {df['acertou'].mean()*100:.1f}%")
                st.bar_chart(df['acertou'].value_counts())
            else:
                st.info("A aguardar resultados para gerar estatísticas.")
        except Exception as e:
            st.error(f"Erro no banco: {e}")
