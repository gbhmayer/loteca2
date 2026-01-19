import itertools

class LotecaFechamento:
    def __init__(self):
        # Matriz simplificada para 3 Triplos Reduzidos (Garante 13 se acertar os 14)
        # Em vez de 27 jogos, usamos apenas 9.
        self.matriz_3t_reduzida = [
            ['1', '1', '1'], ['1', 'X', 'X'], ['1', '2', '2'],
            ['X', '1', 'X'], ['X', 'X', '2'], ['X', '2', '1'],
            ['2', '1', '2'], ['2', 'X', '1'], ['2', '2', 'X']
        ]

    def gerar_desdobramento_total(self, palpites_lista):
        """
        Gera TODAS as combinações possíveis (Custo integral).
        palpites_lista: Lista de strings ['1', '1X', '1X2', ...]
        """
        opcoes = []
        for p in palpites_lista:
            # Converte '1X' em ['1', 'X'], etc.
            opcoes.append(list(p.replace(" ", "")))
        
        # Produto cartesiano de todas as opções
        combinacoes = list(itertools.product(*opcoes))
        return combinacoes

    def gerar_reduzido_3t(self, palpites_lista):
        """
        Exemplo de fechamento reduzido para 3 triplos específicos.
        Reduz de 27 para 9 cartões com garantia de 13 pontos.
        """
        # Identifica quais índices são triplos
        indices_triplos = [i for i, p in enumerate(palpites_lista) if len(p) == 3]
        
        if len(indices_triplos) < 3:
            return "Erro: É necessário ao menos 3 triplos para este fechamento."

        jogos_gerados = []
        for linha_matriz in self.matriz_3t_reduzida:
            novo_cartao = list(palpites_lista)
            for i, idx in enumerate(indices_triplos[:3]): # Aplica nos 3 primeiros triplos
                novo_cartao[idx] = linha_matriz[i]
            jogos_gerados.append(novo_cartao)
            
        return jogos_gerados