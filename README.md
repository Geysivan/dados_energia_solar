# Análise da Micro e Minigeração Distribuída (MMGD) Solar no Piauí

Este repositório contém os scripts Python, dados de entrada e resultados visuais (mapas) utilizados na análise da expansão da energia solar fotovoltaica (MMGD) no estado do Piauí, Brasil. O trabalho foi desenvolvido como suporte à seção de análise de dados do artigo acadêmico [**Inserir Título Provisório ou Final do Artigo Aqui**].

## CONTEXTO

O objetivo principal foi processar dados públicos de fontes como a Empresa de Pesquisa Energética (EPE) e o Instituto Brasileiro de Geografia e Estatística (IBGE) para gerar visualizações que ilustrassem:

1.  A distribuição espacial do número absoluto de sistemas MMGD solar no Piauí.
2.  A densidade desses sistemas em relação ao número de domicílios por município.

## ESTRUTURA DO REPOSITÓRIO

* **/ (Raiz)**: Contém os scripts Python, arquivos de dados geográficos (`.json`) e os mapas finais gerados (`.png`).
* **Arquivos de Dados Principais (Entrada):**
    * `capacidade_instalada.xlsx`: Base de dados da EPE com histórico de instalações e potência por município, classe, modalidade, etc. (Usado para gerar `dados_para_mapa.csv`).
    * `domicilios.xlsx`: Número de domicílios particulares permanentes por município (Fonte: IBGE Censo 2022). Usado para o cálculo de densidade.
    * `Energia_solar_sobre_total.xlsx`: Dados consolidados de geração solar e consumo total anual no Piauí (Fonte: EPE Anuário). Usado para calcular a participação.
    * `PI_Municipios_2022.json`: Arquivo GeoJSON com as geometrias dos municípios do Piauí (Fonte: IBGE).
    * `br_states.json`: Arquivo GeoJSON com as geometrias dos estados do Brasil (Fonte: IBGE/GitHub Luiz Pedone).
* **Scripts Python (`.py`):**
    * `analise_energia_solar_pi.py`: Lê `capacidade_instalada.xlsx`, aplica filtros relevantes (UF, fonte, classe residencial/rural, etc.) e gera o arquivo `dados_para_mapa.csv` com o número acumulado de sistemas por município.
    * `mapa_densidade.py`: Lê `dados_para_mapa.csv` e `domicilios.xlsx`, calcula a métrica de densidade (sistemas por 1.000 domicílios), junta com os dados geográficos de `PI_Municipios_2022.json` e `br_states.json`, e gera o mapa coroplético de densidade (`mapa_densidade_piaui_LINEAR_ticks_ajustados.png`) com escala linear e elementos cartográficos.
    * `criar_mapa_pi.py`: (Script original, gerou `mapa_publicacao_final.png`) Lê `dados_para_mapa.csv`, junta com os dados geográficos e gera o mapa coroplético do número absoluto de sistemas, utilizando escala logarítmica e elementos cartográficos. *Nota: Verificar se este script ainda é necessário ou se `mapa_densidade.py` o substituiu em funcionalidade.*
    * `percentual_solar.py`: Lê `Energia_solar_sobre_total.xlsx`, calcula a participação percentual da geração solar no consumo total anual e salva o resultado em `participacao_solar_consumo_pi.xlsx`.
    * *(Opcional: Incluir scripts de inspeção como `verificar_excel.py`, `verificar_filtros.py` se achar relevante)*
* **Resultados Gerados:**
    * `dados_para_mapa.csv`: Tabela intermediária com número de sistemas por município.
    * `participacao_solar_consumo_pi.xlsx`: Tabela com o cálculo da participação anual.
    * `mapa_publicacao_final.png`: Imagem do mapa de número absoluto de sistemas.
    * `mapa_densidade_piaui_LINEAR_ticks_ajustados.png`: Imagem do mapa de densidade de sistemas.

## REQUISITOS

Para executar os scripts Python, é necessário ter:

* Python 3.x
* Bibliotecas Python:
    * `pandas` (e `openpyxl` para ler Excel): `pip install pandas openpyxl`
    * `geopandas`: (Requer instalação cuidadosa dependendo do sistema operacional, veja a [documentação oficial](https://geopandas.org/en/stable/getting_started/install.html)) `pip install geopandas`
    * `matplotlib`: `pip install matplotlib`
    * `matplotlib-scalebar`: `pip install matplotlib-scalebar`

## COMO USAR

1.  Clone este repositório: `git clone https://www.youtube.com/watch?v=xtwls2XmJUI`
2.  Navegue até a pasta do projeto: `cd dados_energia_solar`
3.  Instale as bibliotecas listadas em "Requisitos".
4.  Certifique-se de que todos os arquivos de dados de entrada (`.xlsx`, `.json`) estão presentes na pasta.
5.  Execute os scripts desejados a partir do terminal. Exemplo:
    ```bash
    python analise_energia_solar_pi.py
    python mapa_densidade.py
    python percentual_solar.py
    ```
6.  Os arquivos de resultado (`.csv`, `.xlsx`, `.png`) serão gerados ou atualizados na mesma pasta.

## AUTORES

* **[Geysivan C S]** - Análise de dados e desenvolvimento dos scripts.
* **Pedro Henrique** - Idealização, referencial teórico do artigo.
