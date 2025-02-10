import streamlit as st
import pandas as pd
import urllib.parse
import requests

# Configuração da página
st.set_page_config(page_title="Download de Relatórios", layout="centered")

# Aplicar estilo da fonte Rawline
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Rawline:wght@300;400;600&display=swap');
        * {
            font-family: 'Rawline', sans-serif;
        }
        .br-button {
            --button-radius: 100em;
            --button-medium: 40px;
            --button-size: var(--button-medium);
            background-color: #1351B4;
            color: white;
            border-radius: var(--button-radius);
            padding: 10px 20px;
            font-weight: bold;
            text-align: center;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border: none;
            cursor: pointer;
            height: var(--button-size);
            width: auto;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# Carregar lista de municípios a partir do arquivo local
@st.cache_data
def carregar_municipios():
    df = pd.read_csv("municipios.csv", dtype={"id_municipio": str})
    df["nome_completo"] = df["nome"] + " - " + df["sigla_uf"]
    return df


municipios = carregar_municipios()

# Criar dropdown para seleção do município
municipio_escolhido = st.selectbox(
    "Selecione o município:", municipios["nome_completo"]
)

# Buscar código IBGE e UF correspondente
if municipio_escolhido:
    municipio_info = municipios[
        municipios["nome_completo"] == municipio_escolhido
    ].iloc[0]
    codigo_ibge = municipio_info["id_municipio"]
    nome_municipio = urllib.parse.quote(municipio_info["nome"], safe="")
    uf = municipio_info["sigla_uf"]

    # Montar a URL do relatório no formato correto
    url_relatorio = f"https://storage.googleapis.com/br-mec-privado-relatorio-prefeitos/relatorio_prefeitos/{uf}/{codigo_ibge}_{nome_municipio}_{uf}.pdf.pdf"

    # Verificar se o arquivo existe
    response = requests.head(url_relatorio)
    if response.status_code == 200:
        st.markdown(
            f'<a href="{url_relatorio}" target="_blank"><button class="br-button">Baixar Relatório</button></a>',
            unsafe_allow_html=True,
        )
    else:
        st.error("Relatório não encontrado para este município.")
