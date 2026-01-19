import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk

class LotecaDashboard(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Dashboard de Assertividade")
        self.geometry("900x600")
        self.attributes("-topmost", True)

        self.gerar_grafico_acertos()

    def calcular_performance_regras(self):
        """
        Lógica para cruzar quais regras foram citadas na análise 
        e se o palpite final foi certeiro.
        """
        conn = sqlite3.connect("loteca.db")
        cursor = conn.cursor()
        
        # Busca jogos que já possuem resultado real
        cursor.execute("""
            SELECT analise_detalhada, palpite_sugerido, resultado_real 
            FROM jogos 
            WHERE resultado_real IS NOT NULL
        """)
        dados = cursor.fetchall()
        conn.close()

        # Dicionário para contar acertos por regra (Exemplo simplificado)
        # Em um sistema avançado, buscaríamos palavras-chave das regras na analise_detalhada
        stats = {"Riqueza": 0, "Rivalidade": 0, "Crise": 0, "Mando": 0, "Outras": 0}
        total_jogos = len(dados)

        for analise, palpite, real in dados:
            acertou = real in palpite
            # Se a análise cita termos de uma regra, atribuímos o acerto/erro a ela
            if "milionário" in analise.lower() or "saf" in analise.lower():
                if acertou: stats["Riqueza"] += 1
            if "clássico" in analise.lower() or "rivalidade" in analise.lower():
                if acertou: stats["Rivalidade"] += 1
            # ... repetir para outras regras ...

        return stats

    def gerar_grafico_acertos(self):
        stats = self.calcular_performance_regras()
        
        # Criando a figura do Matplotlib
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        fig.patch.set_facecolor('#2b2b2b') # Cor de fundo Dark
        ax.set_facecolor('#2b2b2b')

        regras = list(stats.keys())
        valores = list(stats.values())

        bars = ax.bar(regras, valores, color='#2980b9')
        
        # Estilização do Gráfico
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.set_title("Eficiência por Regra Especialista", color='white', pad=20)
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Integrando o gráfico no CustomTkinter
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)