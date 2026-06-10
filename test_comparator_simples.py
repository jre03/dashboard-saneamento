"""Teste simplificado do Comparador de Versoes (Fase 5)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from modules import parser, comparator
import pandas as pd

print("\n" + "="*80)
print("TESTE SIMPLIFICADO: COMPARADOR DE VERSOES")
print("="*80 + "\n")

try:
    # Carregar dados reais
    print("Carregando dados ETA...")
    df_original = parser.normalizar_planilha("../data-eta/20260424 - Plano-de-Acao_ETAs.xlsx", "ETA")
    print(f"[OK] {len(df_original)} linhas carregadas\n")

    # Criar versao modificada para teste
    df_modificada = df_original.copy()

    # Fazer algumas mudancas
    df_modificada.loc[0, "status_atual"] = "Atrasado"  # Mudou status
    df_modificada.loc[1, "evolucao"] = 0.5  # Mudou evolucao
    df_modificada.loc[2, "responsavel"] = "NOVO_RESPONSAVEL"  # Mudou responsavel

    print("Comparando versoes...")
    diff = comparator.comparar_versoes(df_original, df_modificada, "ETA")

    alterados, adicionados, removidos = comparator.contar_alteracoes(diff)

    print(f"[OK] Comparacao concluida:")
    print(f"     Alterados: {alterados}")
    print(f"     Adicionados: {adicionados}")
    print(f"     Removidos: {removidos}\n")

    # Mostrar exemplo de alteracao
    if alterados > 0:
        print("Exemplos de alteracoes:")
        for i, item in enumerate(diff["alterados"][:3]):
            print(f"\n  {i+1}. {item.get('municipio')} - {item.get('atividade')}")
            for alt in item.get("alteracoes", [])[:2]:
                print(f"     {alt['campo']}: {alt['antes']} para {alt['depois']}")

    # Testar geracao de texto
    print("\n" + "-"*80)
    print("Gerando textos de historico...")
    if alterados > 0:
        item = diff["alterados"][0]
        texto = comparator.gerar_texto_historico(item, "ETA")
        print(f"[OK] Texto gerado (sem caracteres especiais):")
        print(f"     {texto}")

    # Testar entradas de historico
    print("\n" + "-"*80)
    print("Gerando entradas de historico...")
    entradas = comparator.gerar_entradas_historico(diff, "ETA")
    print(f"[OK] {len(entradas)} entradas geradas")

    if entradas:
        entrada = entradas[0]
        print(f"\n     Exemplo:")
        print(f"     - Tipo: {entrada['tipo']}")
        print(f"     - Municipio: {entrada['municipio_filtro']}")
        print(f"     - Campo: {entrada['campo']}")
        print(f"     - Antes: {entrada['antes']}")
        print(f"     - Depois: {entrada['depois']}")

    print("\n" + "="*80)
    print("TESTE CONCLUIDO COM SUCESSO")
    print("="*80 + "\n")

except Exception as e:
    print(f"[FALHOU] {e}")
    import traceback
    traceback.print_exc()
