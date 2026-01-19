import sqlite3
import google.generativeai as genai

class LotecaAnalyst:
    def __init__(self, db_name="loteca.db"):
        self.db_name = db_name
        self.config = self._carregar_configuracoes()
        
        # Inicializa a API com a sua chave e modelo preferido
        if self.config['api_key']:
            genai.configure(api_key=self.config['api_key'])
            self.model = genai.GenerativeModel(self.config['modelo'])

    def _carregar_configuracoes(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT gemini_api_key, modelo_dados FROM configuracoes LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        return {
            'api_key': row[0] if row else None,
            'modelo': row[1] if row else 'gemini-1.5-pro'
        }

    def _obter_regras_ativas(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT nome, descricao FROM regras WHERE ativo = 1")
        regras = cursor.fetchall()
        conn.close()
        return "\n".join([f"- {r[0]}: {r[1]}" for r in regras])

    def analisar_rodada(self, rodada_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Busca todos os jogos pendentes desta rodada
        cursor.execute("SELECT id, confronto FROM jogos WHERE rodada_id = ?", (rodada_id,))
        jogos = cursor.fetchall()
        regras_texto = self._obter_regras_ativas()

        print(f"Iniciando análise da Rodada {rodada_id}...")

        for jogo_id, confronto in jogos:
            print(f"Analisando: {confronto}...")
            
            prompt = f"""
            Você é um sistema especialista em previsões de futebol para a Loteca.
            Use suas ferramentas de busca para encontrar notícias de hoje sobre os times abaixo.
            
            CONFRONTO: {confronto}
            
            REGRAS PARA APLICAR NA ANÁLISE:
            {regras_texto}
            
            FORMATO DE RESPOSTA (Obrigatório):
            ANÁLISE: (Um parágrafo resumindo notícias, desfalques, clima e aplicação das regras)
            PALPITE: (Responda apenas com: Coluna 1, Meio ou Coluna 2)
            """

            try:
                response = self.model.generate_content(prompt)
                full_text = response.text
                
                # Divisão simples para extrair análise e palpite
                partes = full_text.split("PALPITE:")
                analise_detalhada = partes[0].replace("ANÁLISE:", "").strip()
                palpite_sugerido = partes[1].strip() if len(partes) > 1 else "Inconclusivo"

                # Atualiza o banco com o resultado
                cursor.execute("""
                    UPDATE jogos 
                    SET analise_detalhada = ?, palpite_sugerido = ? 
                    WHERE id = ?
                """, (analise_detalhada, palpite_sugerido, jogo_id))
                
                conn.commit()
            except Exception as e:
                print(f"Erro ao analisar {confronto}: {e}")

        conn.close()
        print("Análise completa finalizada.")

# Para rodar o teste (assumindo que a Rodada 1 existe)
if __name__ == "__main__":
    analista = LotecaAnalyst()
    analista.analisar_rodada(1)