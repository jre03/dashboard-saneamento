"""
Módulo de Componentes Visuais — Paleta Biancade.

Paleta aprovada:
  #000000 — Preto Principal (textos)
  #8C8C8C — Cinza Neutro (secundário, bordas)
  #917952 — Marrom Terroso Claro (acentos, botões)
  #423725 — Marrom Terroso Escuro (headers, badges)
  #FFFFFF — Branco (fundo)
  #F5F2EE — Fundo sidebar / cards
  #E0D9CF — Bordas
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)

# Paleta Biancade
COR_ESCURO   = "#423725"
COR_CLARO    = "#917952"
COR_CINZA    = "#8C8C8C"
COR_FUNDO    = "#F5F2EE"
COR_BORDA    = "#E0D9CF"

# Cores de fundo por status (tabela)
FUNDO_STATUS = {
    "Concluído": "#F0EDE6",
    "Pendente":  "#FDFBF8",
    "N/A":       "#F8F8F8",
}


# ---------------------------------------------------------------------------
# Cartões de métricas
# ---------------------------------------------------------------------------

def cartoes_metricas(df: pd.DataFrame) -> None:
    """Exibe 3 cartões: % Concluído, % Pendente, % N/A — paleta Biancade."""
    if df is None or len(df) == 0:
        st.info("Nenhum dado para exibir métricas.")
        return

    total = len(df)
    concluidos = (df["evolucao"] == 1.0).sum()
    pendentes  = (df["evolucao"] == 0.0).sum()
    na         = df["evolucao"].isna().sum()

    pct_c = concluidos / total * 100 if total else 0
    pct_p = pendentes  / total * 100 if total else 0
    pct_n = na         / total * 100 if total else 0

    col1, col2, col3 = st.columns(3)

    for col, titulo, valor, acento in [
        (col1, "Concluído", pct_c, COR_ESCURO),
        (col2, "Pendente",  pct_p, COR_CLARO),
        (col3, "N/A",       pct_n, COR_CINZA),
    ]:
        with col:
            st.markdown(
                f"""
                <div style="
                    background:{COR_FUNDO};
                    border-left:4px solid {acento};
                    border-radius:6px;
                    padding:16px 18px;
                    margin-bottom:8px;
                ">
                    <div style="font-size:0.8em;color:{acento};font-weight:600;
                                text-transform:uppercase;letter-spacing:0.5px;">
                        {titulo}
                    </div>
                    <div style="font-size:2em;font-weight:700;color:#000000;line-height:1.2;">
                        {valor:.0f}%
                    </div>
                    <div style="font-size:0.78em;color:{COR_CINZA};margin-top:4px;">
                        {int(concluidos if titulo=='Concluído' else (pendentes if titulo=='Pendente' else na))} de {total} itens
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ---------------------------------------------------------------------------
# Tabela com filtros inline por coluna
# ---------------------------------------------------------------------------

