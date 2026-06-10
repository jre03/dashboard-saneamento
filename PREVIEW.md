# 🎨 PREVIEW VISUAL — Dashboard Saneamento

## Status Atual (Fase 1)

O app está rodando em **http://localhost:8501** com:
- ✅ Título "📊 Dashboard de Acompanhamento de Projetos de Saneamento"
- ✅ Mensagem de status (Fase 1 concluída)
- ✅ Tema visual aplicado (paleta profissional)
- ✅ Roadmap das 10 fases visível

---

## 📐 LAYOUT ESPERADO (Fase 7+)

### SIDEBAR (sempre visível à esquerda)

```
┌─────────────────────────────────────────┐
│ 🏠 Dashboard Saneamento                 │
├─────────────────────────────────────────┤
│                                         │
│ 📊 Tipo de Projeto:                    │
│ ┌─────────────────────────────────────┐ │
│ │ ▼ Selecione um tipo                │ │
│ │   ☐ ETA                            │ │
│ │   ☐ Captação                       │ │
│ │   ☐ ETE                            │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ 🔍 Filtros:                            │
│                                         │
│ Município Filtro:                      │
│ ┌─────────────────────────────────────┐ │
│ │ ✓ MATRIZ DE CAMARAGIBE             │ │
│ │ ✓ COLÔNIA LEOPOLDINA               │ │
│ │ ☐ PORTO CALVO                      │ │
│ │ ☐ CHAPÉU BAIXO                     │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ Atividade:                             │
│ ┌─────────────────────────────────────┐ │
│ │ ✓ Topografia                       │ │
│ │ ✓ Orçamentos                       │ │
│ │ ☐ Sondagens                        │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ Responsável:                           │
│ ┌─────────────────────────────────────┐ │
│ │ ✓ BIANCADE                         │ │
│ │ ✓ VERDE                            │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ Status Atual:                          │
│ ┌─────────────────────────────────────┐ │
│ │ ✓ Concluído                        │ │
│ │ ✓ Pendente                         │ │
│ │ ✓ Atrasado                         │ │
│ │ ✓ N/A                              │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ Evolução (%):                          │
│ [0 ─────●─────── 100]                 │
│                                         │
├─────────────────────────────────────────┤
│ 🔐 Upload & Exclusão                   │
├─────────────────────────────────────────┤
│                                         │
│ Senha Admin:                           │
│ ┌─────────────────────────────────────┐ │
│ │ ••••••••                           │ │
│ └─────────────────────────────────────┘ │
│ [Autenticar]                            │
│                                         │
│ Carregar Arquivo(s):                   │
│ [Clique para selecionar...]             │
│ (visível apenas se autenticado)        │
│                                         │
│ Excluir Arquivo:                       │
│ ┌─────────────────────────────────────┐ │
│ │ ▼ Selecione arquivo...             │ │
│ └─────────────────────────────────────┘ │
│ [Excluir]                               │
│ (visível apenas se autenticado)        │
│                                         │
└─────────────────────────────────────────┘
```

---

## 📊 ABA 1: VISÃO GERAL (Padrão)

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                     🔍 Visão Geral │ Comparativo │ Histórico                 ║
╚═══════════════════════════════════════════════════════════════════════════════╝

