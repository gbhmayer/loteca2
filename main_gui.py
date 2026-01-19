import customtkinter as ctk
from database import LotecaDB
from parser_jogos import LotecaParser
from analisador import LotecaAnalyst
from calculadora import LotecaCalc
from regras_gui import RegrasWindow

# Configuração de aparência
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class LotecaApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Loteca Expert AI - 2026")
        self.geometry("1100x700")

        # Inicialização dos módulos
        self.db = LotecaDB()
        self.parser = LotecaParser()
        self.calc = LotecaCalc()

        # Layout em Grid (2 colunas, 1 linha)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR (Configurações e Regras) ---
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="LOTECA AI", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(pady=20)

        self.btn_regras = ctk.CTkButton(self.sidebar, text="Gerenciar Regras", command=self.abrir_regras)
        self.btn_regras.pack(pady=10, padx=20)

        self.label_custo = ctk.CTkLabel(self.sidebar, text="Custo Estimado: R$ 0,00", font=("Arial", 14))
        self.label_custo.pack(side="bottom", pady=20)

        # --- ÁREA PRINCIPAL ---
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.label_instrucao = ctk.CTkLabel(self.main_frame, text="Cole a rodada da semana abaixo:")
        self.label_instrucao.pack(pady=10)

        # Campo para colar os jogos
        self.txt_jogos = ctk.CTkTextbox(self.main_frame, height=200, width=600)
        self.txt_jogos.pack(pady=10, padx=20)

        # Botões de Ação
        self.btn_processar = ctk.CTkButton(self.main_frame, text="1. Processar Rodada", command=self.processar_rodada)
        self.btn_processar.pack(pady=5)

        self.btn_analisar = ctk.CTkButton(self.main_frame, text="2. Analisar com Gemini", 
                                          fg_color="green", hover_color="darkgreen", command=self.executar_ia)
        self.btn_analisar.pack(pady=5)

        # Área de Resultados
        self.txt_resultado = ctk.CTkTextbox(self.main_frame, height=250, width=700)
        self.txt_resultado.pack(pady=20, padx=20)

    # --- FUNÇÕES DE INTERFACE ---
    def processar_rodada(self):
        texto = self.txt_jogos.get("1.0", "end")
        data_f = "2026-01-25" # Exemplo: pegar de um campo de data futuramente
        id_r, total = self.parser.processar_texto_rodada(texto, data_f)
        self.txt_resultado.insert("end", f"Sucesso! {total} jogos carregados na Rodada ID: {id_r}\n")
        self.rodada_atual = id_r

    def executar_ia(self):
        self.txt_resultado.insert("end", "Iniciando análise inteligente... Aguarde.\n")
        analista = LotecaAnalyst()
        analista.analisar_rodada(self.rodada_atual)
        self.txt_resultado.insert("end", "Análise concluída! Verifique o banco de dados ou relatórios.\n")

    def abrir_regras(self):
        # Aqui você criaria uma nova janela Toplevel para ativar/desativar as 12 regras
        print("Abrindo gestão de regras...")
        if not hasattr(self, "janela_regras") or not self.janela_regras.winfo_exists():
            self.janela_regras = RegrasWindow(self)
        else:
            self.janela_regras.focus()

if __name__ == "__main__":
    app = LotecaApp()
    app.mainloop()