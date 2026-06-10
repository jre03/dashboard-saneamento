"""Testes simplificados da Fase 2: Parser"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from modules import parser
from datetime import datetime

print("\n" + "="*80)
print("TESTES DA FASE 2: PARSER DE PLANILHAS")
print("="*80 + "\n")

# TEST 1: Identificacao de tipo
print("TEST 1: Identificacao de Tipo")
print("-" * 80)
arquivos_teste = {
    "../data-eta/20260424 - Plano-de-Ação_ETAs.xlsx": "ETA",
    "../data-captação/20260602 - Plano-de-Ação_Captações.xlsx": "Captação",
    "../data-ete/20260603 - Plano-de-Ação_ETEs.xlsx": "ETE",
}

for caminho, tipo_esperado in arquivos_teste.items():
    tipo = parser.identificar_tipo(caminho)
    match = "OK" if tipo == tipo_esperado else "FALHOU"
    print(f"[{match}] {caminho}")
    print(f"      Esperado: {tipo_esperado}, Obtido: {tipo}")

# TEST 2: Extrair data
print("\nTEST 2: Extracao de Data")
print("-" * 80)
nomes_teste = {
    "20260424 - Plano-de-Ação_ETAs.xlsx": datetime(2026, 4, 24),
    "20260602 - Plano-de-Ação_Captações.xlsx": datetime(2026, 6, 2),
}

for nome, data_esperada in nomes_teste.items():
    data = parser.extrair_data_arquivo(nome)
    match = "OK" if data == data_esperada else "FALHOU"
    print(f"[{match}] {nome} => {data}")

# TEST 3: Normalizar ETAs
print("\nTEST 3: Normalizacao de ETAs")
print("-" * 80)
try:
    df_eta = parser.normalizar_planilha("../data-eta/20260424 - Plano-de-Ação_ETAs.xlsx", "ETA")
    print(f"[OK] ETAs lidas: {len(df_eta)} linhas, {len(df_eta.columns)} colunas")
    print(f"     Municipios com dados: {df_eta['municipio'].notna().sum()}")
    print(f"     Atividades com dados: {df_eta['atividade'].notna().sum()}")
    print(f"     Evolucoes unicas: {sorted(df_eta['evolucao'].dropna().unique())}")
    print("\n     Amostra de dados:")
    print(df_eta[["municipio", "atividade", "evolucao", "status_atual"]].head(5).to_string())
except Exception as e:
    print(f"[FALHOU] {e}")

# TEST 4: Normalizar Captacoes
print("\nTEST 4: Normalizacao de Captacoes")
print("-" * 80)
try:
    df_capt = parser.normalizar_planilha("../data-captação/20260602 - Plano-de-Ação_Captações.xlsx", "Captação")
    print(f"[OK] Captacoes lidas: {len(df_capt)} linhas, {len(df_capt.columns)} colunas")
    print(f"     Municipios com dados: {df_capt['municipio'].notna().sum()}")
    print(f"     Atividades com dados: {df_capt['atividade'].notna().sum()}")
    print(f"     Evolucoes unicas: {sorted(df_capt['evolucao'].dropna().unique())}")
except Exception as e:
    print(f"[FALHOU] {e}")

# TEST 5: Normalizar ETEs
print("\nTEST 5: Normalizacao de ETEs")
print("-" * 80)
try:
    df_ete = parser.normalizar_planilha("../data-ete/20260603 - Plano-de-Ação_ETEs.xlsx", "ETE")
    print(f"[OK] ETEs lidas: {len(df_ete)} linhas, {len(df_ete.columns)} colunas")
    print(f"     Municipios com dados: {df_ete['municipio'].notna().sum()}")
    print(f"     Unidades com dados: {df_ete['unidade'].notna().sum()}")
    print(f"     Atividades com dados: {df_ete['atividade'].notna().sum()}")
    print(f"     Evolucoes unicas: {sorted(df_ete['evolucao'].dropna().unique())}")
    print(f"     Status unicos: {df_ete['status_atual'].unique()}")
except Exception as e:
    print(f"[FALHOU] {e}")

print("\n" + "="*80)
print("TESTES CONCLUIDOS")
print("="*80 + "\n")
