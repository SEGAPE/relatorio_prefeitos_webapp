import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Download de Relatórios", layout="wide")

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Rawline:wght@300;400;600&display=swap');
        * {
            font-family: 'Rawline', sans-serif;
        }
        .stApp {
            background-color: white !important;
            color: black !important;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            align-items: center;
        }
        header[data-testid="stHeader"] {
            display: none !important;
        }
        .block-container {
            padding-top: 0.5rem !important;
        }
        .br-button {
            background-color: #1351B4;
            color: white;
            border-radius: 12px;
            padding: 8px 14px;
            font-weight: bold;
            font-size: 0.82rem;
            text-align: center;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border: none;
            cursor: pointer;
            width: 90px;
            line-height: 1.4;
            margin-top: 22px;
        }
        div[data-baseweb="select"] > div {
            background-color: #FFFFFF;
            border-color: #D3D3D3;
        }
        div[role="listbox"] ul {
            background-color: #FFFFFF;
        }
        div[role="listbox"] li {
            color: #000000;
        }
        div[role="listbox"] li:hover {
            background-color: #F0F0F0;
        }
        /* Forçar colunas lado a lado em qualquer largura */
        [data-testid="stHorizontalBlock"] > [data-testid="stVerticalBlockBorderWrapper"],
        [data-testid="stHorizontalBlock"] > div {
            min-width: 0 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def carregar_municipios():
    df = pd.read_csv("src/static/municipios.csv", dtype={"id_municipio": str})
    return df


@st.cache_data
def carregar_index_csv(caminho_csv):
    return pd.read_csv(caminho_csv)


def renderizar_aba_csv(csv_path, base_url, prefix):
    import os
    if not os.path.exists(csv_path):
        st.warning(f"Arquivo não encontrado: `{csv_path}`. Adicione o arquivo à pasta `src/static/`.")
        return
    df = carregar_index_csv(csv_path)

    ufs = sorted(df["uf"].dropna().unique())
    col_uf, col_mun, col_btn = st.columns([1, 2, 1])

    with col_uf:
        st.markdown("**Selecione UF**")
        uf_escolhida = st.selectbox(
            "",
            options=ufs,
            index=None,
            placeholder="Selecione a UF",
            key=f"uf_{prefix}",
            label_visibility="collapsed",
        )

    municipio_escolhido = None
    with col_mun:
        st.markdown("**Selecione o município**")
        municipios_uf = (
            df[df["uf"] == uf_escolhida]["municipio"].sort_values().tolist()
            if uf_escolhida else []
        )
        municipio_escolhido = st.selectbox(
            "",
            options=municipios_uf,
            index=None,
            placeholder="Digite aqui seu município",
            key=f"mun_{prefix}",
            label_visibility="collapsed",
            disabled=not uf_escolhida,
        )

    with col_btn:
        st.markdown("&nbsp;", unsafe_allow_html=True)
        if municipio_escolhido:
            linha = df[(df["uf"] == uf_escolhida) & (df["municipio"] == municipio_escolhido)].iloc[0]
            url = base_url + linha["caminho"]
            st.markdown(
                f'<a href="{url}" target="_blank"><button class="br-button">Baixar<br>Relatório</button></a>',
                unsafe_allow_html=True,
            )


def renderizar_aba_2024():
    municipios = carregar_municipios()

    ufs = sorted(municipios["sigla_uf"].dropna().unique())
    col_uf, col_mun, col_btn = st.columns([1, 2, 1])

    with col_uf:
        st.markdown("**Selecione UF**")
        uf_escolhida = st.selectbox(
            "",
            options=ufs,
            index=None,
            placeholder="Selecione a UF",
            key="uf_2024",
            label_visibility="collapsed",
        )

    municipio_escolhido = None
    with col_mun:
        st.markdown("**Selecione o município**")
        municipios_uf = (
            municipios[municipios["sigla_uf"] == uf_escolhida]["nome"]
            .sort_values()
            .tolist()
            if uf_escolhida else []
        )
        municipio_escolhido = st.selectbox(
            "",
            options=municipios_uf,
            index=None,
            placeholder="Digite aqui seu município",
            key="mun_2024",
            label_visibility="collapsed",
            disabled=not uf_escolhida,
        )

    with col_btn:
        st.markdown("&nbsp;", unsafe_allow_html=True)
        if municipio_escolhido:
            info = municipios[
                (municipios["nome"] == municipio_escolhido)
                & (municipios["sigla_uf"] == uf_escolhida)
            ].iloc[0]
            codigo_ibge = info["id_municipio"]
            nome_enc = urllib.parse.quote(info["nome"], safe="")
            uf = info["sigla_uf"]
            url = (
                f"https://storage.googleapis.com/br-mec-privado-relatorio-prefeitos/"
                f"relatorio_prefeitos/{uf}/{codigo_ibge}_{nome_enc}_{uf}.pdf.pdf"
            )
            st.markdown(
                f'<a href="{url}" target="_blank"><button class="br-button">Baixar<br>Relatório</button></a>',
                unsafe_allow_html=True,
            )


st.markdown("<p style='margin:0 0 4px 0; font-weight:600;'>Selecione o relatório</p>", unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["Relatório Educacional 2025", "Relatório Equidade Racial", "Relatório Educacional 2024"])

with tab1:
    renderizar_aba_csv(
        csv_path="src/static/atm_pdf_index_uf.csv",
        base_url="https://storage.googleapis.com/br-mec-privado-relatorio-prefeitos/atm_2026/",
        prefix="mec2025",
    )

with tab2:
    renderizar_aba_csv(
        csv_path="src/static/atm_eq_pdf_index_uf.csv",
        base_url="https://storage.googleapis.com/br-mec-privado-relatorio-prefeitos/atm-eq_052026/",
        prefix="eq2025",
    )

with tab3:
    renderizar_aba_2024()
