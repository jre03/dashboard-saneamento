"""
Módulo de Comparação entre Versões de Planilhas.

Funcionalidades:
- Comparação entre duas versões de um mesmo tipo de projeto
- Identificação de itens alterados, adicionados e removidos
- Geração de descrição textual das alterações
- Merge por chave única (combinação de colunas)

Merge keys por tipo:
- Captações: [municipio_filtro, municipio, atividade, plano_de_acao]
- ETAs: [municipio_filtro, municipio, atividade, plano_de_acao]
- ETEs: [municipio_filtro, municipio, unidade, atividade, plano_de_acao]

Campos monitorados para diff:
- evolucao, status_atual, data_entrega_final, data_estimada, data_conclusao
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Chaves de merge por tipo
MERGE_KEYS = {
    "ETA": ["municipio_filtro", "municipio", "atividade", "plano_de_acao"],
    "Captação": ["municipio_filtro", "municipio", "atividade", "plano_de_acao"],
    "ETE": ["municipio_filtro", "municipio", "unidade", "atividade", "plano_de_acao"],
}

# Campos a monitorar para alterações
CAMPOS_MONITOR = [
    "evolucao",
    "status_atual",
    "data_entrega_final",
    "data_estimada",
    "data_conclusao",
    "responsavel",
]


def _formatar_valor(valor: Any) -> str:
    """
    Formata valor para exibição no histórico.

    Args:
        valor: Valor a formatar

    Returns:
        String formatada ou "N/A"
    """
    if pd.isna(valor) or valor is None:
        return "N/A"
    elif isinstance(valor, float):
        if 0 <= valor <= 1:
            return f"{valor*100:.0f}%"
        return f"{valor:.2f}"
    elif isinstance(valor, datetime):
        return valor.strftime("%d/%m/%Y")
    else:
        return str(valor)


def _criar_chave(row: pd.Series, tipo: str) -> str:
    """
    Cria chave única para um item baseado no tipo.

    Args:
        row: Linha do DataFrame
        tipo: "ETA" | "Captação" | "ETE"

    Returns:
        String com chave única (separada por |)
    """
    keys = MERGE_KEYS.get(tipo, [])
    valores = [str(row.get(k, "")) for k in keys]
    return "|".join(valores)


def comparar_versoes(
    df_v1: pd.DataFrame,
    df_v2: pd.DataFrame,
    tipo: str,
) -> Dict[str, Any]:
    """
    Compara duas versões de um tipo de projeto e retorna diff estruturado.

    Estrutura do retorno:
    {
        "alterados": [
            {
                "chave": "...",
                "municipio": "...",
                "atividade": "...",
                "alteracoes": [
                    {
                        "campo": "status_atual",
                        "antes": "Pendente",
                        "depois": "Concluído"
                    },
                    ...
                ]
            },
            ...
        ],
        "adicionados": [
            {"municipio": "...", "atividade": "...", ...},
            ...
        ],
        "removidos": [
            {"municipio": "...", "atividade": "...", ...},
            ...
        ]
    }

    Args:
        df_v1: DataFrame da versão anterior (normalizado)
        df_v2: DataFrame da versão atual (normalizado)
        tipo: "ETA" | "Captação" | "ETE"

    Returns:
        Dict com estrutura de diff
    """
    try:
        if df_v1 is None or df_v2 is None:
            return {"alterados": [], "adicionados": [], "removidos": []}

        if len(df_v1) == 0 or len(df_v2) == 0:
            return {"alterados": [], "adicionados": [], "removidos": []}

        # Copiar dataframes para não modificar originals
        df_v1 = df_v1.copy()
        df_v2 = df_v2.copy()

        # Criar chaves únicas
        df_v1["__chave__"] = df_v1.apply(lambda row: _criar_chave(row, tipo), axis=1)
        df_v2["__chave__"] = df_v2.apply(lambda row: _criar_chave(row, tipo), axis=1)

        # Merge outer para comparar
        df_merged = df_v1[["__chave__", "municipio", "unidade", "atividade"] + CAMPOS_MONITOR].merge(
            df_v2[["__chave__", "municipio", "unidade", "atividade"] + CAMPOS_MONITOR],
            on="__chave__",
            how="outer",
            suffixes=("_v1", "_v2"),
        )

        alterados = []
        adicionados = []
        removidos = []

        # Iterar sobre merged
        for _, row in df_merged.iterrows():
            chave = row["__chave__"]

            # Verificar se foi adicionado (só em v2)
            if pd.isna(row.get("status_atual_v1")):
                adicionados.append({
                    "chave": chave,
                    "municipio": row["municipio_v2"],
                    "unidade": row.get("unidade_v2"),
                    "atividade": row["atividade_v2"],
                    "status_atual": row["status_atual_v2"],
                    "evolucao": row.get("evolucao_v2"),
                })
                continue

            # Verificar se foi removido (só em v1)
            if pd.isna(row.get("status_atual_v2")):
                removidos.append({
                    "chave": chave,
                    "municipio": row["municipio_v1"],
                    "unidade": row.get("unidade_v1"),
                    "atividade": row["atividade_v1"],
                    "status_atual": row["status_atual_v1"],
                    "evolucao": row.get("evolucao_v1"),
                })
                continue

            # Verificar se foi alterado
            alteracoes = []
            for campo in CAMPOS_MONITOR:
                col_v1 = f"{campo}_v1"
                col_v2 = f"{campo}_v2"

                if col_v1 not in row.index or col_v2 not in row.index:
                    continue

                val_v1 = row[col_v1]
                val_v2 = row[col_v2]

                # Comparar (tratando NaN)
                if pd.isna(val_v1) and pd.isna(val_v2):
                    continue
                elif pd.isna(val_v1) or pd.isna(val_v2):
                    alteracoes.append({
                        "campo": campo,
                        "antes": _formatar_valor(val_v1),
                        "depois": _formatar_valor(val_v2),
                    })
                elif val_v1 != val_v2:
                    alteracoes.append({
                        "campo": campo,
                        "antes": _formatar_valor(val_v1),
                        "depois": _formatar_valor(val_v2),
                    })

            if alteracoes:
                alterados.append({
                    "chave": chave,
                    "municipio": row["municipio_v2"],
                    "unidade": row.get("unidade_v2"),
                    "atividade": row["atividade_v2"],
                    "alteracoes": alteracoes,
                })

        logger.info(
            f"Comparacao concluida: {len(alterados)} alterados, "
            f"{len(adicionados)} adicionados, {len(removidos)} removidos"
        )

        return {
            "alterados": alterados,
            "adicionados": adicionados,
            "removidos": removidos,
        }

    except Exception as e:
        logger.error(f"Erro ao comparar versoes: {e}")
        return {"alterados": [], "adicionados": [], "removidos": []}


def gerar_texto_historico(
    diff_item: Dict[str, Any],
    tipo: str,
    municipio: Optional[str] = None,
    unidade: Optional[str] = None,
) -> str:
    """
    Gera descrição textual de uma alteração.

    Exemplo de saída:
    "[ETA] MATRIZ DE CAMARAGIBE — Projeto Hidráulico: Status alterou de Pendente para Concluído"
    "[ETE] COLÔNIA LEOPOLDINA / ETE Colônia Leopoldina — Orçamentos: Evolução alterou de 0% para 80%"

    Args:
        diff_item: Entrada do diff (alterado, adicionado ou removido)
        tipo: "ETA" | "Captação" | "ETE"
        municipio: Município (override)
        unidade: Unidade (override, apenas ETEs)

    Returns:
        String legível com descrição da alteração
    """
    try:
        municipio = municipio or diff_item.get("municipio", "")
        atividade = diff_item.get("atividade", "")
        unidade = unidade or diff_item.get("unidade")

        # Construir prefixo com localização
        if tipo == "ETE" and unidade:
            localizacao = f"{municipio} / {unidade}"
        else:
            localizacao = municipio

        # Construir descrição da mudança
        if "alteracoes" in diff_item:
            # Item alterado
            alteracoes_texto = []
            for alt in diff_item["alteracoes"]:
                campo = alt["campo"]
                antes = alt["antes"]
                depois = alt["depois"]
                alteracoes_texto.append(
                    f"{campo.replace('_', ' ').capitalize()}: {antes} → {depois}"
                )

            mudanca = ", ".join(alteracoes_texto)
        elif diff_item.get("status_atual"):
            # Item adicionado ou removido
            mudanca = f"Status: {diff_item['status_atual']}"
        else:
            mudanca = "Alteração"

        # Montar texto final
        texto = f"[{tipo}] {localizacao} — {atividade}: {mudanca}"
        return texto

    except Exception as e:
        logger.error(f"Erro ao gerar texto de histórico: {e}")
        return "[Erro] Descrição indisponível"


def gerar_entradas_historico(
    diff: Dict[str, Any],
    tipo: str,
) -> List[Dict[str, Any]]:
    """
    Converte diff em lista de entradas de histórico.

    Args:
        diff: Dict retornado por comparar_versoes
        tipo: "ETA" | "Captação" | "ETE"

    Returns:
        Lista de dicts com entradas de histórico
    """
    try:
        entradas = []

        # Processar alterados
        for item in diff.get("alterados", []):
            entrada = {
                "data_upload": datetime.now().isoformat(),
                "tipo": tipo,
                "municipio_filtro": item.get("municipio", ""),
                "unidade": item.get("unidade"),
                "atividade": item.get("atividade", ""),
                "campo": item["alteracoes"][0].get("campo") if item.get("alteracoes") else "",
                "antes": item["alteracoes"][0].get("antes") if item.get("alteracoes") else "",
                "depois": item["alteracoes"][0].get("depois") if item.get("alteracoes") else "",
                "texto": gerar_texto_historico(item, tipo),
            }
            entradas.append(entrada)

        # Processar adicionados
        for item in diff.get("adicionados", []):
            entrada = {
                "data_upload": datetime.now().isoformat(),
                "tipo": tipo,
                "municipio_filtro": item.get("municipio", ""),
                "unidade": item.get("unidade"),
                "atividade": item.get("atividade", ""),
                "campo": "novo_item",
                "antes": "",
                "depois": item.get("status_atual", ""),
                "texto": f"[{tipo}] {item.get('municipio', '')} — {item.get('atividade', '')}: Novo item adicionado",
            }
            entradas.append(entrada)

        # Processar removidos
        for item in diff.get("removidos", []):
            entrada = {
                "data_upload": datetime.now().isoformat(),
                "tipo": tipo,
                "municipio_filtro": item.get("municipio", ""),
                "unidade": item.get("unidade"),
                "atividade": item.get("atividade", ""),
                "campo": "item_removido",
                "antes": item.get("status_atual", ""),
                "depois": "",
                "texto": f"[{tipo}] {item.get('municipio', '')} — {item.get('atividade', '')}: Item removido",
            }
            entradas.append(entrada)

        logger.info(f"Geradas {len(entradas)} entradas de histórico")
        return entradas

    except Exception as e:
        logger.error(f"Erro ao gerar entradas de histórico: {e}")
        return []


def contar_alteracoes(diff: Dict[str, Any]) -> Tuple[int, int, int]:
    """
    Conta total de alterações no diff.

    Args:
        diff: Dict retornado por comparar_versoes

    Returns:
        Tupla (total_alterados, total_adicionados, total_removidos)
    """
    return (
        len(diff.get("alterados", [])),
        len(diff.get("adicionados", [])),
        len(diff.get("removidos", [])),
    )
