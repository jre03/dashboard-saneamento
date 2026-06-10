# Setup GitHub para Fase 3: Storage

## Visao Geral

A Fase 3 implementa persistencia versionada usando GitHub. Os arquivos sao armazenados no repositorio e sincronizados automaticamente.

## Pre-requisitos

1. **Conta GitHub** — https://github.com (gratuito)
2. **Personal Access Token** — Para API access
3. **Repositorio GitHub** — Sera criado/configurado

## Passo a Passo

### 1. Criar Repositorio GitHub

```bash
# Opcao A: Via GitHub Web UI (mais facil para iniciantes)
# 1. Ir para https://github.com/new
# 2. Nome: dashboard-saneamento
# 3. Descricao: Dashboard de acompanhamento de projetos de saneamento
# 4. Privacidade: Private (recomendado)
# 5. Criar repositorio

# Opcao B: Via GitHub CLI
gh repo create biancade/dashboard-saneamento --private --source=. --remote=origin --push
```

### 2. Gerar Personal Access Token

1. Ir para: https://github.com/settings/tokens
2. Clicar em "Generate new token" → "Generate new token (classic)"
3. Nome: `dashboard-saneamento-token`
4. Selecionar escopos (permissions):
   - [x] `repo` — Acesso completo ao repositorio
   - [x] `read:org` — Ler organizacao
5. Copiar o token (sera mostrado apenas uma vez!)

### 3. Configurar Secrets Localmente

Criar arquivo `.streamlit/secrets.toml`:

```toml
GITHUB_TOKEN = "ghp_seu_token_gerado_aqui"
ADMIN_PASSWORD = "uma_senha_segura_aqui"
```

**IMPORTANTE:**
- Nao compartilhe este arquivo
- Nao commit para Git (ja esta em .gitignore)
- Mude para uma senha forte

### 4. Testar Localmente

```bash
cd dashboard-saneamento

# Rodar Streamlit com secrets
streamlit run app.py

# Ou via linha de comando
python test_storage_fase3.py  # Teste básico (sem GitHub)
```

### 5. Deploy no Streamlit Cloud

Quando pronto para produção:

1. Fazer push do repositorio para GitHub:
   ```bash
   git add .
   git commit -m "Deploy: Fase 3 Storage completa"
   git push -u origin main
   ```

2. Ir para https://share.streamlit.io
3. Conectar repositorio GitHub
4. Selecionar `dashboard-saneamento` repo
5. Configurar secrets:
   - Em Settings → Secrets
   - Adicionar `GITHUB_TOKEN` e `ADMIN_PASSWORD`
6. Deploy!

## Estrutura do Repositorio GitHub

Apos usar o app, o repositorio ficara assim:

```
dashboard-saneamento/
├── data/
│   ├── captacoes/
│   │   ├── 20260602 - Plano-de-Acao_Captacoes.xlsx
│   │   ├── 20260610 - Plano-de-Acao_Captacoes.xlsx
│   │   └── ...
│   ├── etas/
│   │   ├── 20260424 - Plano-de-Acao_ETAs.xlsx
│   │   └── ...
│   └── etes/
│       ├── 20260603 - Plano-de-Acao_ETEs.xlsx
│       └── ...
├── history.json        # Feed de historico (imutavel)
├── metadata.json       # Indice de metadados
├── README.md
├── .gitignore
└── ... (codigo da aplicacao)
```

## Variáveis de Ambiente

| Variavel | Obrigatorio | Padrao | Descricao |
|----------|-----------|--------|-----------|
| `GITHUB_TOKEN` | Sim | - | Personal Access Token do GitHub |
| `ADMIN_PASSWORD` | Sim | - | Senha para upload/exclusao |
| `GITHUB_OWNER` | Nao | `biancade` | Owner do repositorio |
| `GITHUB_REPO` | Nao | `dashboard-saneamento` | Nome do repositorio |

## Troubleshooting

### "Repository not found"
- [ ] Verificar que GITHUB_OWNER esta correto
- [ ] Verificar que GITHUB_REPO existe
- [ ] Verificar que o token tem permissao `repo`

### "Invalid authentication credentials"
- [ ] GITHUB_TOKEN expirou (gerar novo)
- [ ] GITHUB_TOKEN esta errado (copiar novamente)
- [ ] Token foi revogado (regenerar)

### "Permission denied"
- [ ] Token nao tem permissao `repo`
- [ ] Repositorio é privado e token nao acessa
- [ ] Usuario do token nao tem acesso ao repo

### Arquivo nao aparece depois de upload
- [ ] Recarregar pagina (refresh)
- [ ] Verificar no GitHub que arquivo foi commitado
- [ ] Verificar logs no terminal Streamlit

## Seguranca

### Checklist

- [ ] Nao fazer commit de `secrets.toml`
- [ ] Token é privado (nunca compartilhe)
- [ ] Senha de admin é unica e forte
- [ ] Repositorio é privado
- [ ] Apenas usuarios confiáveis tem acesso
- [ ] Revisar logs de commit no GitHub regularmente

### Melhores Praticas

1. **Tokens**: Gerar um novo token para cada aplicacao/ambiente
2. **Passwords**: Usar geradores de senha (ex: 1Password, LastPass)
3. **Commits**: Sempre deixar mensagens claras no GitHub
4. **Rotacao**: Trocar token a cada 6 meses
5. **Auditoria**: Revisar quem acessa o repositorio

## Proximos Passos

- [ ] Criar repositorio GitHub
- [ ] Gerar Personal Access Token
- [ ] Configurar `secrets.toml` localmente
- [ ] Testar uploads/exclusoes
- [ ] Deploy no Streamlit Cloud
- [ ] Configurar secrets no Cloud

## Recursos Uteis

- GitHub Docs: https://docs.github.com
- PyGithub Docs: https://pygithub.readthedocs.io
- Streamlit Secrets: https://docs.streamlit.io/deploy/streamlit-cloud/deploy-your-app/secrets-management
- Personal Access Tokens: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens

---

**Status**: Fase 3 completa! Storage pronto para uso com GitHub.
