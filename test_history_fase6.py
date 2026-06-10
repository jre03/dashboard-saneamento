"""Testes da Fase 6: Historico & Exportacao"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from modules import history
from datetime import datetime, timedelta
import pandas as pd

print("\n" + "="*80)
print("TESTES DA FASE 6: HISTORICO & EXPORTACAO")
print("="*80 + "\n")

# Criar historico mock com varias entradas
print("Criando historico mock...")
agora = datetime.now()

historico_mock = [
    {
        "data_upload": (agora - timedelta(days=1)).isoformat(),
        "tipo": "ETA",
        "municipio": "MATRIZ DE CAMARAGIBE",
        "unidade": None,
        "atividade": "Projeto Hidraulico",
        "campo": "status_atual",
        "antes": "Pendente",
        "depois": "Concluido",
        "texto": "[ETA] MATRIZ DE CAMARAGIBE — Projeto Hidraulico: status_atual: Pendente > Concluido",
    },
    {
        "data_upload": (agora - timedelta(days=3)).isoformat(),
        "tipo": "Captacao",
        "municipio": "BRANQUINHA",
        "unidade": None,
        "atividade": "Topografia",
        "campo": "evolucao",
        "antes": "0%",
        "depois": "50%",
        "texto": "[Captacao] BRANQUINHA — Topografia: evolucao: 0% > 50%",
    },
    {
        "data_upload": (agora - timedelta(days=10)).isoformat(),
        "tipo": "ETE",
        "municipio": "COLONIA LEOPOLDINA",
        "unidade": "ETE Colonia Leopoldina",
        "atividade": "Orcamentos",
        "campo": "status_atual",
        "antes": "Pendente",
        "depois": "Concluido",
        "texto": "[ETE] COLONIA LEOPOLDINA / ETE Colonia Leopoldina — Orcamentos: status_atual: Pendente > Concluido",
    },
    {
        "data_upload": (agora - timedelta(days=40)).isoformat(),
        "tipo": "ETA",
        "municipio": "PORTO CALVO",
        "unidade": None,
        "atividade": "Sondagens",
        "campo": "status_atual",
        "antes": "Pendente",
        "depois": "Atrasado",
        "texto": "[ETA] PORTO CALVO — Sondagens: status_atual: Pendente > Atrasado",
    },
]

print(f"[OK] {len(historico_mock)} entradas criadas\n")

# TEST 1: Filtrar por periodo
print("TEST 1: Filtragem por Periodo")
print("-" * 80)
try:
    periodos = ["2 semanas", "1 mes", "3 meses", "6 meses", "tudo"]

    for periodo in periodos:
        filtrado = history.filtrar_historico(historico_mock, periodo=periodo)
        print(f"[OK] {periodo:15} -> {len(filtrado)} entradas")

except Exception as e:
    print(f"[FALHOU] {e}")

# TEST 2: Filtrar por tipo
print("\nTEST 2: Filtragem por Tipo")
print("-" * 80)
try:
    for tipo in ["ETA", "Captacao", "ETE"]:
        filtrado = history.filtrar_historico(historico_mock, tipo=tipo)
        print(f"[OK] Tipo {tipo:10} -> {len(filtrado)} entradas")

except Exception as e:
    print(f"[FALHOU] {e}")

# TEST 3: Filtrar por municipio
print("\nTEST 3: Filtragem por Municipio")
print("-" * 80)
try:
    municipios = history.obter_municipios_unicos(historico_mock)
    print(f"[OK] Municipios encontrados: {municipios}\n")

    for mun in municipios[:2]:
        filtrado = history.filtrar_historico(historico_mock, municipio=mun)
        print(f"[OK] {mun:25} -> {len(filtrado)} entradas")

except Exception as e:
    print(f"[FALHOU] {e}")

# TEST 4: Contar entradas por periodo
print("\nTEST 4: Contagem por Periodo")
print("-" * 80)
try:
    contagem = history.contar_entradas_por_periodo(historico_mock)

    for periodo, count in contagem.items():
        print(f"[OK] {periodo:15} -> {count} entradas")

except Exception as e:
    print(f"[FALHOU] {e}")

# TEST 5: Exportar para TXT
print("\nTEST 5: Exportacao para TXT")
print("-" * 80)
try:
    # Teste 1: Tudo
    txt_tudo = history.exportar_txt(historico_mock, tipo=None, periodo="tudo")
    linhas_tudo = txt_tudo.split("\n")
    print(f"[OK] Exportacao completa:")
    print(f"     Linhas: {len(linhas_tudo)}")
    print(f"     Primeiras linhas:")
    for linha in linhas_tudo[:5]:
        if linha:
            print(f"     {linha}")

    # Teste 2: Apenas ultimas 2 semanas
    print(f"\n[OK] Exportacao (2 semanas):")
    txt_2sem = history.exportar_txt(historico_mock, periodo="2 semanas")
    linhas_2sem = txt_2sem.split("\n")
    print(f"     Linhas: {len(linhas_2sem)}")

    # Teste 3: Apenas ETA
    print(f"\n[OK] Exportacao (ETA):")
    txt_eta = history.exportar_txt(
        history.filtrar_historico(historico_mock, tipo="ETA"),
        tipo="ETA",
        periodo="tudo"
    )
    print(f"     Linhas: {len(txt_eta.split(chr(10)))}")

except Exception as e:
    print(f"[FALHOU] {e}")

# TEST 6: Gerar entrada
print("\nTEST 6: Geracao de Entrada de Historico")
print("-" * 80)
try:
    diff_item = {
        "municipio": "TESTE",
        "atividade": "Teste Atividade",
        "alteracoes": [
            {
                "campo": "status_atual",
                "antes": "Pendente",
                "depois": "Concluido"
            }
        ]
    }

    entrada = history.gerar_entrada_historico(
        diff_item,
        tipo="ETA",
        municipio="TESTE"
    )

    print("[OK] Entrada gerada:")
    print(f"     Tipo: {entrada.get('tipo')}")
    print(f"     Municipio: {entrada.get('municipio')}")
    print(f"     Atividade: {entrada.get('atividade')}")
    print(f"     Campo: {entrada.get('campo')}")

except Exception as e:
    print(f"[FALHOU] {e}")

print("\n" + "="*80)
print("TESTES CONCLUIDOS")
print("="*80 + "\n")
