import os
import subprocess
import shutil
import sys

# --- CONFIGURAÇÕES ---
NOME_APP = "LotecaExpertAI"
ARQUIVO_PRINCIPAL = "main.py"
BANCO_DADOS = "loteca.db"
# Caminho do PyInstaller que identificamos no seu sistema
PYINSTALLER_PATH = r"C:\Users\gbhma\AppData\Local\Programs\Python\Python314\Scripts\pyinstaller.exe"

def criar_executavel():
    print(f"--- Iniciando Build do {NOME_APP} ---")

    # 1. Verificações Iniciais
    if not os.path.exists(ARQUIVO_PRINCIPAL):
        print(f"Erro: {ARQUIVO_PRINCIPAL} não encontrado!")
        return

    # 2. Comando do PyInstaller
    # --noconsole: não abre tela preta
    # --onefile: gera apenas um .exe
    # --clean: limpa cache antes de buildar
    comando = [
        PYINSTALLER_PATH,
        "--noconsole",
        "--onefile",
        "--clean",
        "--name", NOME_APP,
        "--add-data", f"{BANCO_DADOS};.",
        ARQUIVO_PRINCIPAL
    ]

    try:
        print("Executando PyInstaller... Isso pode levar um minuto.")
        subprocess.run(comando, check=True)
        print("\n[OK] Executável gerado com sucesso na pasta 'dist'.")

        # 3. Copiar o Banco de Dados para a pasta dist (Garante que as regras funcionem)
        dist_path = os.path.join("dist", BANCO_DADOS)
        if os.path.exists(BANCO_DADOS):
            shutil.copy(BANCO_DADOS, dist_path)
            print(f"[OK] Banco de dados {BANCO_DADOS} copiado para a pasta 'dist'.")

        print(f"\n--- TUDO PRONTO! ---")
        print(f"Seu programa está pronto em: {os.path.abspath('dist')}")

    except subprocess.CalledProcessError as e:
        print(f"\n[ERRO] Falha durante a execução do PyInstaller: {e}")
    except Exception as e:
        print(f"\n[ERRO] Ocorreu um problema inesperado: {e}")

if __name__ == "__main__":
    criar_executavel()