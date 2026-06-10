# Deploy no Streamlit Cloud — Passo a Passo

**Status:** Repositório Git pronto | Código 100% testado | Pronto para Deploy

---

## 🚀 PASSO 1: Criar Repositório no GitHub

### 1.1 Acessar GitHub
- Ir para https://github.com/new
- **Nome do repositório:** `dashboard-saneamento`
- **Descrição:** "Dashboard de Acompanhamento de Projetos de Saneamento"
- **Visibilidade:** Public (necessário para Streamlit Cloud)
- **Inicializar sem README** (já temos um)
- Clicar "Create repository"

### 1.2 Adicionar Remote e Push
```bash
cd dashboard-saneamento

# Substituir seu_usuario pelo seu username do GitHub
git remote add origin https://github.com/seu_usuario/dashboard-saneamento.git
git branch -M main
git push -u origin main
```

**Resultado esperado:** Código aparece no GitHub em poucos segundos.

---

## 🔐 PASSO 2: Criar Token GitHub (para GitHub API)

**Necessário para:** Autenticação no app

### 2.1 Gerar Token
1. Acessar: https://github.com/settings/tokens
2. Clicar "Generate new token" → "Generate new token (classic)"
3. **Token name:** `dashboard-saneamento-api`
4. **Expiration:** 90 days (ou conforme política)
5. **Scopes necessários:** Marcar `repo` (full control of private repositories)
6. Clicar "Generate token"
7. **COPIAR o token completo** (não será exibido novamente!)

**Guardar com segurança:**
```
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 🌐 PASSO 3: Acessar Streamlit Cloud

### 3.1 Criar Conta
1. Acessar https://share.streamlit.io/
2. Se não tem conta: "Sign up"
3. Conectar com GitHub (recomendado)

### 3.2 Deploy Novo App
1. Clicar "Create app"
2. Preencher:
   - **Repository:** `seu_usuario/dashboard-saneamento`
   - **Branch:** `main`
   - **Main file path:** `app.py`
3. Clicar "Deploy"

**Vai levar ~1-2 minutos para o primeiro deploy.**

---

## 🔑 PASSO 4: Configurar Secrets (IMPORTANTE!)

### 4.1 Acessar Settings do App
1. No Streamlit Cloud, clicar no app que foi criado
2. Clicar engrenagem (⚙️) no canto superior direito
3. Selecionar "Settings"

### 4.2 Adicionar Secrets
1. Clicar "Advanced settings"
2. Ir para seção "Secrets"
3. Colar o seguinte no editor:

```toml
GITHUB_TOKEN = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
ADMIN_PASSWORD = "sua_senha_super_segura_aqui"
GITHUB_REPO = "seu_usuario/dashboard-saneamento"
GITHUB_OWNER = "seu_usuario"
```

**Importante:**
- Substituir `ghp_...` pelo token copiado antes
- Usar senha forte e memorável
- Nunca compartilhar estes valores

4. Clicar "Save"
5. App vai fazer reboot automaticamente (~1-2 minutos)

---

## ✅ PASSO 5: Validar Deploy

### 5.1 Verificar Status
- Aguardar a página ficar "Your app is live"
- URL será algo como: `https://share.streamlit.io/seu_usuario/dashboard-saneamento/main/app.py`

### 5.2 Testar Funcionalidades Básicas

**Teste 1: Carregar Dados Locais**
- [ ] Clicar em "Carregar Dados Locais (Teste)"
- [ ] Selecionar tipo de projeto
- [ ] Dados devem carregar com sucesso
- [ ] Painel de métricas deve aparecer
- [ ] Gráfico e tabela devem exibir

**Teste 2: Comparativo**
- [ ] Acessar aba "Comparativo"
- [ ] Clicar "Comparar Versões"
- [ ] Métricas devem aparecer (Alterados, Adicionados, Removidos)

**Teste 3: Histórico**
- [ ] Acessar aba "Histórico"
- [ ] Clicar "Carregar Histórico"
- [ ] Feed deve exibir entradas
- [ ] Filtros devem funcionar
- [ ] Botão "Exportar .txt" deve funcionar

**Teste 4: Autenticação (IMPORTANTE)**
- [ ] Tentar fazer upload SEM senha → deve mostrar warning
- [ ] Digitar senha correta → deve desbloquear upload
- [ ] Fazer upload de um arquivo .xlsx
- [ ] Upload deve processar com sucesso

---

## 🐛 Troubleshooting

### Erro: "Your app is crashing"
**Solução:**
1. Clicar "Manage app"
2. Ir para "Logs"
3. Procurar pela mensagem de erro
4. Verificar se `requirements.txt` está completo
5. Testar localmente: `streamlit run app.py`

### Erro: "Module not found"
**Solução:**
- Ir em Settings → Advanced settings
- Verificar Python version é 3.8+
- Redeployar clicando "Reboot app"

### Erro ao fazer upload
**Solução:**
- Verificar se GITHUB_TOKEN está configurado corretamente
- Testar token em: https://api.github.com/user (com header Authorization: token xxx)
- Repositório deve ser público

### Erro de autenticação
**Solução:**
- Verificar se ADMIN_PASSWORD está sem espaços extras
- Testar com a senha configurada
- Se errou, alterar em Settings → Secrets

---

## 📊 URLs Importantes

| Item | URL |
|------|-----|
| App em Produção | `https://share.streamlit.io/seu_usuario/dashboard-saneamento/main/app.py` |
| Repositório GitHub | `https://github.com/seu_usuario/dashboard-saneamento` |
| Gerenciar App | `https://share.streamlit.io/` (procurar seu app) |
| Documentação Streamlit | https://docs.streamlit.io |

---

## 🔄 Atualizações Futuras

Após fazer qualquer mudança no código:

```bash
# 1. Fazer mudanças localmente
# (editar arquivo, etc)

# 2. Testar localmente
streamlit run app.py

# 3. Commit e push
git add .
git commit -m "Descrição da mudança"
git push origin main

# 4. Streamlit Cloud redeploya automaticamente em ~1-2 minutos
# (não precisa fazer nada!)
```

---

## 📞 Suporte

Caso tenha problemas:
1. Verificar Logs do Streamlit Cloud
2. Testar localmente com `streamlit run app.py`
3. Abrir issue no GitHub
4. Contatar: joelson.cunha@biancade.com.br

---

## ✨ Parabéns!

O Dashboard está pronto para produção. Após completar estes passos, você terá um app web funcional, versionado no GitHub e hospedado no Streamlit Cloud.

**Tempo estimado:** 10-15 minutos

---

**Data de Criação:** 10 de junho de 2026  
**Status:** Pronto para Deploy  
**Versão:** 1.0