def tabela_com_filtros(df: pd.DataFrame, chave_estado: str = "filtros") -> pd.DataFrame:
    """
    Exibe filtros inline por coluna e tabela filtrada.

    Filtros:
    - Texto (municipio, atividade, responsavel, plano_de_acao): text_input busca parcial
    - status_atual: selectbox com opções dos dados
    - evolucao: range 0–100%
    - Datas: date_input de/até

    Todos cumulativos (AND). Resultado propagado via retorno e session_state.filtros_ativos.
    """
    if df is None or len(df) == 0:
        st.warning("Nenhum dado para exibir.")
        return pd.DataFrame()

    st.markdown(
        f"<div style='font-size:0.8em;color:{COR_CINZA};margin-bottom:6px;'>"
        "Filtros — todos cumulativos (AND)</div>",
        unsafe_allow_html=True,
    )

    # --- linha de filtros de texto ---
    col_t1, col_t2, col_t3, col_t4 = st.columns(4)
    f_municipio   = col_t1.text_input("Município",    key=f"{chave_estado}_mun",  placeholder="buscar…")
    f_atividade   = col_t2.text_input("Atividade",    key=f"{chave_estado}_atv",  placeholder="buscar…")
    f_responsavel = col_t3.text_input("Responsável",  key=f"{chave_estado}_resp", placeholder="buscar…")
    f_plano       = col_t4.text_input("Plano de Ação",key=f"{chave_estado}_plano",placeholder="buscar…")

    # --- linha de filtros estruturados ---
    col_s1, col_s2, col_s3, col_s4, col_s5 = st.columns(5)

    status_opcoes = ["(todos)"] + sorted(df["status_atual"].dropna().unique().tolist())
    f_status = col_s1.selectbox("Status", status_opcoes, key=f"{chave_estado}_status")

    f_evol_min = col_s2.number_input("Evolução mín %", 0, 100, 0,  step=5, key=f"{chave_estado}_evmin")
    f_evol_max = col_s3.number_input("Evolução máx %", 0, 100, 100, step=5, key=f"{chave_estado}_evmax")

    datas_validas = df["data_entrega_final"].dropna()
    if len(datas_validas) > 0:
        data_min = pd.Timestamp(datas_validas.min()).date()
        data_max = pd.Timestamp(datas_validas.max()).date()
        f_data_ini = col_s4.date_input("Data de (entrega)", value=data_min, key=f"{chave_estado}_dini")
        f_data_fim = col_s5.date_input("Data até",          value=data_max, key=f"{chave_estado}_dfim")
    else:
        f_data_ini = None
        f_data_fim = None

    # --- aplicar filtros ---
    df_f = df.copy()

    if f_municipio:
        df_f = df_f[df_f["municipio"].fillna("").str.contains(f_municipio, case=False, na=False)]
    if f_atividade:
        df_f = df_f[df_f["atividade"].fillna("").str.contains(f_atividade, case=False, na=False)]
    if f_responsavel:
        df_f = df_f[df_f["responsavel"].fillna("").str.contains(f_responsavel, case=False, na=False)]
    if f_plano:
        df_f = df_f[df_f["plano_de_acao"].fillna("").str.contains(f_plano, case=False, na=False)]
    if f_status != "(todos)":
        df_f = df_f[df_f["status_atual"] == f_status]

    # evolucao range
    df_f = df_f[
        df_f["evolucao"].isna() |
        ((df_f["evolucao"] * 100 >= f_evol_min) & (df_f["evolucao"] * 100 <= f_evol_max))
    ]

    if f_data_ini and f_data_fim:
        datas = pd.to_datetime(df_f["data_entrega_final"], errors="coerce")
        mascara_data = (
            datas.isna() |
            ((datas.dt.date >= f_data_ini) & (datas.dt.date <= f_data_fim))
        )
        df_f = df_f[mascara_data]

    # salvar filtros ativos no session_state
    filtros = {}
    if f_municipio:   filtros["municipio"]   = f_municipio
    if f_atividade:   filtros["atividade"]   = f_atividade
    if f_responsavel: filtros["responsavel"] = f_responsavel
    if f_plano:       filtros["plano"]       = f_plano
    if f_status != "(todos)": filtros["status"] = f_status
    st.session_state.filtros_ativos = filtros

    # --- exibir contagem ---
    st.caption(f"{len(df_f)} de {len(df)} itens exibidos")

    # --- formatação de cores por status ---
    def colorir_linha(row):
        status = row.get("status_atual", "")
        cor = FUNDO_STATUS.get(status, "#FFFFFF")
        return [f"background-color:{cor}"] * len(row)

    # Colunas para exibir
    colunas_exibir = [c for c in [
        "municipio_filtro", "municipio", "unidade", "atividade",
        "responsavel", "plano_de_acao", "evolucao",
        "status_atual", "data_entrega_final", "data_estimada", "data_conclusao",
    ] if c in df_f.columns]

    df_display = df_f[colunas_exibir].copy()

    try:
        styled = (
            df_display.style
            .apply(colorir_linha, axis=1)
            .format({"evolucao": lambda v: f"{v*100:.0f}%" if pd.notna(v) else "—"})
        )
        st.dataframe(styled, use_container_width=True, height=420)
    except Exception:
        st.dataframe(df_display, use_container_width=True, height=420)

    return df_f


# ---------------------------------------------------------------------------
# Feed — resumo e linhas
# ---------------------------------------------------------------------------

def resumo_feed(modo: str, dados: Dict[str, Any]) -> None:
    """
    Exibe bloco de resumo textual no feed.

    modo: "versao" | "comparacao"
    dados: dict com campos relevantes (texto, contagens, etc.)
    """
    cor_borda = COR_ESCURO if modo == "versao" else COR_CLARO
    texto     = dados.get("texto", "")

    st.markdown(
        f"""
        <div style="
            border-left:4px solid {cor_borda};
            background:{COR_FUNDO};
            border-radius:0 6px 6px 0;
            padding:12px 16px;
            margin-bottom:12px;
            font-size:0.92em;
            color:#000000;
        ">{texto}</div>
        """,
        unsafe_allow_html=True,
    )


def linha_feed(entrada: Dict[str, Any]) -> None:
    """Exibe uma entrada do histórico formatada."""
    data_str = entrada.get("data_upload", "")
    try:
        data_fmt = pd.to_datetime(data_str).strftime("%d/%m/%Y %H:%M")
    except Exception:
        data_fmt = str(data_str)[:10]

    tipo     = entrada.get("tipo", "")
    mun      = entrada.get("municipio_filtro") or entrada.get("municipio", "")
    unidade  = entrada.get("unidade", "")
    atividade = entrada.get("atividade", "")
    campo    = entrada.get("campo", "")
    antes    = entrada.get("antes", "")
    depois   = entrada.get("depois", "")

    localizacao = f"{mun} / {unidade}" if unidade else mun

    mudanca = f"{campo}: {antes} → {depois}" if campo and antes and depois else entrada.get("texto", "")

    st.markdown(
        f"""
        <div style="
            border-left:3px solid {COR_BORDA};
            padding:8px 12px;
            margin-bottom:6px;
            font-size:0.85em;
        ">
            <span style="color:{COR_CINZA};">{data_fmt}</span>
            <span style="
                background:{COR_FUNDO};border:1px solid {COR_BORDA};
                border-radius:3px;padding:1px 6px;margin:0 6px;
                font-size:0.85em;color:{COR_ESCURO};font-weight:600;
            ">{tipo}</span>
            <strong>{localizacao}</strong> — {atividade}<br>
            <span style="color:{COR_CINZA};margin-left:8px;">{mudanca}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
