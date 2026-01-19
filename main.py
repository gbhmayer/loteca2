import customtkinter as ctk
import sqlite3
import re
import os
import sys
import threading
from datetime import datetime
from tkinter import messagebox

# Módulos customizados
from database import LotecaDB
from parser_jogos import LotecaParser
from analisador import LotecaAnalyst
from calculadora import LotecaCalc
from config_gui import ConfigWindow
from relatorio import gerar_relatorio_txt
from fechamentos import LotecaFechamento
from gerador_volantes import GeradorPDFLoteca
from conferidor import LotecaConferidor
from dashboard import LotecaDashboard

def resource_path(relative_path):
    """ Suporte para caminhos de arquivos no executável PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

class LotecaApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Loteca Expert AI v1.0")
        self.geometry("1200x850")
        
        self.db = LotecaDB()
        self.parser = LotecaParser()
        self.calc = LotecaCalc()
        self.rodada_id = None

        self.setup_ui()
        self.after(5000, self.verificar_resultados_pendentes)

    def setup_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # SIDEBAR
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        ctk.CTkLabel(self.sidebar, text="LOTECA AI", font=("Arial", 24, "bold")).pack(pady=30)

        # BOTÕES
        ctk.CTkButton(self.sidebar, text="⚙ Configurações API", command=self.open_config).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="📊 Dashboard", command=self.open_dashboard).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="🖨 Gerar PDF", fg_color="#e67e22", command=self.gerar_pdf_final).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="✅ Conferir", fg_color="#9b59b6", command=self.conferir_resultados_ia).pack(pady=10, padx=20)

        # CUSTO
        self.cost_frame = ctk.CTkFrame(self.sidebar, fg_color="#2c3e50", corner_radius=10)
        self.cost_frame.pack(side="bottom", fill="x", pady=40, padx=20)
        self.lbl_custo_valor = ctk.CTkLabel(self.cost_frame, text="R$ 0,00", font=("Arial", 22, "bold"), text_color="#2ecc71")
        self.lbl_custo_valor.pack(pady=10)

        # MAIN
        self.main_scroll = ctk.CTkScrollableFrame(self, corner_radius=0)
        self.main_scroll.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.txt_input = ctk.CTkTextbox(self.main_scroll, height=150)
        self.txt_input.pack(fill="x", padx=10, pady=10)
        ctk.CTkButton(self.main_scroll, text="Carregar Rodada", command=self.load_games).pack()

        self.entry_stats = ctk.CTkEntry(self.main_scroll, placeholder_text="Ex: 3d 1t", height=40)
        self.entry_stats.pack(fill="x", padx=10, pady=20)
        self.entry_stats.bind("<KeyRelease>", self.on_stats_change)

        self.btn_ai = ctk.CTkButton(self.main_scroll, text="⚡ ANALISAR COM GEMINI", height=60, command=self.run_ai)
        self.btn_ai.pack(fill="x", pady=10, padx=10)

        self.txt_output = ctk.CTkTextbox(self.main_scroll, height=350, fg_color="#1e1e1e")
        self.txt_output.pack(fill="both", expand=True, padx=10, pady=10)

    # Lógica de Automatação e UI (Simplificada para o exemplo)
    def on_stats_change(self, event):
        texto = self.entry_stats.get().lower()
        d = re.search(r'(\d+)\s*d', texto)
        t = re.search(r'(\d+)\s*t', texto)
        custo = self.calc.calcular_total(int(d.group(1)) if d else 0, int(t.group(1)) if t else 0)
        self.lbl_custo_valor.configure(text=f"R$ {custo:,.2f}")

    def load_games(self):
        texto = self.txt_input.get("1.0", "end").strip()
        self.rodada_id, total = self.parser.processar_texto_rodada(texto, datetime.now().strftime("%Y-%m-%d"))
        self.log(f"Rodada {self.rodada_id} carregada.")

    def run_ai(self):
        analista = LotecaAnalyst()
        analista.analisar_rodada(self.rodada_id)
        self.log("IA finalizou a análise.")

    def verificar_resultados_pendentes(self):
        thread = threading.Thread(target=lambda: self.log("[AUTO] Verificando resultados passados..."))
        thread.start()

    def open_dashboard(self): LotecaDashboard(self)
    def open_config(self): ConfigWindow(self)
    def gerar_pdf_final(self): self.log("PDF Gerado.")
    def conferir_resultados_ia(self): self.log("Conferindo...")
    def export_report(self): gerar_relatorio_txt(self.rodada_id)
    def log(self, msg): self.txt_output.insert("end", f"> {msg}\n"); self.txt_output.see("end")

if __name__ == "__main__":
    app = LotecaApp()
    app.mainloop()