┌───────────────────────────────────────────────────────────────────────────────┐
│ 📈 PAINEL DE MÉTRICAS (DESTAQUE - Prioridade Principal)                      │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Total de Itens          Concluído              Pendente              N/A    │
│  ┌──────────────┐      ┌──────────────┐     ┌──────────────┐    ┌─────────┐ │
│  │     344      │      │    291 85%   │     │     45 13%   │    │  8  2%  │ │
│  │      ↑       │      │      ↑       │     │      ↑       │    │   ↓     │ │
│  │     +10      │      │     +10      │     │      -5      │    │    —    │ │
│  └──────────────┘      └──────────────┘     └──────────────┘    └─────────┘ │
│   (vs semana anterior)                                                       │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│ 📊 GRÁFICO: STATUS POR MUNICÍPIO                                              │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  MATRIZ DE CAMARAGIBE    ████████████░░░░░░░░░░░░  80%                       │
│  COLÔNIA LEOPOLDINA      █████████░░░░░░░░░░░░░░░  70%                       │
│  PORTO CALVO             ██████░░░░░░░░░░░░░░░░░░░  60%                       │
│  CHAPÉU BAIXO            ██████████████░░░░░░░░░░  50%                       │
│  UNIÃO DOS PALMARES      ███████████░░░░░░░░░░░░░░  45%                       │
│  JACUÍPE                 ███████░░░░░░░░░░░░░░░░░░  40%                       │
│  ...                                                                         │
│                                                                               │
│  Legenda:  ■ Concluído   ■ Pendente   ■ Atrasado   ■ N/A                    │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│ 📋 TABELA: DETALHES DOS ITENS (com scroll)                                   │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│ Município │ Atividade │ Responsável │ Status Atual │ Evolução │ Data Conclusão │
│───────────┼───────────┼─────────────┼──────────────┼──────────┼────────────────│
│ MATRIZ... │ Topografia│ BIANCADE    │ Concluído ✓  │ 100%    │ 2026-05-15    │
│ MATRIZ... │ Orçamentos│ VERDE       │ Pendente ⚠   │ 50%     │ 2026-06-30    │
│ COLÔNIA..│ Topografia│ BIANCADE    │ Concluído ✓  │ 100%    │ 2026-04-20    │
│ COLÔNIA..│ Orçamentos│ VERDE       │ Concluído ✓  │ 100%    │ 2026-06-09    │
│ PORTO C..│ Sondagens │ BIANCADE    │ Atrasado ❌  │ 35%     │ 2026-07-15    │
│ ...      │ ...       │ ...         │ ...          │ ...     │ ...            │
│                                                                               │
│  [← 1 de 15 páginas →]                                       [↓ Carregar +] │
│                                                                               │
│ Legenda:  ■ Verde = Concluído   ■ Amarelo = Pendente   ■ Cinza = N/A        │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 ABA 2: COMPARATIVO

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  Visão Geral │ 🔍 Comparativo │ Histórico                                     ║
╚═══════════════════════════════════════════════════════════════════════════════╝

┌───────────────────────────────────────────────────────────────────────────────┐
│ 📊 SELEÇÃO DE VERSÕES                                                        │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Versão A (Anterior):        Versão B (Atual):                              │
│  ┌────────────────────────┐  ┌────────────────────────┐                     │
│  │ ▼ 20260410-ETAs.xlsx   │  │ ▼ 20260424-ETAs.xlsx   │ ✓ Padrão: última    │
│  │   20260327-ETAs.xlsx   │  │   20260410-ETAs.xlsx   │   vs. penúltima    │
│  │   20260319-ETAs.xlsx   │  │   20260327-ETAs.xlsx   │                     │
│  │   20260306-ETAs.xlsx   │  │   20260319-ETAs.xlsx   │ 🎚️ Você pode       │
│  └────────────────────────┘  └────────────────────────┘   comparar         │
│                                                       qualquer época        │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│ ▼ ITENS ALTERADOS (5 mudanças)                                              │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  MATRIZ DE CAMARAGIBE — Projeto Hidráulico                                  │
│  ├─ Status Atual:      Pendente ➜ Concluído ✓                              │
│  └─ Evolução:          80% ➜ 100%                                          │
│                                                                               │
│  COLÔNIA LEOPOLDINA — Orçamentos                                             │
│  ├─ Status Atual:      Atrasado ➜ Pendente ⚠                               │
│  └─ Data Estimada:     2026-06-15 ➜ 2026-07-30                            │
│                                                                               │
│  PORTO CALVO — Topografia                                                    │
│  └─ Responsável:       BIANCADE ➜ VERDE                                    │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│ ▼ ITENS ADICIONADOS (2 novos)                                               │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  JACUÍPE — Canafístula I / Sondagens                                         │
│  ├─ Status: Pendente ⚠                                                      │
│  └─ Evolução: 0%                                                             │
│                                                                               │
│  JACUÍPE — Canafístula II / Sondagens                                        │
│  ├─ Status: Pendente ⚠                                                      │
│  └─ Evolução: 0%                                                             │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│ ▼ ITENS REMOVIDOS (0)                                                        │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  (Nenhum item removido nesta comparação)                                     │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## 📰 ABA 3: HISTÓRICO

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  Visão Geral │ Comparativo │ 🔍 Histórico                                     ║
╚═══════════════════════════════════════════════════════════════════════════════╝

