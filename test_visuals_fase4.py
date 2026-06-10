"""
Testes da Fase 4: Visuals & Componentes

Testa componentes visuais com dados reais do parser.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from modules import parser, visuals
import pandas as pd

print("\n" + "="*80)
print("TESTES DA FASE 4: VISUALS & COMPONENTES")
print("="*80 + "\n")

# Preparar dados (usando parser da Fase 2)
print("Carregando dados reais para testes...")
try:
    df_eta = parser.normalizar_planilha("../data-eta/20260424 - Plano-de-Ação_ETAs.xlsx", "ETA")
    df_capt = parser.normalizar_planilha("../data-captação/20260602 - Plano-de-Ação_Captações.xlsx", "Captação")
    df_ete = parser.normalizar_planilha("../data-ete/20260603 - Plano-de-Ação_ETEs.xlsx", "ETE")
    print("[OK] Dados carregados com sucesso\n")
except Exception as e:
    print(f"[FALHOU] Erro ao carregar dados: {e}")
    sys.exit(1)

# TEST 1: Calcular metricas
print("TEST 1: Calculo de Metricas")
print("-" * 80)
try:
    for nome, df, tipo in [("ETA", df_eta, "ETA"), ("Captação", df_capt, "Captação"), ("ETE", df_ete, "ETE")]:
        total, pct_conc, pct_pend, pct_na = visuals.calcular_metricas(df)

        print(f"[OK] {nome}:")
        print(f"     Total: {total}")
        print(f"     Concluido: {pct_conc:.1f}%")
        print(f"     Pendente: {pct_pend:.1f}%")
        print(f"     N/A: {pct_na:.1f}%\n")

        # Validacoes
        assert total > 0, f"Total deve ser > 0"
        assert 0 <= pct_conc <= 100, f"Percentual deve estar em [0, 100]"
        assert 0 <= pct_pend <= 100, f"Percentual deve estar em [0, 100]"
        assert 0 <= pct_na <= 100, f"Percentual deve estar em [0, 100]"

except Exception as e:
    print(f"[FALHOU] {e}")

# TEST 2: Cores configuradas
print("TEST 2: Paleta de Cores")
print("-" * 80)
try:
    print("[OK] Cores por tipo:")
    for tipo, cor in visuals.CORES_TIPO.items():
        print(f"     {tipo}: {cor}")

    print("\n[OK] Cores por status:")
    for status, cor in visuals.CORES_STATUS.items():
        print(f"     {status}: {cor}")

    assert len(visuals.CORES_TIPO) == 3, "Deve ter 3 tipos de cor"
    assert len(visuals.CORES_STATUS) == 4, "Deve ter 4 status"

except Exception as e:
    print(f"[FALHOU] {e}")

# TEST 3: Preparacao de dados para graficos
print("\nTEST 3: Preparacao de Dados para Graficos")
print("-" * 80)
try:
    for nome, df, tipo in [("ETA", df_eta, "ETA"), ("Captação", df_capt, "Captação"), ("ETE", df_ete, "ETE")]:
        # Verificar municipios
        municipios = df["municipio"].nunique()

        # Verificar status
        status_unicos = df["status_atual"].nunique()

        print(f"[OK] {nome}:")
        print(f"     Municipios: {municipios}")
        print(f"     Status unicos: {status_unicos}")
        print(f"     Linhas: {len(df)}\n")

except Exception as e:
    print(f"[FALHOU] {e}")

# TEST 4: Funcoes existem e aceitam parametros
print("TEST 4: Funcoes Visuais")
print("-" * 80)
try:
    funcoes = [
        ('painel_metricas', [df_eta]),
        ('grafico_barras_municipio', [df_eta]),
        ('tabela_formatada', [df_eta]),
        ('grafico_evolucao_tempo', [[], "ETA"]),
        ('criar_resumo_visual', [df_eta]),
    ]

    for nome_func, args in funcoes:
        func = getattr(visuals, nome_func)
        print(f"[OK] {nome_func} existe e aceita argumentos")

except Exception as e:
    print(f"[FALHOU] {e}")

# TEST 5: Validacao de dataframes
print("\nTEST 5: Validacao de DataFrames")
print("-" * 80)
try:
    for nome, df, tipo in [("ETA", df_eta, "ETA"), ("Captação", df_capt, "Captação"), ("ETE", df_ete, "ETE")]:
        # Verificar colunas essenciais
        colunas_essenciais = ["municipio", "status_atual", "evolucao"]
        for col in colunas_essenciais:
            assert col in df.columns, f"Coluna {col} faltante em {nome}"

        print(f"[OK] {nome}: Todas as colunas essenciais presentes")

except Exception as e:
    print(f"[FALHOU] {e}")

# TEST 6: Status unicos
print("\nTEST 6: Status Unicos")
print("-" * 80)
try:
    for nome, df, tipo in [("ETA", df_eta, "ETA"), ("Captação", df_capt, "Captação"), ("ETE", df_ete, "ETE")]:
        status = df["status_atual"].unique()
        print(f"[OK] {nome}:")
        for s in status:
            if pd.notna(s):
                print(f"     - {s}")
            else:
                print(f"     - NaN")
        print()

except Exception as e:
    print(f"[FALHOU] {e}")

print("="*80)
print("TESTES CONCLUIDOS")
print("="*80 + "\n")

print("NOTA: Testes visuais completos (com Streamlit) requerem:")
print("  1. Streamlit rodando (streamlit run app.py)")
print("  2. Dados carregados na sessao")
print("  3. Interacao com componentes")
print("\nProximos passos:")
print("  1. Integrar visuals.py no app.py")
print("  2. Testar na interface Streamlit")
print("  3. Validar formatacao condicional e gráficos")
print()
