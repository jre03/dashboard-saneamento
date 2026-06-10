"""Teste do Comparador com dados mock (Fase 5)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from modules import comparator
import pandas as pd
import numpy as np

print("\n" + "="*80)
print("TESTE: COMPARADOR DE VERSOES (DADOS MOCK)")
print("="*80 + "\n")

# Criar DataFrames mock para testar
print("Criando dados mock para teste...")

df_v1 = pd.DataFrame({
    "municipio_filtro": ["CAPTA1", "CAPTA1", "CAPTA2", "CAPTA2"],
    "municipio": ["CAPT-A", "CAPT-A", "CAPT-B", "CAPT-B"],
    "unidade": [np.nan, np.nan, np.nan, np.nan],
    "atividade": ["Topografia", "Orcamentos", "Topografia", "Orcamentos"],
    "plano_de_acao": ["Envio", "Elaboracao", "Envio", "Elaboracao"],
    "responsavel": ["BIANCADE", "VERDE", "BIANCADE", "VERDE"],
    "status_atual": ["Concluido", "Pendente", "Pendente", "Pendente"],
    "evolucao": [1.0, 0.0, 0.0, 0.0],
    "data_entrega_final": ["2026-05-15", None, "2026-06-15", None],
    "data_estimada": [None, "2026-06-30", None, "2026-07-15"],
    "data_conclusao": ["2026-05-10", None, None, None],
    "tipo_projeto": ["Captacao"] * 4,
})

# V2: Com algumas mudancas
df_v2 = df_v1.copy()
df_v2.loc[0, "status_atual"] = "Atrasado"  # Item 1 mudou
df_v2.loc[1, "evolucao"] = 0.5  # Item 2 progresso
# Item 3 foi removido
df_v2 = df_v2[df_v2.index != 2]
# Item 4 novo adicionado
novo_item = {
    "municipio_filtro": "CAPTA3",
    "municipio": "CAPT-C",
    "unidade": np.nan,
    "atividade": "Sondagens",
    "plano_de_acao": "Envio",
    "responsavel": "BIANCADE",
    "status_atual": "Pendente",
    "evolucao": 0.0,
    "data_entrega_final": None,
    "data_estimada": "2026-08-15",
    "data_conclusao": None,
    "tipo_projeto": "Captacao",
}
df_v2 = pd.concat([df_v2, pd.DataFrame([novo_item])], ignore_index=True)

print(f"[OK] V1: {len(df_v1)} linhas")
print(f"[OK] V2: {len(df_v2)} linhas\n")

# TEST 1: Comparar
print("TEST 1: Comparacao de Versoes")
print("-" * 80)
diff = comparator.comparar_versoes(df_v1, df_v2, "Captacao")
alterados, adicionados, removidos = comparator.contar_alteracoes(diff)

print(f"[OK] Resultados:")
print(f"     Alterados: {alterados}")
print(f"     Adicionados: {adicionados}")
print(f"     Removidos: {removidos}\n")

if alterados > 0:
    print("     Exemplo - Item alterado:")
    item = diff["alterados"][0]
    print(f"     - Atividade: {item.get('atividade')}")
    print(f"     - Municipio: {item.get('municipio')}")
    for alt in item.get("alteracoes", []):
        print(f"     - {alt['campo']}: {alt['antes']} > {alt['depois']}")

# TEST 2: Gerar textos de historico
print("\n" + "-"*80)
print("TEST 2: Geracao de Textos de Historico")
print("-" * 80)

if alterados > 0:
    for i, item in enumerate(diff["alterados"], 1):
        texto = comparator.gerar_texto_historico(item, "Captacao")
        print(f"[OK] {i}. {texto}")

# TEST 3: Gerar entradas
print("\n" + "-"*80)
print("TEST 3: Geracao de Entradas de Historico")
print("-" * 80)

entradas = comparator.gerar_entradas_historico(diff, "Captacao")
print(f"[OK] {len(entradas)} entradas geradas\n")

for i, entrada in enumerate(entradas, 1):
    print(f"{i}. Tipo: {entrada['tipo']}")
    print(f"   Municipio: {entrada['municipio_filtro']}")
    print(f"   Campo: {entrada['campo']}")
    print(f"   {entrada['antes']} > {entrada['depois']}")
    print()

# TEST 4: Validar estrutura
print("-"*80)
print("TEST 4: Validacao de Estrutura")
print("-" * 80)

assert "alterados" in diff
assert "adicionados" in diff
assert "removidos" in diff

for item in diff["alterados"]:
    assert "municipio" in item
    assert "atividade" in item
    assert "alteracoes" in item
    for alt in item["alteracoes"]:
        assert "campo" in alt
        assert "antes" in alt
        assert "depois" in alt

print("[OK] Estrutura do diff validada corretamente")

print("\n" + "="*80)
print("TODOS OS TESTES PASSARAM")
print("="*80 + "\n")
