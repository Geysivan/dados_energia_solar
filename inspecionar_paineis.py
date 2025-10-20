import pandas as pd
import os

# --- 1. Configuração dos Arquivos ---
# A pasta é a mesma onde o script está rodando.
pasta_dados = os.path.dirname(os.path.abspath(__file__))

# Lista com os nomes dos arquivos Excel que você mencionou.
# Verifique se os nomes correspondem exatamente aos arquivos na sua pasta.
arquivos_excel = [
    "capacidade_instalada.xlsx",
    "geracao_e_eletricidade.xlsx",
    "retorno_fianceiro.xlsx", # Mantive o nome como vc escreveu, com "fianceiro"
    "projecoes.xlsx"
]

# --- 2. Inspecionar cada arquivo da lista ---
print("🕵️  Iniciando a inspeção dos arquivos do painel da EPE...")

for nome_arquivo in arquivos_excel:
    caminho_arquivo = os.path.join(pasta_dados, nome_arquivo)
    print(f"\n======================================================================")
    print(f"|| Inspecionando Arquivo: {nome_arquivo}")
    print(f"======================================================================")
    
    try:
        # Tenta ler o arquivo Excel. pd.read_excel lê a primeira planilha por padrão.
        df = pd.read_excel(caminho_arquivo)
        
        # Mostra a lista de colunas
        print("\n✅ Colunas encontradas:")
        print(df.columns.tolist())
        
        # Mostra as 10 primeiras linhas do arquivo
        print("\n✅ Conteúdo das 10 primeiras linhas:")
        # O .to_string() garante que todas as colunas sejam exibidas
        print(df.head(10).to_string())

    except FileNotFoundError:
        print(f"\n❌ ERRO: O arquivo '{nome_arquivo}' não foi encontrado na pasta.")
        print("   Por favor, verifique se o nome está correto e se o arquivo está no lugar certo.")
    except Exception as e:
        print(f"\n⚠️ Erro inesperado ao tentar ler o arquivo '{nome_arquivo}': {e}")