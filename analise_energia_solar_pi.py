import pandas as pd
import os

# --- 1. Configuração dos Arquivos ---
pasta_dados = os.path.dirname(os.path.abspath(__file__))
arquivo_principal = "capacidade_instalada.xlsx"
caminho_arquivo = os.path.join(pasta_dados, arquivo_principal)

arquivo_saida = "dados_para_mapa.csv"
caminho_saida = os.path.join(pasta_dados, arquivo_saida)

# --- 2. Carregar e Filtrar os Dados do Excel ---
try:
    df = pd.read_excel(caminho_arquivo)
    print("✅ Arquivo Excel 'capacidade_instalada.xlsx' carregado com sucesso.")

    # --- PASSO DE CORREÇÃO: Limpeza dos Nomes das Colunas ---
    # Remove espaços em branco do início e do fim de todos os nomes de colunas
    df.columns = df.columns.str.strip()
    print("🧹 Nomes das colunas limpos e padronizados.")
    print("📋 Colunas encontradas após a limpeza:", df.columns.tolist())

    print("\n🔍 Aplicando filtros para o mapa...")

    # Aplica todos os filtros que você definiu
    df_filtrado = df[
        (df['uf'] == 'PI') &
        (df['fonte_resumo'] == 'Fotovoltaica') &
        (df['classe'].isin(['Residencial', 'Rural'])) &
        (df['subgrupo'].isin(['B1', 'B2'])) &
        (df['modalidade'].isin(['Geração na própria UC', 'Autoconsumo remoto', 'Geração compartilhada'])) &
        (df['mini_micro'].isin(['MicroGD'])) &
        (df['segmento'].isin(['residencial', 'residencial_remoto']))
    ].copy()
    
    print(f"   - Total de registros encontrados para o Piauí com os filtros: {len(df_filtrado)}")

    # --- 3. Processar e Agregar os Dados por Município ---
    print("\n🔄 Agregando o NÚMERO DE SISTEMAS por município...")
    
    dados_municipios = (
        df_filtrado.groupby('municipio')
        .agg(
            Numero_Sistemas=('n_sistemas', 'sum')
        )
        .reset_index()
    )

    dados_municipios = dados_municipios.sort_values(by='Numero_Sistemas', ascending=False)

    # --- 4. Salvar o Resultado ---
    dados_municipios.to_csv(caminho_saida, index=False, sep=';', encoding='utf-8-sig')

    print(f"\n✅ Arquivo '{arquivo_saida}' pronto para o mapa foi gerado com sucesso!")
    print("\n🏙️ Top 10 municípios por Número de Sistemas:")
    print(dados_municipios.head(10))

except FileNotFoundError:
    print(f"❌ ERRO: O arquivo '{arquivo_principal}' não foi encontrado.")
except KeyError as e:
    print(f"❌ ERRO de Chave (Coluna não encontrada): {e}")
    print("   Verifique se o nome da coluna na lista impressa acima corresponde ao nome usado no filtro.")
except Exception as e:
    print(f"⚠️ Erro inesperado: {e}")