import re
import sqlite3

class LotecaParser:
    def __init__(self, db_name="loteca.db"):
        self.db_name = db_name

    def processar_texto_rodada(self, texto_bruto, data_final):
        # 1. Criar a rodada no banco e pegar o ID
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO rodadas (data_final_rodada) VALUES (?)", (data_final,))
        rodada_id = cursor.lastrowid
        
        # 2. Regex para capturar os confrontos
        # Procura por: (Número opcional) (Time 1) 'x' ou '-' (Time 2)
        padrao = r"(?:\d+[\s.-]*)?(.+?)\s*[xX-]\s*(.+)"
        
        linhas = texto_bruto.strip().split('\n')
        jogos_encontrados = 0

        for linha in linhas:
            match = re.search(padrao, linha)
            if match:
                time1 = match.group(1).strip()
                time2 = match.group(2).strip()
                confronto = f"{time1} x {time2}"
                
                # 3. Inserir o jogo vinculado à rodada
                cursor.execute(
                    "INSERT INTO jogos (rodada_id, confronto) VALUES (?, ?)",
                    (rodada_id, confronto)
                )
                jogos_encontrados += 1
        
        conn.commit()
        conn.close()
        return rodada_id, jogos_encontrados

# Exemplo de uso:
if __name__ == "__main__":
    parser = LotecaParser()
    texto_exemplo = """
    1. Flamengo x Vasco
    2. Palmeiras x Santos
    3. Grêmio x Internacional
    4. Atlético-MG x Cruzeiro
    """
    
    id_r, total = parser.processar_texto_rodada(texto_exemplo, "2026-01-25")
    print(f"Rodada {id_r} criada com {total} jogos inseridos.")