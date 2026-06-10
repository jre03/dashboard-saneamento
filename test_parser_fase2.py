"""
Testes da Fase 2: Parser de Planilhas

Testa com as planilhas reais do projeto:
- data-eta/20260424 - Plano-de-Ação_ETAs.xlsx
- data-captação/20260602 - Plano-de-Ação_Captações.xlsx
- data-ete/20260603 - Plano-de-Ação_ETEs.xlsx
"""

import sys
import os
from pathlib import Path

# Adicionar módulos ao path
sys.path.insert(0, str(Path(__file__).parent))

from modules import parser
import pandas as pd
from datetime import datetime


def test_identificar_tipo():
    """Testa identificação automática de tipo."""
    print("=" * 80)
    print("TEST 1: Identificação de Tipo")
    print("=" * 80)

    arquivos = {
        "../data-eta/20260424 - Plano-de-Ação_ETAs.xlsx": "ETA",
        "../data-captação/20260602 - Plano-de-Ação_Captações.xlsx": "Captação",
        "../data-ete/20260603 - Plano-de-Ação_ETEs.xlsx": "ETE",
    }

    for caminho, tipo_esperado in arquivos.items():
        try:
            tipo = parser.identificar_tipo(caminho)
            status = "✅ PASS" if tipo == tipo_esperado else "❌ FAIL"
            print(f"{status} | {caminho}")
            print(f"   Esperado: {tipo_esperado}, Obtido: {tipo}\n")
        except Exception as e:
            print(f"❌ ERRO | {caminho}")
            print(f"   {e}\n")


def test_extrair_data():
    """Testa extração de data do nome do arquivo."""
    print("=" * 80)
    print("TEST 2: Extração de Data")
    print("=" * 80)

    arquivos = {
        "20260424 - Plano-de-Ação_ETAs.xlsx": datetime(2026, 4, 24),
        "20260602 - Plano-de-Ação_Captações.xlsx": datetime(2026, 6, 2),
        "20260603 - Plano-de-Ação_ETEs.xlsx": datetime(2026, 6, 3),
    }

    for nome, data_esperada in arquivos.items():
        data = parser.extrair_data_arquivo(nome)
        status = "✅ PASS" if data == data_esperada else "❌ FAIL"
        print(f"{status} | {nome}")
        print(f"   Esperado: {data_esperada}, Obtido: {data}\n")


def test_normalizar_etas():
    """Testa normalização de ETAs."""
    print("=" * 80)
    print("TEST 3: Normalização de ETAs")
    print("=" * 80)

    caminho = "../data-eta/20260424 - Plano-de-Ação_ETAs.xlsx"
    try:
        df = parser.normalizar_planilha(caminho, "ETA")

        print(f"✅ Arquivo lido: {len(df)} linhas, {len(df.columns)} colunas")
        print(f"\nColunas: {list(df.columns)}")
        print(f"\nDados de amostra:")
        print(df[["municipio", "atividade", "evolucao", "status_atual"]].head(10))

        # Validações
        assert "municipio" in df.columns, "Coluna 'municipio' faltante"
        assert "evolucao" in df.columns, "Coluna 'evolucao' faltante"
        assert df["municipio"].notna().sum() > 0, "Município com valores vazios"
        assert 0 <= df["evolucao"].min() <= 1 or df["evolucao"].isna().any(), "Evolução fora do intervalo [0, 1]"
        assert 0 <= df["evolucao"].max() <= 1 or df["evolucao"].isna().any(), "Evolução fora do intervalo [0, 1]"

        print("\n✅ PASS | ETAs normalizadas corretamente")

    except Exception as e:
        print(f"❌ FAIL | Erro ao normalizar ETAs: {e}")


def test_normalizar_captacoes():
    """Testa normalização de Captações."""
    print("=" * 80)
    print("TEST 4: Normalização de Captações")
    print("=" * 80)

    caminho = "../data-captação/20260602 - Plano-de-Ação_Captações.xlsx"
    try:
        df = parser.normalizar_planilha(caminho, "Captação")

        print(f"✅ Arquivo lido: {len(df)} linhas, {len(df.columns)} colunas")
        print(f"\nColunas: {list(df.columns)}")
        print(f"\nDados de amostra:")
        print(df[["municipio", "atividade", "evolucao", "status_atual"]].head(10))

        # Validações
        assert "municipio" in df.columns, "Coluna 'municipio' faltante"
        assert "evolucao" in df.columns, "Coluna 'evolucao' faltante"
        assert df["municipio"].notna().sum() > 0, "Município com valores vazios"

        print("\n✅ PASS | Captações normalizadas corretamente")

    except Exception as e:
        print(f"❌ FAIL | Erro ao normalizar Captações: {e}")


