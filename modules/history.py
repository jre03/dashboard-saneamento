"""
Módulo de Feed de Histórico e Exportação.

Funcionalidades:
- Geração de entrada de histórico a partir de diffs
- Filtragem de histórico por tipo, município e período
- Exportação de histórico em formato .txt legível
- Formatação de feed vertical (mais recentes no topo)

Períodos suportados:
- "2 semanas" — últimos 14 dias
- "1 mês" — últimos 30 dias
- "3 meses" — últimos 90 dias
- "6 meses" — últimos 180 dias
- "tudo" — sem filtro de período
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

# Períodos pré-definidos (em dias)
PERIODOS = {
    "2 semanas": 14,
    "1 mês": 30,
    "3 meses": 90,
    "6 meses": 180,
    "tudo": None,  # Sem limite
}


def gerar_entrada_historico(
    diff_item: Dict[str, Any],
    tipo: str,
    municipio: str,
    unidade: Optional[str] = None,
    data_upload: Optional[datetime] = None,
) -> Dict[str, Any]:
    """
    Cria uma entrada estruturada de histórico a partir de um diff_item.

    Args:
        diff_item: Item do diff (alterado, adicionado ou removido)
        tipo: "ETA" | "Captação" | "ETE"
        municipio: Município ou localidade
        unidade: Unidade (apenas para ETE)
        data_upload: Data/hora do upload (padrão: agora)

    Returns:
        Dict com estrutura de entrada de histórico
    """
    try:
        if data_upload is None:
            data_upload = datetime.now()

        # Extrair dados do diff_item
        atividade = diff_item.get("atividade", "")
        status_atual = diff_item.get("status_atual", "")

        # Determinar tipo de mudança
        if "alteracoes" in diff_item:
            campo = diff_item["alteracoes"][0].get("campo") if diff_item["alteracoes"] else ""
            antes = diff_item["alteracoes"][0].get("antes") if diff_item["alteracoes"] else ""
            depois = diff_item["alteracoes"][0].get("depois") if diff_item["alteracoes"] else ""
        else:
            campo = ""
            antes = ""
            depois = ""

        entrada = {
            "data_upload": data_upload.isoformat() if isinstance(data_upload, datetime) else data_upload,
            "tipo": tipo,
            "municipio": municipio,
            "unidade": unidade,
            "atividade": atividade,
            "campo": campo,
            "antes": antes,
            "depois": depois,
            "texto": _gerar_texto_entrada(
                tipo=tipo,
                municipio=municipio,
                unidade=unidade,
                atividade=atividade,
                campo=campo,
                antes=antes,
                depois=depois,
            ),
        }

        return entrada

    except Exception as e:
        logger.error(f"Erro ao gerar entrada de histórico: {e}")
        return {}


def _gerar_texto_entrada(
    tipo: str,
    municipio: str,
    unidade: Optional[str],
    atividade: str,
    campo: str,
    antes: str,
    depois: str,
) -> str:
    """
    Gera texto legível para a entrada de histórico.

    Args:
        tipo: Tipo do projeto
        municipio: Município
        unidade: Unidade (ETE)
        atividade: Atividade
        campo: Campo alterado
        antes: Valor anterior
        depois: Novo valor

    Returns:
        String formatada
    """
    try:
        # Construir localização
        if tipo == "ETE" and unidade:
            localizacao = f"{municipio} / {unidade}"
        else:
            localizacao = municipio

        # Construir mudança
        if campo and antes and depois:
            mudanca = f"{campo}: {antes} > {depois}"
        elif antes or depois:
            mudanca = f"Status: {depois or antes}"
        else:
            mudanca = "Alteracao"

        return f"[{tipo}] {localizacao} — {atividade}: {mudanca}"

    except Exception as e:
        logger.error(f"Erro ao gerar texto: {e}")
        return ""


def filtrar_historico(
    historico: List[Dict[str, Any]],
    tipo: Optional[str] = None,
    municipio: Optional[str] = None,
    periodo: str = "tudo",
) -> List[Dict[str, Any]]:
    """
    Filtra histórico por tipo, município e período.

    Args:
        historico: Lista completa de entradas de histórico
        tipo: "ETA" | "Captação" | "ETE" | None (tudo)
        municipio: Nome do município | None (tudo)
        periodo: "2 semanas" | "1 mês" | "3 meses" | "6 meses" | "tudo"

    Returns:
        Histórico filtrado, ordenado por data decrescente
    """
    try:
        if not historico or len(historico) == 0:
            return []

        df_hist = pd.DataFrame(historico)

        # Converter data_upload para datetime
        if "data_upload" in df_hist.columns:
            df_hist["data_upload"] = pd.to_datetime(df_hist["data_upload"], errors="coerce")

        # Filtrar por tipo
        if tipo and tipo != "Todos":
            df_hist = df_hist[df_hist["tipo"] == tipo]

        # Filtrar por município
        if municipio and municipio != "Todos":
            df_hist = df_hist[df_hist["municipio"] == municipio]

        # Filtrar por período
        dias_limite = PERIODOS.get(periodo)
        if dias_limite is not None:
            data_limite = datetime.now() - timedelta(days=dias_limite)
            df_hist = df_hist[df_hist["data_upload"] >= data_limite]

        # Ordenar por data decrescente (mais recentes primeiro)
        df_hist = df_hist.sort_values("data_upload", ascending=False)

        # Converter de volta para lista de dicts
        resultado = df_hist.to_dict("records")

        logger.info(
            f"Histórico filtrado: tipo={tipo}, municipio={municipio}, "
            f"periodo={periodo}, resultados={len(resultado)}"
        )

        return resultado

    except Exception as e:
        logger.error(f"Erro ao filtrar histórico: {e}")
        return []


def exportar_txt(
    historico_filtrado: List[Dict[str, Any]],
    tipo: Optional[str] = None,
    periodo: str = "tudo",
    municipio: Optional[str] = None,
) -> str:
    """
    Exporta histórico filtrado em formato .txt legível.

    Formato:
    ```
    =====
    [TIPO] Historico de Alteracoes — DATA
    Filtro: PERIODO | Municipio: MUNICIPIO | Tipo: TIPO
    =====

    MUNICIPIO 1
      • Data — [TIPO] Atividade
        Mudanca

    MUNICIPIO 2
      • Data — [TIPO] Atividade
        Mudanca
    ```

    Args:
        historico_filtrado: Lista filtrada de entradas
        tipo: Tipo selecionado para o título
        periodo: Período selecionado
        municipio: Município selecionado

    Returns:
        String formatada em .txt
    """
    try:
        if not historico_filtrado or len(historico_filtrado) == 0:
            return "Sem entradas de histórico para o período/filtro selecionado.\n"

        # Cabeçalho
        data_agora = datetime.now().strftime("%d/%m/%Y")
        tipo_titulo = tipo or "Todos"

        linhas = [
            "=" * 80,
            f"[{tipo_titulo}] Historico de Alteracoes — {data_agora}",
            f"Filtro: {periodo} | Municipio: {municipio or 'Todos'} | Tipo: {tipo_titulo}",
            "=" * 80,
            "",
        ]

        # Agrupar por município
        municipios_dict = {}
        for entrada in historico_filtrado:
            mun = entrada.get("municipio", "N/A")
            if mun not in municipios_dict:
                municipios_dict[mun] = []
            municipios_dict[mun].append(entrada)

        # Formatar por município
        for mun in sorted(municipios_dict.keys()):
            linhas.append(mun)

            entradas = municipios_dict[mun]
            for entrada in entradas:
                # Extrair data
                data_str = entrada.get("data_upload", "")
                if isinstance(data_str, str):
                    try:
                        data_obj = pd.to_datetime(data_str)
                        data_fmt = data_obj.strftime("%d/%m/%Y %H:%M")
                    except:
                        data_fmt = data_str[:10]  # Tentar pegar YYYY-MM-DD
                else:
                    data_fmt = str(data_str)[:10]

                atividade = entrada.get("atividade", "")
                texto = entrada.get("texto", "")

                # Extrair apenas a mudança (após ":")
                if ":" in texto:
                    mudanca = texto.split(":", 1)[1].strip()
                else:
                    mudanca = texto

                linhas.append(f"  • {data_fmt} — {atividade}")
                linhas.append(f"    {mudanca}")

            linhas.append("")

        # Rodapé
        linhas.append("=" * 80)
        linhas.append(f"Total de entradas: {len(historico_filtrado)}")
        linhas.append("")

        return "\n".join(linhas)

    except Exception as e:
        logger.error(f"Erro ao exportar para txt: {e}")
        return f"Erro ao exportar histórico: {e}\n"


def obter_municipios_unicos(historico: List[Dict[str, Any]]) -> List[str]:
    """
    Obtém lista de municípios únicos no histórico.

    Args:
        historico: Lista de entradas de histórico

    Returns:
        Lista ordenada de municípios únicos
    """
    try:
        if not historico:
            return []

        municipios = set()
        for entrada in historico:
            mun = entrada.get("municipio")
            if mun:
                municipios.add(mun)

        return sorted(list(municipios))

    except Exception as e:
        logger.error(f"Erro ao obter municípios: {e}")
        return []


def obter_tipos_unicos(historico: List[Dict[str, Any]]) -> List[str]:
    """
    Obtém lista de tipos únicos no histórico.

    Args:
        historico: Lista de entradas de histórico

    Returns:
        Lista ordenada de tipos únicos
    """
    try:
        if not historico:
            return []

        tipos = set()
        for entrada in historico:
            tipo = entrada.get("tipo")
            if tipo:
                tipos.add(tipo)

        return sorted(list(tipos))

    except Exception as e:
        logger.error(f"Erro ao obter tipos: {e}")
        return []


def contar_entradas_por_periodo(historico: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Conta número de entradas por período.

    Args:
        historico: Lista completa de entradas

    Returns:
        Dict com contagem por período
    """
    try:
        if not historico:
            return {p: 0 for p in PERIODOS.keys()}

        df_hist = pd.DataFrame(historico)

        if "data_upload" not in df_hist.columns or len(df_hist) == 0:
            return {p: 0 for p in PERIODOS.keys()}

        df_hist["data_upload"] = pd.to_datetime(df_hist["data_upload"], errors="coerce")

        contagem = {}
        for periodo, dias in PERIODOS.items():
            if dias is None:
                contagem[periodo] = len(df_hist)
            else:
                data_limite = datetime.now() - timedelta(days=dias)
                contagem[periodo] = len(df_hist[df_hist["data_upload"] >= data_limite])

        return contagem

    except Exception as e:
        logger.error(f"Erro ao contar entradas: {e}")
        return {p: 0 for p in PERIODOS.keys()}
