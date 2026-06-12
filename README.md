# Dashboard de Acompanhamento de Projetos de Saneamento

Aplicação web interativa para gestão centralizada de planos de ação de projetos de saneamento em Alagoas.

## 🎯 Objetivo

Centralizar o acompanhamento de **planos de ação** de três tipos de projetos:
- **Captações** (21 municípios)
- **ETAs** — Estações de Tratamento de Água (11 municípios)
- **ETEs/EEEs** — Estações de Tratamento de Esgoto (18 localidades, 27 unidades)

Suporte para múltiplas versões históricas (60+), análise comparativa entre épocas e geração automática de feed de notícias com histórico de alterações.

## ✨ Funcionalidades Principais

### 📊 Visualização (Público)
- Upload e gestão de múltiplas versões de planilhas Excel
- Filtros avançados (município, atividade, responsável, status, evolução)
- Painel de métricas: % concluído, % pendente, % não aplicável
- Gráfico de barras por município (status empilhado)
- Tabela com formatação condicional (cores por status)
- Comparação entre versões (padrão: última vs. penúltima, flexibilidade para qualquer época)
- Feed de histórico com filtro por período
- Exportação de histórico em `.txt`

### 🔐 Upload & Exclusão (Autenticado)
- Autenticação simples via senha
- Upload de múltiplos arquivos `.xlsx`
- Identificação automática de tipo de projeto
- Exclusão individual de arquivo
- Commit automático no GitHub (versionamento)

## 🏗️ Arquitetura

```
dashboard-saneamento/
├── app.py                          # Entrada, tabs, sidebar
├── modules/
│   ├── __init__.py
│   ├── parser.py                   # Leitura e normalização Excel
│   ├── comparator.py               # Diff entre versões
│   ├── storage.py                  # GitHub API + session_state
│   ├── visuals.py                  # Componentes Streamlit
│   └── history.py                  # Feed e exportação
├── .streamlit/
│   └── config.toml                 # Configuração de tema
├── requirements.txt                # Dependências
├── .gitignore
└── README.md
```

## 🚀 Quick Start

### 1. Clonar e Setup

```bash
cd dashboard-saneamento
pip install -r requirements.txt
```

### 2. Configurar Secrets (Local)

Criar `.streamlit/secrets.toml`:

```toml
GITHUB_TOKEN = "seu_token_github"
ADMIN_PASSWORD = "sua_senha_admin"
```

### 3. Rodar Localmente

```bash
streamlit run app.py
```

Acesso: http://localhost:8501

### 4. Deploy no Streamlit Cloud

1. Push código para GitHub
2. Conectar repositório em [Streamlit Cloud](https://share.streamlit.io)
3. Configurar secrets em Settings → Secrets
4. App será publicado automaticamente

## 📋 Estrutura de Dados

### Tipos de Planilha

| Tipo | Aba | Header | Municípios | Colunas Especiais |
|------|-----|--------|-----------|------------------|
| **ETA** | `Resumo e Plano Ação` | Linha 3 | 11 | Data Início/Término PE, Status ETA |
| **Captação** | `Plano Ação` | Linha 2 | 23 | - |
| **ETE** | `Plano Ação` | Linha 2 | 40 | Unidade, OBSERVAÇÕES |

### Colunas Normalizadas

```
municipio_filtro, municipio, unidade, atividade, responsavel,
plano_de_acao, evolucao, status_atual, data_entrega_final,
data_estimada, data_conclusao, tipo_projeto
```

### Campo Evolução

| Valor | Significado |
|-------|-------------|
| `1.0` | Concluído (100%) |
| `0.8`, `0.9` | Progresso parcial |
| `0.5` | 50% concluído |
| `0.0` | Pendente (0%) |
| `NaN` | Não aplicável (traço ou vazio) |

## 🎨 Paleta de Cores

| Tipo | Cor | Hex |
|------|-----|-----|
| Captação | Azul | `#1E6FE8` |
| ETA | Verde | `#2E9E5B` |
| ETE | Laranja | `#E87820` |

## 📚 Documentação

- **PRD.md** — Especificação completa do produto
- **CLAUDE.md** — Guia técnico e conhecimento crítico
- **PLAN.md** — Plano de implementação por fases

## 🧪 Testes

```bash
# Verificar estrutura
python -m pytest tests/

# Lint
python -m pylint modules/

# Type check
python -m mypy modules/
```

## 🔧 Desenvolvimento

### Fase Atual
Implementação por fases (ver `PLAN.md`):
1. ✅ Infraestrutura & Setup
2. ⏳ Parser de Planilhas
3. ⏳ Storage (GitHub)
4. ⏳ Visuals & Componentes
5. ⏳ Comparador de Versões
6. ⏳ Histórico & Exportação
7. ⏳ App Principal & Integração
8. ⏳ Autenticação
9. ⏳ Tema & Polimento
10. ⏳ Deploy & Testes

### Contribuir

1. Crie branch feature: `git checkout -b feature/minha-feature`
2. Commit com mensagens claras
3. Push: `git push origin feature/minha-feature`
4. Abra Pull Request

## 📞 Suporte

Para dúvidas ou bugs:
1. Consulte documentação em `PRD.md`, `CLAUDE.md`, `PLAN.md`
2. Verifique logs Streamlit: `.streamlit/logs/`
3. Abra issue no repositório

## 📄 Licença

Desenvolvido para Biancade Engenharia e Construção.

---

**Última atualização:** 2026-06-09  
**Versão:** 1.0.0 (em desenvolvimento)
# redeploy
