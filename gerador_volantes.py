from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import os

class GeradorPDFLoteca:
    def __init__(self, nome_arquivo="Volantes_Loteca_Para_Marcar.pdf"):
        self.nome_arquivo = nome_arquivo
        # Configurações de layout (em centímetros)
        self.margem_esquerda = 2 * cm
        self.altura_inicial = 27 * cm
        self.espaco_entre_linhas = 1.5 * cm
        self.largura_coluna_check = 1.5 * cm

    def desenhar_cabecalho(self, c, numero_volante):
        c.setFont("Helvetica-Bold", 16)
        c.drawString(self.margem_esquerda, self.altura_inicial + 1*cm, f"LOTECA EXPERT AI - VOLANTE {numero_volante:02d}")
        c.setFont("Helvetica", 10)
        c.drawString(self.margem_esquerda, self.altura_inicial + 0.3*cm, "Use este guia para marcar seu cartão na lotérica.")
        
        # Desenha cabeçalho das colunas
        c.setFont("Helvetica-Bold", 12)
        y_cols = self.altura_inicial - 0.5 * cm
        c.drawString(self.margem_esquerda + 7*cm, y_cols, "COL 1")
        c.drawString(self.margem_esquerda + 9.5*cm, y_cols, "COL X")
        c.drawString(self.margem_esquerda + 12*cm, y_cols, "COL 2")
        c.line(self.margem_esquerda, y_cols - 0.2*cm, self.margem_esquerda + 15*cm, y_cols - 0.2*cm)

    def desenhar_linha_jogo(self, c, numero_jogo, palpite_simples, y_pos):
        """Deseja uma linha com o número do jogo e os quadrados de marcação"""
        # Número do Jogo
        c.setFont("Helvetica-Bold", 12)
        c.drawString(self.margem_esquerda, y_pos + 0.3*cm, f"Jogo {numero_jogo:02d}")
        
        # Posições X dos quadrados
        x_col1 = self.margem_esquerda + 7 * cm
        x_colX = self.margem_esquerda + 9.5 * cm
        x_col2 = self.margem_esquerda + 12 * cm
        
        # Tamanho do quadrado
        tamanho_box = 0.8 * cm
        
        # Função auxiliar para desenhar o quadrado e marcar X se necessário
        def desenhar_box(x_pos, coluna_alvo):
            # Desenha o quadrado vazio
            c.rect(x_pos, y_pos, tamanho_box, tamanho_box, fill=0)
            # Se o palpite for para esta coluna, desenha um "X" grande dentro
            if palpite_simples == coluna_alvo:
                c.setFont("Helvetica-Bold", 14)
                # Ajuste fino para centralizar o X no quadrado
                c.drawString(x_pos + 0.15*cm, y_pos + 0.15*cm, "X")

        desenhar_box(x_col1, '1')
        desenhar_box(x_colX, 'X')
        desenhar_box(x_col2, '2')
        
        # Linha divisória sutil
        c.setStrokeColorRGB(0.8, 0.8, 0.8)
        c.line(self.margem_esquerda, y_pos - 0.3*cm, self.margem_esquerda + 15*cm, y_pos - 0.3*cm)
        c.setStrokeColorRGB(0, 0, 0) # Volta para preto

    def gerar_pdf_volantes(self, lista_de_volantes):
        """
        Recebe uma lista de listas. Ex: [['1', 'X', ...], ['1', '1', ...]]
        Cada sublista é um volante de 14 jogos.
        """
        c = canvas.Canvas(self.nome_arquivo, pagesize=A4)
        
        for i, volante_atual in enumerate(lista_de_volantes, 1):
            self.desenhar_cabecalho(c, i)
            
            y_atual = self.altura_inicial - 2 * cm
            
            for num_jogo, palpite in enumerate(volante_atual, 1):
                self.desenhar_linha_jogo(c, num_jogo, palpite, y_atual)
                y_atual -= self.espaco_entre_linhas
                
            # Finaliza a página atual e cria uma nova para o próximo volante
            c.showPage()
            
        c.save()
        print(f"PDF gerado com sucesso: {self.nome_arquivo}")
        os.startfile(self.nome_arquivo)

# --- Teste rápido isolado ---
if __name__ == "__main__":
    # Simulação de 2 volantes gerados pelo módulo de fechamento
    volante_teste_1 = ['1', 'X', '2', '1', 'X', '2', '1', 'X', '2', '1', 'X', '2', '1', 'X']
    volante_teste_2 = ['1', '1', '1', 'X', 'X', 'X', '2', '2', '2', '1', '1', '1', 'X', 'X']
    
    gerador = GeradorPDFLoteca()
    gerador.gerar_pdf_volantes([volante_teste_1, volante_teste_2])