import customtkinter as ctk
import sqlite3

class RegrasWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Gerenciador de Regras Especialistas")
        self.geometry("500x600")
        self.attributes("-topmost", True) # Mantém a janela na frente

        self.db_path = "loteca.db"
        self.switches = {} # Dicionário para guardar as variáveis dos switches

        # Layout
        self.label = ctk.CTkLabel(self, text="Ativar/Desativar Regras de Análise", 
                                  font=ctk.CTkFont(size=16, weight="bold"))
        self.label.pack(pady=20)

        # Frame com scroll para as regras
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=450, height=400)
        self.scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.carregar_regras_do_banco()

        self.btn_salvar = ctk.CTkButton(self, text="Salvar Configurações", 
                                        command=self.salvar_alteracoes)
        self.btn_salvar.pack(pady=20)

    def carregar_regras_do_banco(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, ativo FROM regras")
        regras = cursor.fetchall()
        conn.close()

        for id_regra, nome, ativo in regras:
            # Variável booleana para o switch
            var = ctk.BooleanVar(value=True if ativo == 1 else False)
            self.switches[id_regra] = var

            # Cria o switch na interface
            switch = ctk.CTkSwitch(self.scroll_frame, text=nome, variable=var)
            switch.pack(pady=10, padx=20, anchor="w")

    def salvar_alteracoes(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for id_regra, var in self.switches.items():
            novo_status = 1 if var.get() else 0
            cursor.execute("UPDATE regras SET ativo = ? WHERE id = ?", (novo_status, id_regra))
        
        conn.commit()
        conn.close()
        self.destroy() # Fecha a janela após salvar