import sqlite3
import os
from datetime import datetime

def gerar_relatorio_txt(rodada_id):
    conn = sqlite3.connect("loteca.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT confronto, analise_detalhada, palpite_sugerido 
        FROM jogos WHERE rodada_id = ?
    """, (rodada_id,))
    jogos = cursor.fetchall()
    
    filename = f"Analise_Loteca_Rodada_{rodada_id}.txt"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"=== RELATÓRIO DE ANÁLISE LOTECA AI ===\n")
        f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        f.write("="*40 + "\n\n")
        
        for i, (conf, analise, palpite) in enumerate(jogos, 1):
            f.write(f"JOGO {i:02d}: {conf}\n")
            f.write(f"ANÁLISE: {analise.strip()}\n")
            f.write(f"PALPITE: {palpite}\n")
            f.write("-" * 30 + "\n")
            
    conn.close()
    os.startfile(filename)
    return filename