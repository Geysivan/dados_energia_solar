import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import os
# LogNorm não é mais necessário aqui
from matplotlib.ticker import ScalarFormatter
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib_scalebar.scalebar import ScaleBar

# --- 1. Configuração dos Arquivos ---
pasta_dados = os.path.dirname(os.path.abspath(__file__))
arquivo_dados_sistemas = "dados_para_mapa.csv"
arquivo_domicilios = "domicilios.xlsx"
arquivo_mapa_pi = "PI_Municipios_2022.json"
arquivo_brasil = "br_states.json"
# Novo nome para distinguir do mapa logarítmico
arquivo_mapa_saida = "mapa_densidade_piaui.png" 

caminho_dados_sistemas = os.path.join(pasta_dados, arquivo_dados_sistemas)
caminho_domicilios = os.path.join(pasta_dados, arquivo_domicilios)
caminho_mapa_pi = os.path.join(pasta_dados, arquivo_mapa_pi)
caminho_brasil = os.path.join(pasta_dados, arquivo_brasil)
caminho_mapa_saida = os.path.join(pasta_dados, arquivo_mapa_saida)

# --- 2. Carregar e Preparar os Dados ---
try:
    print("🌍 Carregando dados geoespaciais e de sistemas...")
    mapa_pi = gpd.read_file(caminho_mapa_pi)
    br_estados = gpd.read_file(caminho_brasil)
    dados_sistemas = pd.read_csv(caminho_dados_sistemas, sep=';')

    print("🏠 Carregando dados de domicílios do IBGE...")
    df_domicilios = pd.read_excel(caminho_domicilios, header=0)
    df_domicilios.columns = df_domicilios.columns.str.strip()
    df_domicilios.rename(columns={
        'Municípios': 'municipio',
        'Domicílios particulares permanentes - Domicílios': 'total_domicilios'
    }, inplace=True)
    df_domicilios['total_domicilios'] = df_domicilios['total_domicilios'].astype(str).str.replace('.', '', regex=False)
    df_domicilios['total_domicilios'] = pd.to_numeric(df_domicilios['total_domicilios'], errors='coerce')
    df_domicilios = df_domicilios[['municipio', 'total_domicilios']]

    # --- 3. Juntar Dados e Calcular a DENSIDADE ---
    print("🔄 Juntando dados e calculando densidade...")
    dados_sistemas['municipio'] = dados_sistemas['municipio'].str.title()
    df_domicilios['municipio'] = df_domicilios['municipio'].str.title()
    dados_completos = pd.merge(dados_sistemas, df_domicilios, on='municipio', how='left')
    dados_completos['Densidade'] = (dados_completos['Numero_Sistemas'] / dados_completos['total_domicilios']) * 1000
    dados_completos['Densidade'] = dados_completos['Densidade'].fillna(0)
    
    mapa_pi['name'] = mapa_pi['name'].str.title()
    mapa_completo_pi = mapa_pi.merge(dados_completos, left_on='name', right_on='municipio', how='left')
    mapa_completo_pi['Densidade'] = mapa_completo_pi['Densidade'].fillna(0)

    # Diagnóstico
    min_dens = mapa_completo_pi[mapa_completo_pi['Densidade'] > 0]['Densidade'].min()
    max_dens = mapa_completo_pi['Densidade'].max()
    print(f"📊 Densidade Mínima (maior que zero): {min_dens:.2f}")
    print(f"📊 Densidade Máxima: {max_dens:.2f}")

    # --- 4. Gerar o Mapa de DENSIDADE com ESCALA LINEAR ---
    print("🎨 Gerando o mapa de DENSIDADE com escala LINEAR...")
    fig, ax = plt.subplots(1, 1, figsize=(15, 15))

    br_estados.plot(ax=ax, color="#E7E3E3", edgecolor='white', linewidth=0.7)
    
    # Base azul clara para todos os municípios
    mapa_completo_pi.plot(ax=ax, color='#cce6ff', edgecolor='0.8', linewidth=0.3)
    
    # Plotando os dados com escala linear (sem LogNorm)
    mapa_completo_pi.plot(
        column='Densidade', 
        cmap='Blues', 
        ax=ax, 
        edgecolor='0.8', 
        linewidth=0.3,
        # vmin=0 garante que a escala comece no zero
        vmin=0, vmax=max_dens, 
        legend=False
    )
    
    # --- 5. Criar a Legenda LINEAR ---
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("bottom", size="4%", pad="5%")
    formatter = ScalarFormatter()
    formatter.set_scientific(False)
    
    # <<< AJUSTE AQUI: Removido o LogNorm da ScalarMappable >>>
    sm = plt.cm.ScalarMappable(cmap='Blues', norm=plt.Normalize(vmin=0, vmax=max_dens))
    
    # Define os ticks manualmente para a escala linear (ajuste se necessário)
    ticks_legenda_linear = [0, round(max_dens/4.1),40, round(max_dens*3/4.1), 80] 
    
    fig.colorbar(sm, cax=cax, orientation='horizontal', format=formatter, ticks=ticks_legenda_linear) 
    cax.set_xlabel("Sistemas por 1.000 Domicílios", fontsize=12)

    # --- 6 a 9: O resto do código permanece igual ---
    minx, miny, maxx, maxy = mapa_pi.total_bounds
    ax.set_xlim(minx - 1, maxx + 1)
    ax.set_ylim(miny - 1, maxy + 1)
    ax.set_title('Densidade de Sistemas de Geração Solar por Município no Piauí', fontdict={'fontsize': '20', 'fontweight': '3'}, pad=20) # Título ajustado
    ax.set_axis_off()
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_edgecolor('black')
        spine.set_linewidth(1.5)

    scalebar = ScaleBar(111.32, 'km', length_fraction=0.25, location='lower left', pad=0.5,
                        frameon=False, font_properties={'size': 12})
    ax.add_artist(scalebar)

    ax_inset = inset_axes(ax, width="25%", height="25%", loc='upper left', borderpad=2)
    br_estados.plot(ax=ax_inset, color='lightgray', edgecolor='white', linewidth=0.3)
    br_estados[br_estados['ESTADO'] == 'Piauí'].plot(ax=ax_inset, color='#003366', edgecolor='white')
    ax_inset.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
    for spine in ax_inset.spines.values():
        spine.set_visible(True)
        spine.set_edgecolor('black')
        spine.set_linewidth(1)

    fig.text(0.77, 0.18, 
             'Fonte: EPE (2025); IBGE (2022)\nElaboração: CIETE/SEPLAN (2025)', 
             ha='right', va='bottom', fontsize=10, style='italic')

    plt.savefig(caminho_mapa_saida, dpi=300, bbox_inches='tight')
    print(f"\n✅ Mapa de DENSIDADE (LINEAR) salvo com sucesso como '{arquivo_mapa_saida}'!")

except FileNotFoundError as e:
    print(f"❌ ERRO: Arquivo não encontrado! {e.filename}")
except KeyError as e:
    print(f"❌ ERRO de Chave (Coluna não encontrada): {e}")   
except Exception as e:
    print(f"⚠️ Erro inesperado: {e}")