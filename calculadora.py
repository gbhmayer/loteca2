import sqlite3

class LotecaCalc:
    def __init__(self, db_name="loteca.db"):
        self.db_name = db_name

    def obter_preco_base(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT preco_base_aposta FROM configuracoes LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else 3.00

    def calcular_custo_total(self, num_duplos, num_triplos):
        p_base = self.obter_preco_base()
        custo = p_base * (2 ** num_duplos) * (3 ** num_triplos)
        return custo

    def gerar_fechamento_simples(self, palpites_principais):
        """
        Transforma palpites com duplos e triplos em uma lista de cartões simples.
        Exemplo: '1', '1X', '1X2' -> vira uma lista de strings para volantes individuais.
        """
        import itertools
        
        # Converte strings como '1X' em listas ['1', 'X']
        opcoes_por_jogo = []
        for p in palpites_principais:
            if p == '1X': opcoes_por_jogo.append(['1', 'X'])
            elif p == 'X2': opcoes_por_jogo.append(['X', '2'])
            elif p == '12': opcoes_por_jogo.append(['1', '2'])
            elif p == '1X2': opcoes_por_jogo.append(['1', 'X', '2'])
            else: opcoes_por_jogo.append([p]) # Secos: '1', 'X' ou '2'

        # Gera o produto cartesiano (todas as combinações possíveis)
        combinacoes = list(itertools.product(*opcoes_por_jogo))
        return combinacoes

# Exemplo de teste
if __name__ == "__main__":
    calc = LotecaCalc()
    # Simulação: 2 duplos e 1 triplo
    preco = calc.calcular_custo_total(2, 1)
    print(f"Custo para 2 Duplos e 1 Triplo: R$ {preco:.2f}")
    
    # Exemplo de expansão de um jogo pequeno (apenas 3 jogos para ilustrar)
    meus_palpites = ['1', '1X', '1X2'] # Jogo 1 seco, Jogo 2 duplo, Jogo 3 triplo
    cartoes = calc.gerar_fechamento_simples(meus_palpites)
    print(f"Total de cartões simples gerados: {len(cartoes)}")
    for i, c in enumerate(cartoes):
        print(f"Cartão {i+1}: {c}")