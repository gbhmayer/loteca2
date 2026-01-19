import sqlite3
import os

class LotecaCalc:
    def __init__(self):
        # Procura o banco na mesma pasta do script
        self.db_path = os.path.join(os.path.dirname(__file__), "loteca.db")

    def get_base_price(self):
        try:
            conn = sqlite3.connect(self.db_path)
            res = conn.execute("SELECT preco_base_aposta FROM configuracoes LIMIT 1").fetchone()
            conn.close()
            return res[0] if res else 3.00
        except:
            return 3.00 # Valor padrão caso o banco não exista ainda

    def calcular_total(self, duplos, triplos):
        """Fórmula: PreçoBase * 2^D * 3^T"""
        base = self.get_base_price()
        return base * (2 ** duplos) * (3 ** triplos)
