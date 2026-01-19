import sqlite3

class LotecaDB:
    def __init__(self, db_name="loteca.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        
        # 1. Configurações (API Key, Modelo, Preço Base)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS configuracoes (
                id INTEGER PRIMARY KEY,
                gemini_api_key TEXT,
                modelo_dados TEXT DEFAULT 'gemini-1.5-pro',
                preco_base_aposta REAL DEFAULT 3.00
            )
        ''')

        # 2. Gestão de Regras
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS regras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT NOT NULL,
                ativo INTEGER DEFAULT 1
            )
        ''')

        # 3. Rodadas (para agrupar os 14 jogos)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rodadas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_final_rodada DATE,
                status TEXT DEFAULT 'Pendente'
            )
        ''')

        # 4. Jogos e Análises
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jogos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rodada_id INTEGER,
                confronto TEXT,
                analise_detalhada TEXT,
                palpite_sugerido TEXT,
                FOREIGN KEY (rodada_id) REFERENCES rodadas(id)
            )
        ''')
        
        self.conn.commit()

    def inserir_regra_inicial(self, nome, descricao):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO regras (nome, descricao) VALUES (?, ?)", (nome, descricao))
        self.conn.commit()

# Inicialização rápida para teste
if __name__ == "__main__":
    db = LotecaDB()
    print("Banco de dados e tabelas criados com sucesso!")