┌───────────────────────────────────────────────────────────────────────────────┐
│ 🔎 FILTROS DE PERÍODO                                                        │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Período:                    Tipo:                   Município:              │
│  ┌──────────────────────┐   ┌────────────────────┐  ┌────────────────────┐  │
│  │ ▼ Últimos 3 meses ▼ │   │ ▼ Todos       ▼    │  │ ▼ Todos       ▼    │  │
│  │  Últimas 2 semanas  │   │  ETA               │  │  MATRIZ...         │  │
│  │  Último mês         │   │  Captação          │  │  COLÔNIA...        │  │
│  │  Últimos 3 meses    │   │  ETE               │  │  PORTO CALVO       │  │
│  │  Últimos 6 meses    │   │                    │  │  ...               │  │
│  │  Tudo               │   └────────────────────┘  └────────────────────┘  │
│  └──────────────────────┘                                                   │
│                                                  [Atualizar] [⬇ Exportar .txt]│
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│ 📰 FEED DE ALTERAÇÕES (mais recentes no topo)                               │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  📅 09/06/2026 14:30 — [ETE] COLÔNIA LEOPOLDINA                             │
│     ETE Colônia Leopoldina / Orçamentos                                      │
│     Status: Pendente ⚠ → Concluído ✓                                        │
│                                                                               │
│  📅 09/06/2026 10:15 — [ETA] MATRIZ DE CAMARAGIBE                           │
│     Projeto Hidráulico                                                       │
│     Evolução: 80% → 100% (Completo)                                         │
│                                                                               │
│  📅 08/06/2026 16:45 — [Captação] BRANQUINHA                                │
│     Topografia                                                               │
│     Status: Pendente ⚠ → Atrasado ❌                                        │
│     Responsável: BIANCADE → VERDE                                           │
│                                                                               │
│  📅 07/06/2026 09:30 — [ETE] PORTO CALVO                                    │
│     ETE Porto Calvo / Sondagens                                              │
│     Status: Pendente ⚠ → Concluído ✓                                        │
│     Data Conclusão: 2026-07-15 (realizado em 2026-06-07)                    │
│                                                                               │
│  📅 05/06/2026 14:20 — [ETA] CHAPÉU BAIXO                                   │
│     Projeto Elétrico                                                         │
│     Evolução: 0% → 50% (Em andamento)                                       │
│     Novo Responsável: VERDE                                                  │
│                                                                               │
│  [← Carregar mais histórico →]                                              │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘

📄 ARQUIVO EXPORTADO EXEMPLO (⬇ Exportar .txt):

═══════════════════════════════════════════════════════════════════════════════
[ETE] Histórico de Alterações — 09/06/2026
Filtro: Últimos 3 meses | Município: Todos | Tipo: Todos
═══════════════════════════════════════════════════════════════════════════════

COLÔNIA LEOPOLDINA
  • 09/06/2026 14:30 — ETE Colônia Leopoldina / Orçamentos
    Status: Pendente → Concluído

  • 02/06/2026 11:20 — ETE Colônia Leopoldina / Plano Hidráulico
    Evolução: 0% → 80%

PORTO CALVO
  • 07/06/2026 09:30 — ETE Porto Calvo / Sondagens
    Status: Pendente → Concluído

MATRIZ DE CAMARAGIBE
  • 09/06/2026 10:15 — [ETA] Projeto Hidráulico
    Evolução: 80% → 100%

═══════════════════════════════════════════════════════════════════════════════
```

---

## 🎨 PALETA DE CORES

| Elemento | Cor | Hex | Uso |
|----------|-----|-----|-----|
| Primária | Azul | `#1E6FE8` | Botões, links, tipo Captação |
| ETA | Verde | `#2E9E5B` | Indicador tipo ETA |
| ETE | Laranja | `#E87820` | Indicador tipo ETE |
| Concluído | Verde Claro | `#d4edda` | Fundo linha tabela |
| Pendente | Amarelo Claro | `#fff3cd` | Fundo linha tabela |
| Atrasado | Vermelho Claro | `#f8d7da` | Fundo linha tabela |
| N/A | Cinza | `#e2e3e5` | Fundo linha tabela |
| Fundo | Branco | `#FFFFFF` | Background |
| Fundo Secundário | Cinza Claro | `#F0F2F6` | Cards, sidebar |
| Texto | Escuro | `#1A1A2E` | Corpo texto |

---

## ✨ CARACTERÍSTICAS VISUAIS

### ✅ Em Desenvolvimento
- Tema Streamlit light com paleta profissional
- Layout responsivo (desktop/tablet)
- Filtros interativos (multiselect, slider)
- Componentes reutilizáveis (métricas, gráficos, tabelas)
- Formatação condicional por status

### ⏳ Planejado
- Tooltips explicativos em hover
- Animações suaves de filtro
- Spinner durante carregamento
- Toast messages (sucesso/erro)
- Dark mode opcional (Fase 9)

---

## 🚀 Próximos Passos

1. ✅ Fase 1: Infraestrutura (Este arquivo)
2. ⏳ Fase 2: Parser — ler planilhas reais
3. ⏳ Fase 3: Storage — integrar GitHub
4. ⏳ Fases 4-10: Completar funcionalidades

**Quando chegar à Fase 7**, este preview se tornará a interface real! 🎨
