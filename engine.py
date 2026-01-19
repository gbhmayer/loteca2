import google.generativeai as genai

class LotecaEngine:
    def __init__(self, api_key, model_name='gemini-1.5-pro'):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def gerar_prompt_analise(self, jogo, regras):
        """Monta o prompt estruturado com as suas regras personalizadas."""
        texto_regras = "\n".join([f"- {r[0]}: {r[1]}" for r in regras])
        
        prompt = f"""
        Você é um especialista em análise tática e estatística de futebol para a Loteca.
        
        REGRAS DE ANÁLISE (Obrigatórias):
        {texto_regras}
        
        CONFRONTO ATUAL: {jogo}
        
        TAREFA:
        1. Pesquise notícias recentes (até hoje) sobre esses times.
        2. Aplique cada uma das regras acima ao contexto do jogo.
        3. Identifique desfalques, crises ou mudanças de última hora.
        4. Forneça um relatório técnico detalhado.
        5. Sugira o palpite: Coluna 1 (Mandante), Meio (Empate) ou Coluna 2 (Visitante).
        
        Responda em formato estruturado.
        """
        return prompt

    def analisar_partida(self, jogo, lista_regras):
        prompt = self.gerar_prompt_analise(jogo, lista_regras)
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Erro na análise: {str(e)}"