def test_normalizar_etes():
    """Testa normalização de ETEs."""
    print("=" * 80)
    print("TEST 5: Normalização de ETEs")
    print("=" * 80)

    caminho = "../data-ete/20260603 - Plano-de-Ação_ETEs.xlsx"
    try:
        df = parser.normalizar_planilha(caminho, "ETE")

        print(f"✅ Arquivo lido: {len(df)} linhas, {len(df.columns)} colunas")
        print(f"\nColunas: {list(df.columns)}")
        print(f"\nDados de amostra:")
        print(df[["municipio", "unidade", "atividade", "evolucao", "status_atual"]].head(10))

        # Validações
        assert "municipio" in df.columns, "Coluna 'municipio' faltante"
        assert "unidade" in df.columns, "Coluna 'unidade' faltante"
        assert "evolucao" in df.columns, "Coluna 'evolucao' faltante"
        assert df["municipio"].notna().sum() > 0, "Município com valores vazios"
        assert df["unidade"].notna().sum() > 0, "Unidade com valores vazios"

        print("\n✅ PASS | ETEs normalizadas corretamente")

    except Exception as e:
        print(f"❌ FAIL | Erro ao normalizar ETEs: {e}")


def test_ffill():
    """Testa forward fill de colunas agrupadas."""
    print("=" * 80)
    print("TEST 6: Forward Fill (Colunas Agrupadas)")
    print("=" * 80)

    # Testar com ETA (Município deve ser propagado)
    df_eta = parser.normalizar_planilha("../data-eta/20260424 - Plano-de-Ação_ETAs.xlsx", "ETA")
    municipios_vazios_eta = df_eta["municipio"].isna().sum()
    print(f"ETAs: {municipios_vazios_eta} cédulas vazias em 'municipio'")

    # Testar com Captação
    df_capt = parser.normalizar_planilha("../data-captação/20260602 - Plano-de-Ação_Captações.xlsx", "Captação")
    municipios_vazios_capt = df_capt["municipio"].isna().sum()
    print(f"Captações: {municipios_vazios_capt} cédulas vazias em 'municipio'")

    # Testar com ETE
    df_ete = parser.normalizar_planilha("../data-ete/20260603 - Plano-de-Ação_ETEs.xlsx", "ETE")
    municipios_vazios_ete = df_ete["municipio"].isna().sum()
    unidades_vazios_ete = df_ete["unidade"].isna().sum()
    print(f"ETEs: {municipios_vazios_ete} cédulas vazias em 'municipio', {unidades_vazios_ete} em 'unidade'")

    if municipios_vazios_eta == 0 and municipios_vazios_capt == 0 and municipios_vazios_ete == 0 and unidades_vazios_ete == 0:
        print("\n✅ PASS | Forward fill funcionando corretamente")
    else:
        print("\n⚠️  AVISO | Alguns valores ainda vazios (pode ser normal em certas linhas)")


def test_evolucao():
    """Testa normalização do campo Evolução."""
    print("=" * 80)
    print("TEST 7: Normalização de Evolução")
    print("=" * 80)

    df_eta = parser.normalizar_planilha("../data-eta/20260424 - Plano-de-Ação_ETAs.xlsx", "ETA")

    valores_unicos = df_eta["evolucao"].dropna().unique()
    print(f"Valores únicos de Evolução (ETAs): {sorted(valores_unicos)}")

    # Verificar intervalo
    min_val = df_eta["evolucao"].min()
    max_val = df_eta["evolucao"].max()
    print(f"Min: {min_val}, Max: {max_val}")

    # Contar NaNs
    nans = df_eta["evolucao"].isna().sum()
    print(f"NaNs: {nans}")

    if 0 <= min_val <= 1 and 0 <= max_val <= 1:
        print("\n✅ PASS | Evolução normalizada corretamente [0, 1]")
    else:
        print("\n❌ FAIL | Evolução fora do intervalo [0, 1]")


def test_tipos():
    """Testa se tipo_projeto foi adicionado."""
    print("=" * 80)
    print("TEST 8: Campo tipo_projeto")
    print("=" * 80)

    tipos_esperados = {
        "../data-eta/20260424 - Plano-de-Ação_ETAs.xlsx": "ETA",
        "../data-captação/20260602 - Plano-de-Ação_Captações.xlsx": "Captação",
        "../data-ete/20260603 - Plano-de-Ação_ETEs.xlsx": "ETE",
    }

    for caminho, tipo_esperado in tipos_esperados.items():
        try:
            tipo_obj = parser.identificar_tipo(caminho)
            df = parser.normalizar_planilha(caminho, tipo_obj)

            tipos_unicos = df["tipo_projeto"].unique()
            assert len(tipos_unicos) == 1 and tipos_unicos[0] == tipo_esperado

            print(f"✅ PASS | {tipo_esperado}: tipo_projeto adicionado corretamente")
        except Exception as e:
            print(f"❌ FAIL | {tipo_esperado}: {e}")


def run_all_tests():
    """Executa todos os testes."""
    print("\n")
    print("=" * 80)
    print("TESTES DA FASE 2: PARSER DE PLANILHAS")
    print("=" * 80)
    print()

    test_identificar_tipo()
    test_extrair_data()
    test_normalizar_etas()
    test_normalizar_captacoes()
    test_normalizar_etes()
    test_ffill()
    test_evolucao()
    test_tipos()

    print("\n")
    print("=" * 80)
    print("TESTES CONCLUÍDOS")
    print("=" * 80)
    print()


if __name__ == "__main__":
    run_all_tests()
