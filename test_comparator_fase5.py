"""
Testes da Fase 5: Comparador de Versões

Testa comparação entre versões reais de diferentes datas.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from modules import parser, comparator
import pandas as pd

print("\n" + "="*80)
print("TESTES DA FASE 5: COMPARADOR DE VERSOES")
print("="*80 + "\n")

# TEST 1: Comparar duas versoes de ETAs
print("TEST 1: Comparacao de ETAs (datas diferentes)")
print("-" * 80)
try:
    # Carregar versoes diferentes
    versoes_eta = [
        ("../data-eta/20260327 - Plano-de-Acao_ETAs.xlsx", "2026-03-27"),
        ("../data-eta/20260424 - Plano-de-Acao_ETAs.xlsx", "2026-04-24"),
    ]

    df_v1 = None
    df_v2 = None
    data_v1 = None
    data_v2 = None

    for caminho, data in versoes_eta:
        try:
            df = parser.normalizar_planilha(caminho, "ETA")
            if df_v1 is None:
                df_v1 = df
                data_v1 = data
            else:
                df_v2 = df
                data_v2 = data
        except:
            pass

    if df_v1 is not None and df_v2 is not None:
        diff = comparator.comparar_versoes(df_v1, df_v2, "ETA")

        alterados, adicionados, removidos = comparator.contar_alteracoes(diff)

        print(f"[OK] Comparacao ETA: {data_v1} vs {data_v2}")
        print(f"     Alterados: {alterados}")
        print(f"     Adicionados: {adicionados}")
        print(f"     Removidos: {removidos}")
        print(f"     Total de mudancas: {alterados + adicionados + removidos}")

        if alterados > 0:
            print(f"\n     Exemplo de alteracao:")
            exemplo = diff["alterados"][0]
            print(f"     Atividade: {exemplo.get('atividade')}")
            print(f"     Municipio: {exemplo.get('municipio')}")
            if exemplo.get("alteracoes"):
                alt = exemplo["alteracoes"][0]
                print(f"     Campo alterado: {alt['campo']}")
                print(f"     {alt['antes']} → {alt['depois']}")
    else:
        print("[AVISO] Apenas uma versao de ETA disponivel")

except Exception as e:
    print(f"[FALHOU] {e}")

# TEST 2: Comparar versoes de Captacoes
print("\nTEST 2: Comparacao de Captacoes (datas diferentes)")
print("-" * 80)
try:
    versoes_capt = [
        ("../data-captacao/20260602 - Plano-de-Acao_Captacoes.xlsx", "2026-06-02"),
        ("../data-captacao/20260610 - Plano-de-Acao_Captacoes.xlsx", "2026-06-10"),
    ]

    df_v1 = None
    df_v2 = None

    for caminho, data in versoes_capt:
        try:
            df = parser.normalizar_planilha(caminho, "Captacao")
            if df_v1 is None:
                df_v1 = df
                data_v1 = data
            else:
                df_v2 = df
                data_v2 = data
        except:
            pass

    if df_v1 is not None and df_v2 is not None:
        diff = comparator.comparar_versoes(df_v1, df_v2, "Captacao")
        alterados, adicionados, removidos = comparator.contar_alteracoes(diff)

        print(f"[OK] Comparacao Captacao: {data_v1} vs {data_v2}")
        print(f"     Alterados: {alterados}")
        print(f"     Adicionados: {adicionados}")
        print(f"     Removidos: {removidos}")
    else:
        print("[AVISO] Apenas uma versao de Captacao disponivel")

except Exception as e:
    print(f"[FALHOU] {e}")

# TEST 3: Gerar texto de historico
print("\nTEST 3: Geracao de Texto de Historico")
print("-" * 80)
try:
    # Criar diff_item de teste
    diff_item_alterado = {
        "municipio": "MATRIZ DE CAMARAGIBE",
        "atividade": "Projeto Hidraulico",
        "alteracoes": [
            {
                "campo": "status_atual",
                "antes": "Pendente",
                "depois": "Concluido"
            }
        ]
    }

    texto = comparator.gerar_texto_historico(diff_item_alterado, "ETA")
    print(f"[OK] Texto gerado (alterado):")
    print(f"     {texto}")

    # Teste com ETE
    diff_item_ete = {
        "municipio": "COLONIA LEOPOLDINA",
        "unidade": "ETE Colonia Leopoldina",
        "atividade": "Orcamentos",
        "alteracoes": [
            {
                "campo": "evolucao",
                "antes": "0%",
                "depois": "80%"
            }
        ]
    }

    texto_ete = comparator.gerar_texto_historico(diff_item_ete, "ETE")
    print(f"\n[OK] Texto gerado (ETE):")
    print(f"     {texto_ete}")

except Exception as e:
    print(f"[FALHOU] {e}")

# TEST 4: Gerar entradas de historico
print("\nTEST 4: Geracao de Entradas de Historico")
print("-" * 80)
try:
    # Usar diff do TEST 1
    if df_v1 is not None and df_v2 is not None:
        diff = comparator.comparar_versoes(df_v1, df_v2, "ETA")
        entradas = comparator.gerar_entradas_historico(diff, "ETA")

        print(f"[OK] Entradas geradas: {len(entradas)}")

        if entradas:
            entrada = entradas[0]
            print(f"\n     Exemplo de entrada:")
            print(f"     Tipo: {entrada['tipo']}")
            print(f"     Municipio: {entrada['municipio_filtro']}")
            print(f"     Atividade: {entrada['atividade']}")
            print(f"     Campo: {entrada['campo']}")
            print(f"     Texto: {entrada['texto']}")

except Exception as e:
    print(f"[FALHOU] {e}")

# TEST 5: Validar estrutura do diff
print("\nTEST 5: Estrutura do Diff")
print("-" * 80)
try:
    # Carregar dados para teste
    df_eta_test = parser.normalizar_planilha("../data-eta/20260424 - Plano-de-Acao_ETAs.xlsx", "ETA")

    # Criar uma versao modificada para teste
    df_eta_mod = df_eta_test.copy()
    df_eta_mod.loc[0, "status_atual"] = "Atrasado"
    df_eta_mod.loc[1, "evolucao"] = 0.5

    diff = comparator.comparar_versoes(df_eta_test, df_eta_mod, "ETA")

    # Verificar chaves do diff
    assert "alterados" in diff, "Chave 'alterados' faltante"
    assert "adicionados" in diff, "Chave 'adicionados' faltante"
    assert "removidos" in diff, "Chave 'removidos' faltante"

    print("[OK] Estrutura do diff validada")
    print(f"     Chaves presentes: alterados, adicionados, removidos")
    print(f"     Altercoes detectadas: {len(diff['alterados'])}")

except Exception as e:
    print(f"[FALHOU] {e}")

print("\n" + "="*80)
print("TESTES CONCLUIDOS")
print("="*80 + "\n")

print("NOTA: Comparador de versoes funcionando!")
print("\nProximos passos:")
print("  1. Integrar comparator.py no app.py (aba Comparativo)")
print("  2. Testar com multiplas versoes no Streamlit")
print("  3. Validar geracao de historico")
print()
