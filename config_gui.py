import customtkinter as ctk
import sqlite3

class ConfigWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Configurações do Sistema")
        self.geometry("450x400")
        self.attributes("-topmost", True)
        self.db_path = "loteca.db"

        ctk.CTkLabel(self, text="Configurações de API e Sistema", font=("Arial", 16, "bold")).pack(pady=20)

        # API Key
        ctk.CTkLabel(self, text="Gemini API Key:").pack()
        self.entry_key = ctk.CTkEntry(self, width=350, show="*")
        self.entry_key.pack(pady=5)

        # Modelo
        ctk.CTkLabel(self, text="Modelo de IA:").pack()
        self.combo_model = ctk.CTkComboBox(self, values=["gemini-1.5-pro", "gemini-1.5-flash", "gemini-3-pro"], width=200)
        self.combo_model.pack(pady=5)

        # Preço Base
        ctk.CTkLabel(self, text="Preço Aposta Simples (R$):").pack()
        self.entry_price = ctk.CTkEntry(self, width=100)
        self.entry_price.pack(pady=5)

        self.btn_save = ctk.CTkButton(self, text="Salvar Configurações", fg_color="green", command=self.save)
        self.btn_save.pack(pady=30)

        self.load_current_config()

    def load_current_config(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT gemini_api_key, modelo_dados, preco_base_aposta FROM configuracoes LIMIT 1")
        row = cursor.fetchone()
        if row:
            self.entry_key.insert(0, row[0] or "")
            self.combo_model.set(row[1] or "gemini-1.5-pro")
            self.entry_price.insert(0, str(row[2] or "3.00"))
        conn.close()

    def save(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM configuracoes")
        cursor.execute("INSERT INTO configuracoes (gemini_api_key, modelo_dados, preco_base_aposta) VALUES (?, ?, ?)",
                       (self.entry_key.get(), self.combo_model.get(), float(self.entry_price.get().replace(",", "."))))
        conn.commit()
        conn.close()
        self.destroy()