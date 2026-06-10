"""
Módulo de Componentes Visuais Streamlit.

Funcionalidades:
- Painel de métricas (total, % concluído, % pendente, % N/A)
- Gráfico de barras por município (status empilhado)
- Tabela com formatação condicional (cores por status)
- Barra de progresso inline para evolução
- Paleta de cores por tipo de projeto

Cores:
- Captação: Azul (#1E6FE8)
- ETA: Verde (#2E9E5B)
- ETE: Laranja (#E87820)
- Status: Verde claro, Amarelo claro, Cinza claro
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)

# Paleta de cores por tipo de projeto
CORES_TIPO = {
    "Captação": "#1E6FE8",  # Azul
    "ETA": "#2E9E5B",       # Verde
    "ETE": "#E87820",       # Laranja
}

# Paleta de cores por status
CORES_STATUS = {
    "Concluído": "#2E9E5B",     # Verde
    "Pendente": "#FFA500",      # Laranja
    "Atrasado": "#E74C3C",      # Vermelho
    "N/A": "#95A5A6",           # Cinza
}

# Cores de fundo para formatacao condicional
CORES_BACKGROUND = {
    "Concluído": "#d4edda",     # Verde claro
    "Pendente": "#fff3cd",      # Amarelo claro
    "Atrasado": "#f8d7da",      # Vermelho claro
    "N/A": "#e2e3e5",           # Cinza claro
}


def calcular_metricas(df: pd.DataFrame) -> Tuple[int, float, float, float]:
    """
    Calcula métricas de progresso a partir do DataFrame.

    Args:
        df: DataFrame normalizado

    Returns:
        Tupla (total_itens, pct_concluido, pct_pendente, pct_na)
    """
    if df is None or len(df) == 0:
        return 0, 0.0, 0.0, 0.0

    total = len(df)

    # Contar status
    concluidos = (df["status_atual"] == "Concluído").sum()
    pendentes = (df["status_atual"] == "Pendente").sum()
    atrasados = (df["status_atual"] == "Atrasado").sum()
    na = (df["status_atual"].isna() | (df["status_atual"] == "N/A")).sum()

    # Calcular percentuais
    pct_concluido = (concluidos / total) * 100 if total > 0 else 0.0
    pct_pendente = (pendentes / total) * 100 if total > 0 else 0.0
    pct_atrasado = (atrasados / total) * 100 if total > 0 else 0.0
    pct_na = (na / total) * 100 if total > 0 else 0.0

    logger.info(
        f"Metricas: Total={total}, Concluido={pct_concluido:.1f}%, "
        f"Pendente={pct_pendente:.1f}%, Atrasado={pct_atrasado:.1f}%, N/A={pct_na:.1f}%"
    )

    return total, pct_concluido, pct_pendente, pct_na


def painel_metricas(df: pd.DataFrame, tipo_projeto: Optional[str] = None) -> None:
    """
    Exibe painel com 4 métricas principais de progresso.

    Métricas:
    - Total de itens
    - Percentual concluído
    - Percentual pendente
    - Percentual não aplicável

    Args:
        df: DataFrame filtrado com os dados
        tipo_projeto: Tipo do projeto (para cor da métrica)
    """
    try:
        total, pct_concluido, pct_pendente, pct_na = calcular_metricas(df)

        # Determinar cor primária
        cor_primaria = CORES_TIPO.get(tipo_projeto, "#1E6FE8") if tipo_projeto else "#1E6FE8"

        # Criar colunas para as 4 métricas com cards customizados
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            exibir_card_metrica(
                titulo="📊 Total",
                valor=str(int(total)),
                subtitulo="itens no sistema",
                cor=cor_primaria
            )

        with col2:
            exibir_card_metrica(
                titulo="✅ Concluído",
                valor=f"{pct_concluido:.0f}%",
                subtitulo="concluídos",
                cor="#2E9E5B"
            )

        with col3:
            exibir_card_metrica(
                titulo="⏳ Pendente",
                valor=f"{pct_pendente:.0f}%",
                subtitulo="pendentes",
                cor="#E87820"
            )

        with col4:
            exibir_card_metrica(
                titulo="➖ N/A",
                valor=f"{pct_na:.0f}%",
                subtitulo="não aplicáveis",
                cor="#95A5A6"
            )

    except Exception as e:
        logger.error(f"Erro ao exibir painel de métricas: {e}")
        st.error(f"Erro ao calcular métricas: {e}")


def grafico_barras_municipio(df: pd.DataFrame, tipo_projeto: Optional[str] = None) -> Optional[go.Figure]:
    """
    Cria gráfico de barras empilhadas (status por município).

    Estrutura:
    - Eixo X: Contagem de itens
    - Eixo Y: Município
    - Cores: Por status (Concluído, Pendente, Atrasado, N/A)
    - Tipo: Barras horizontais empilhadas

    Args:
        df: DataFrame filtrado
        tipo_projeto: Tipo do projeto (para título)

    Returns:
        Figura Plotly ou None se erro
    """
    try:
        if df is None or len(df) == 0:
            st.warning("Sem dados para exibir gráfico")
            return None

        # Preparar dados
        df_grafico = df.copy()

        # Limpar status nulos
        df_grafico["status_atual"] = df_grafico["status_atual"].fillna("N/A")

        # Agrupar por município e status
        grafico_dados = (
            df_grafico.groupby(["municipio", "status_atual"])
            .size()
            .reset_index(name="quantidade")
        )

        # Ordenar municípios por total de itens (decrescente)
        municipios_ordenados = (
            df_grafico.groupby("municipio").size().sort_values(ascending=True).index.tolist()
        )

        # Criar figura
        fig = px.bar(
            grafico_dados,
            x="quantidade",
            y="municipio",
            color="status_atual",
            color_discrete_map=CORES_STATUS,
            barmode="stack",
            orientation="h",
            title=f"Status por Município - {tipo_projeto or 'Dashboard'}",
            labels={"quantidade": "Itens", "municipio": "Município", "status_atual": "Status"},
            height=max(400, len(municipios_ordenados) * 20),
        )

        # Customizações
        fig.update_layout(
            xaxis_title="Número de Itens",
            yaxis_title="Município",
            legend_title="Status",
            hovermode="y unified",
            plot_bgcolor="rgba(240, 242, 246, 1)",
            paper_bgcolor="white",
            font=dict(size=11),
        )

        # Manter ordem de municípios
        fig.update_yaxes(categoryorder="array", categoryarray=municipios_ordenados)

        logger.info(f"Gráfico de municípios criado: {len(municipios_ordenados)} municípios")
        return fig

    except Exception as e:
        logger.error(f"Erro ao criar gráfico: {e}")
        st.error(f"Erro ao criar gráfico: {e}")
        return None


def tabela_formatada(
    df: pd.DataFrame,
    colunas_display: Optional[list] = None,
    altura_max: int = 400,
) -> Optional[pd.DataFrame]:
    """
    Exibe tabela com formatação condicional por status.

    Formatação:
    - Concluído: Fundo verde claro
    - Pendente: Fundo amarelo claro
    - Atrasado: Fundo vermelho claro
    - N/A: Fundo cinza claro

    Args:
        df: DataFrame com dados
        colunas_display: Colunas a exibir (None = todas)
        altura_max: Altura máxima da tabela em pixels

    Returns:
        DataFrame estilizado ou None se erro
    """
    try:
        if df is None or len(df) == 0:
            st.warning("Sem dados para exibir tabela")
            return None

        df_tabela = df.copy()

        # Selecionar colunas
        if colunas_display:
            colunas_validas = [col for col in colunas_display if col in df_tabela.columns]
            df_tabela = df_tabela[colunas_validas]

        # Função de estilo condicional
        def estilo_status(row):
            """Aplica cor de fundo baseado no status_atual."""
            status = row.get("status_atual", "N/A")

            if pd.isna(status):
                cor = CORES_BACKGROUND.get("N/A", "#e2e3e5")
            else:
                cor = CORES_BACKGROUND.get(status, "#ffffff")

            return [f"background-color: {cor}"] * len(row)

        # Aplicar estilo
        df_styled = df_tabela.style.apply(estilo_status, axis=1)
        df_styled = df_styled.format({
            "evolucao": "{:.1%}",
        }, na_rep="—")

        # Exibir com st.dataframe
        st.dataframe(
            df_styled,
            use_container_width=True,
            height=min(altura_max, len(df_tabela) * 35 + 100),
        )

        logger.info(f"Tabela exibida: {len(df_tabela)} linhas")
        return df_tabela

    except Exception as e:
        logger.error(f"Erro ao exibir tabela: {e}")
        st.error(f"Erro ao exibir tabela: {e}")
        return None


def barra_progresso_evolucao(valor: float, label: str = "Progresso") -> None:
    """
    Exibe barra de progresso com número para evolução parcial.

    Só exibe para valores 0 < evolucao < 1 (progresso parcial).
    Para 0 ou 1, exibe apenas o valor numérico.

    Args:
        valor: Float entre 0 e 1 (ou NaN)
        label: Rótulo da barra
    """
    try:
        if pd.isna(valor):
            st.text("N/A")
            return

        # Validar intervalo
        if not (0 <= valor <= 1):
            st.text(f"Valor inválido: {valor}")
            return

        if valor == 0 or valor == 1:
            # Apenas mostrar percentual
            st.text(f"{valor*100:.0f}%")
        else:
            # Mostrar barra + percentual
            col1, col2 = st.columns([4, 1])

            with col1:
                st.progress(valor)

            with col2:
                st.text(f"{valor*100:.0f}%")

    except Exception as e:
        logger.error(f"Erro ao exibir barra de progresso: {e}")
        st.text("Erro ao exibir")


def grafico_evolucao_tempo(
    historico: list,
    tipo_projeto: Optional[str] = None,
) -> Optional[go.Figure]:
    """
    Cria gráfico de evolução de progresso ao longo do tempo.

    Args:
        historico: Lista de entradas do histórico
        tipo_projeto: Tipo do projeto (para filtro)

    Returns:
        Figura Plotly ou None
    """
    try:
        if not historico or len(historico) == 0:
            return None

        # Filtrar por tipo se especificado
        df_hist = pd.DataFrame(historico)

        if "tipo" in df_hist.columns and tipo_projeto:
            df_hist = df_hist[df_hist["tipo"] == tipo_projeto]

        if len(df_hist) == 0:
            return None

        # Converter data_upload para datetime
        if "data_upload" in df_hist.columns:
            df_hist["data_upload"] = pd.to_datetime(
                df_hist["data_upload"], errors="coerce"
            )

        # Agrupar por data e contar alterações
        df_hist_dia = (
            df_hist.groupby(df_hist["data_upload"].dt.date)
            .size()
            .reset_index(name="alteracoes")
        )
        df_hist_dia.columns = ["data", "alteracoes"]

        # Criar gráfico
        fig = px.line(
            df_hist_dia,
            x="data",
            y="alteracoes",
            markers=True,
            title=f"Alterações ao Longo do Tempo - {tipo_projeto or 'Todos'}",
            labels={"data": "Data", "alteracoes": "Número de Alterações"},
            height=350,
        )

        fig.update_layout(
            hovermode="x unified",
            plot_bgcolor="rgba(240, 242, 246, 1)",
            paper_bgcolor="white",
        )

        logger.info(f"Gráfico de evolução criado: {len(df_hist_dia)} pontos")
        return fig

    except Exception as e:
        logger.error(f"Erro ao criar gráfico de evolução: {e}")
        return None


def exibir_card_metrica(
    titulo: str,
    valor: str,
    subtitulo: Optional[str] = None,
    cor: str = "#1E6FE8",
) -> None:
    """
    Exibe um card customizado com métrica.

    Args:
        titulo: Título do card
        valor: Valor principal (ex: "85%")
        subtitulo: Texto secundário (ex: "Concluído")
        cor: Cor em hex (padrão: azul)
    """
    try:
        # Card com design moderno e sombra
        html = f"""
        <div style="
            background: linear-gradient(135deg, {cor}10 0%, {cor}05 100%);
            border: 2px solid {cor}30;
            border-radius: 10px;
            padding: 18px;
            margin-bottom: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        ">
            <div style="
                font-size: 0.85em;
                font-weight: 600;
                color: {cor};
                margin-bottom: 8px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            ">{titulo}</div>
            <div style="
                font-size: 2em;
                font-weight: 700;
                color: #1A1A2E;
                margin-bottom: 4px;
                line-height: 1.2;
            ">{valor}</div>
            {f'<div style="font-size: 0.8em; color: #888; margin-top: 6px;">{subtitulo}</div>' if subtitulo else ''}
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

    except Exception as e:
        logger.error(f"Erro ao exibir card: {e}")


def criar_resumo_visual(df: pd.DataFrame, tipo_projeto: Optional[str] = None) -> None:
    """
    Cria um resumo visual completo com múltiplos componentes.

    Args:
        df: DataFrame com dados
        tipo_projeto: Tipo do projeto
    """
    try:
        if df is None or len(df) == 0:
            st.info("Nenhum dado disponível para exibir")
            return

        # Painel de métricas
        st.subheader("📊 Painel de Métricas")
        painel_metricas(df, tipo_projeto)

        # Gráfico
        st.subheader("📈 Status por Município")
        fig = grafico_barras_municipio(df, tipo_projeto)
        if fig:
            st.plotly_chart(fig, use_container_width=True)

        # Tabela
        st.subheader("📋 Detalhes")
        tabela_formatada(df)

    except Exception as e:
        logger.error(f"Erro ao criar resumo visual: {e}")
        st.error(f"Erro ao exibir resumo: {e}")
