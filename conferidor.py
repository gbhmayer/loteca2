import sqlite3
import google.generativeai as genai
import re

class LotecaConferidor:
    def __init__(self, db_name="loteca.db"):
        self.db_name = db_name
        self.config = self._carregar_config()
        if self.config['api_key']:
            genai.configure(api_key=self.config['api_key'])
            # Usamos um modelo rápido para essa tarefa simples
            self.model = genai.GenerativeModel('gemini-1.5-flash')

    def _carregar_config(self):
        conn = sqlite3.connect(self.db_name)
        row = conn.execute("SELECT gemini_api_key FROM configuracoes LIMIT 1").fetchone()
        conn.close()
        return {'api_key': row[0] if row else None}

    def _determinar_coluna(self, gols_mandante, gols_visitante):
        if gols_mandante > gols_visitante: return '1'
        if gols_visitante > gols_mandante: return '2'
        return 'X'

    def conferir_rodada(self, rodada_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # 1. Busca os jogos da rodada
        cursor.execute("SELECT id, confronto, palpite_sugerido FROM jogos WHERE rodada_id = ?", (rodada_id,))
        jogos = cursor.fetchall()
        
        if not jogos:
            print("Rodada não encontrada.")
            return

        # 2. Monta lista de jogos para o Gemini pesquisar de uma vez
        lista_jogos_txt = "\n".join([f"ID {j[0]}: {j[1]}" for j in jogos])
        
        prompt = f"""
        Você é um conferidor de resultados de futebol.
        Pesquise os placares finais dos jogos abaixo que ocorreram neste fim de semana.
        
        LISTA DE JOGOS:
        {lista_jogos_txt}
        
        Retorne APENAS uma lista no seguinte formato estrito para cada jogo:
        ID: [id do jogo] | PLACAR: [gols time 1] x [gols time 2]
        
        Exemplo de resposta:
        ID: 45 | PLACAR: 2 x 1
        ID: 46 | PLACAR: 0 x 0
        """
        
        print("Consultando resultados via IA... Aguarde.")
        response = self.model.generate_content(prompt)
        texto_resposta = response.text
        
        acertos = 0
        relatorio_final = []

        # 3. Processa a resposta da IA e atualiza o banco
        # Regex para capturar: ID: (número) | PLACAR: (número) x (número)
        padrao_regex = r"ID:\s*(\d+)\s*\|\s*PLACAR:\s*(\d+)\s*x\s*(\d+)"
        
        print("\n--- RESULTADOS ENCONTRADOS ---")
        for match in re.finditer(padrao_regex, texto_resposta):
            jogo_id_str, gols1_str, gols2_str = match.groups()
            jogo_id = int(jogo_id_str)
            gols1 = int(gols1_str)
            gols2 = int(gols2_str)
            
            coluna_vencedora = self._determinar_coluna(gols1, gols2)
            
            # Busca qual era o palpite da IA para este jogo
            palpite_ia = next((j[2] for j in jogos if j[0] == jogo_id), "N/A")
            
            # Verifica se acertou (considerando palpites duplos/triplos como '1X', '1X2')
            status = "ERROU"
            # Se a coluna vencedora '1' estiver dentro do palpite '1X', é acerto.
            if coluna_vencedora in palpite_ia.replace(" ", "").replace("Meio", "X").replace("Coluna", ""):
                status = "ACERTOU"
                acertos += 1

            # Atualiza o banco (você precisaria criar essa coluna 'resultado_real' no banco primeiro)
            # cursor.execute("UPDATE jogos SET resultado_real = ? WHERE id = ?", (coluna_vencedora, jogo_id))
            
            linha_relatorio = f"Jogo ID {jogo_id}: Placar {gols1}x{gols2} (Col {coluna_vencedora}) | IA previu: {palpite_ia} -> {status}"
            print(linha_relatorio)
            relatorio_final.append(linha_relatorio)

        conn.commit()
        conn.close()
        
        resumo = f"\n=== RESUMO FINAL ===\nTotal de Acertos da IA: {acertos} de {len(jogos)}"
        print(resumo)
        relatorio_final.append(resumo)
        
        # Salva um txt com a conferência
        with open(f"Conferencia_Rodada_{rodada_id}.txt", "w") as f:
            f.write("\n".join(relatorio_final))
            
        return acertos, len(jogos)

# --- Teste rápido (Requer que uma rodada exista no banco e a API Key esteja configurada) ---
# if __name__ == "__main__":
#    conferidor = LotecaConferidor()
#    # Substitua 1 pelo ID da rodada que você quer conferir
#    conferidor.conferir_rodada(1)