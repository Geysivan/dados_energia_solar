import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.colors import LogNorm
from matplotlib.ticker import ScalarFormatter
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
# Importa a biblioteca da barra de escala
from matplotlib_scalebar.scalebar import ScaleBar

# --- 1. Configuração dos Arquivos ---
pasta_dados = os.path.dirname(os.path.abspath(__file__))
arquivo_dados_mapa = "dados_para_mapa.csv"
caminho_dados_mapa = os.path.join(pasta_dados, arquivo_dados_mapa)
arquivo_mapa_pi = "PI_Municipios_2022.json"
caminho_mapa_pi = os.path.join(pasta_dados, arquivo_mapa_pi)
arquivo_brasil = "br_states.json"
caminho_brasil = os.path.join(pasta_dados, arquivo_brasil)
arquivo_mapa_saida = "mapa_publicacao_final.png" # Novo nome para a versão final
caminho_mapa_saida = os.path.join(pasta_dados, arquivo_mapa_saida)

# --- 2. Carregar os Dados ---
try:
    print("🌍 Carregando dados geoespaciais...")
    mapa_pi = gpd.read_file(caminho_mapa_pi)
    br_estados = gpd.read_file(caminho_brasil)
    dados_sistemas = pd.read_csv(caminho_dados_mapa, sep=';')

    # --- 3. Preparar e Juntar os Dados ---
    mapa_pi['name'] = mapa_pi['name'].str.title()
    dados_sistemas['municipio'] = dados_sistemas['municipio'].str.title()
    mapa_completo_pi = mapa_pi.merge(
        dados_sistemas, left_on='name', right_on='municipio', how='left'
    )
    mapa_completo_pi['Numero_Sistemas'] = mapa_completo_pi['Numero_Sistemas'].fillna(0)

    # --- 4. Gerar o Mapa Principal ---
    print("🎨 Gerando o mapa final com todos os elementos cartográficos...")
    fig, ax = plt.subplots(1, 1, figsize=(15, 15))

    br_estados.plot(ax=ax, color='#e9e9e9', edgecolor='white', linewidth=0.7)
    mapa_com_sistemas = mapa_completo_pi[mapa_completo_pi['Numero_Sistemas'] > 0]
    mapa_completo_pi.plot(ax=ax, color='#cce6ff', edgecolor='0.8', linewidth=0.3)
    mapa_com_sistemas.plot(
        column='Numero_Sistemas', cmap='Blues', ax=ax, edgecolor='0.8', linewidth=0.3,
        norm=LogNorm(vmin=1, vmax=mapa_com_sistemas['Numero_Sistemas'].max()),
        legend=False
    )
    
    # --- 5. Criar a Legenda ---
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("bottom", size="4%", pad="5%")
    formatter = ScalarFormatter()
    formatter.set_scientific(False)
    sm = plt.cm.ScalarMappable(cmap='Blues', norm=LogNorm(vmin=1, vmax=mapa_com_sistemas['Numero_Sistemas'].max()))
    fig.colorbar(sm, cax=cax, orientation='horizontal', format=formatter)
    cax.set_xlabel("Número de Sistemas de Geração", fontsize=12)

    # --- 6. Ajustar Enquadramento e Título ---
    minx, miny, maxx, maxy = mapa_pi.total_bounds
    ax.set_xlim(minx - 1, maxx + 1)
    ax.set_ylim(miny - 1, maxy + 1)
    ax.set_title('Número de Sistemas de Geração Solar por Município no Piauí', fontdict={'fontsize': '20', 'fontweight': '3'}, pad=20)
    ax.set_axis_off()
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_edgecolor('black')
        spine.set_linewidth(1.5)

    # --- 7. Adicionar Elementos Cartográficos Finais ---
    # Adiciona a Seta Norte
    #ax.text(0.95, 0.98, 'N\n▲', transform=ax.transAxes, fontsize=20,
    #        verticalalignment='top', horizontalalignment='center', fontweight='bold')

    # Adiciona a Barra de Escala Gráfica
    # (111.32 é a conversão aproximada de graus para km no equador)
    scalebar = ScaleBar(111.32, 'km', length_fraction=0.25, location='lower left', pad=0.5,
                        frameon=False, font_properties={'size': 12})
    ax.add_artist(scalebar)

    # Adiciona a Caixa de Localização (Inset)
    ax_inset = inset_axes(ax, width="25%", height="25%", loc='upper left', borderpad=2)
    br_estados.plot(ax=ax_inset, color='lightgray', edgecolor='white', linewidth=0.3)
    br_estados[br_estados['ESTADO'] == 'Piauí'].plot(ax=ax_inset, color='#003366', edgecolor='white')
    ax_inset.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
    for spine in ax_inset.spines.values():
        spine.set_visible(True)
        spine.set_edgecolor('black')
        spine.set_linewidth(1)

    # --- 8. Adicionar Fonte e Elaboração ---
    # Adiciona o texto no canto inferior direito da figura
    fig.text(0.77, 0.18, 
             'Fonte: EPE (2025); IBGE (2022)\nElaboração: CIETE/SEPLAN (2025)', 
             ha='right', va='bottom', fontsize=10, style='italic')

    # --- 9. Salvar o Mapa Final ---
    plt.savefig(arquivo_mapa_saida, dpi=300, bbox_inches='tight')
    print(f"\n✅ Mapa final com todos os elementos salvo com sucesso como '{arquivo_mapa_saida}'!")

except FileNotFoundError as e:
    print(f"❌ ERRO: Arquivo não encontrado! {e.filename}")
except Exception as e:
    print(f"⚠️ Erro inesperado: {e}")