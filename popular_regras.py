import sqlite3

def popular_regras():
    # Conecta-se ao banco de dados (o ficheiro será criado se não existir)
    conn = sqlite3.connect('loteca.db')
    cursor = conn.cursor()

    # Lista das 12 regras estruturadas (Nome, Descrição)
    regras = [
        ("Regra da Rivalidade", "Em clássicos, mesmo que uma equipa esteja numa fase má, o fator emocional equilibra o jogo e a equipa 'dar o sangue'."),
        ("Regra da Economia", "Em início de temporada, equipas grandes tendem a utilizar equipas de reserva ou sub-20 para poupar os titulares."),
        ("Regra da Meteorologia", "Previsão de chuva intensa ou condições climáticas adversas favorecem o empate e o jogo físico em detrimento do técnico."),
        ("Regra da Crise Interna", "Problemas como salários em atraso, direção contestada ou treinador ameaçado prejudicam o rendimento em campo."),
        ("Regra do Mando de Jogo", "O fator casa não garante a vitória, mas exerce uma influência positiva significativa para o clube mandante."),
        ("Regra da Lei do Ex", "Jogadores que enfrentam antigos clubes têm uma tendência estatística para marcar golos ou destacar-se no confronto."),
        ("Regra do Foco Prioritário", "Equipas com jogos decisivos em taças (como Libertadores ou Taça do Brasil) podem negligenciar o jogo do campeonato."),
        ("Regra da Logística Exaustiva", "Viagens continentais longas com menos de 72 horas de intervalo favorecem o adversário ou o empate devido ao desgaste."),
        ("Regra do Fato Novo", "A chegada ou estreia de um novo treinador costuma gerar um choque de motivação imediato no elenco."),
        ("Regra do Gramado Sintético", "Equipas que jogam habitualmente em relvado sintético possuem uma vantagem técnica sobre quem não está adaptado à velocidade da bola."),
        ("Regra do Desespero vs. Zumbi", "Equipas que lutam contra a descida de divisão costumam vencer equipas do meio da tabela que já não lutam por nada."),
        ("Regra da Riqueza", "Clubes com patrocínios milionários ou geridos como SAF tendem a ter elencos mais profundos e efetivos a longo prazo.")
    ]

    try:
        # Insere as regras apenas se a tabela já existir (criada no database.py)
        cursor.executemany(
            "INSERT INTO regras (nome, descricao) VALUES (?, ?)", 
            regras
        )
        conn.commit()
        print(f"Sucesso: {len(regras)} regras foram inseridas na base de dados.")
    except sqlite3.Error as e:
        print(f"Erro ao inserir regras: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    popular_regras()