# Guia de Deploy — Dashboard Saneamento

## Deploy no Streamlit Community Cloud

### Pré-requisitos

- ✅ Conta no GitHub com o repositório do projeto
- ✅ Conta no [Streamlit Community Cloud](https://streamlit.io/cloud)
- ✅ Token de acesso GitHub (para API access)
- ✅ Senha admin para upload/exclusão

### Passo 1: Preparar Repositório GitHub

```bash
# 1. Inicializar repositório (se não existir)
git init
git remote add origin https://github.com/seu_usuario/dashboard-saneamento.git

# 2. Adicionar e commitar arquivos
git add .
git commit -m "Fase 10: Deploy & Testes - Dashboard pronto para produção"

# 3. Push para GitHub
git push -u origin main
```

### Passo 2: Configurar Streamlit Cloud

1. Acessar https://share.streamlit.io/
2. Clicar em "New app"
3. Preencher:
   - **Repository:** seu_usuario/dashboard-saneamento
   - **Branch:** main
   - **Main file path:** app.py
4. Clicar "Deploy"

### Passo 3: Configurar Secrets

Na página de settings do app no Streamlit Cloud:

1. Acessar **Advanced settings** → **Secrets**
2. Copiar conteúdo de `.streamlit/secrets.toml`:

```toml
GITHUB_TOKEN = "seu_token_github"
ADMIN_PASSWORD = "sua_senha_segura"
GITHUB_REPO = "seu_usuario/dashboard-saneamento"
GITHUB_OWNER = "seu_usuario"
```

### Passo 4: Verificar Deploy

- URL do app: `https://share.streamlit.io/seu_usuario/dashboard-saneamento/main/app.py`
- Status: deve mostrar "Your app is live!"
- Teste básico: carregue dados locais na sidebar

### Troubleshooting

#### App não carrega
- ✅ Verificar `requirements.txt` está correto
- ✅ Verificar sintaxe do Python (use `python -m py_compile app.py`)
- ✅ Ver logs do Streamlit Cloud

#### Erro ao fazer upload
- ✅ Verificar `GITHUB_TOKEN` está correto e tem permissão `repo`
- ✅ Verificar repositório existe e é acessível
- ✅ Verificar caminho da aba Excel (pode variar por versão)

#### Erro de autenticação
- ✅ Verificar `ADMIN_PASSWORD` foi definida corretamente
- ✅ Verificar não há espaços extras no secret

### Monitoramento Pós-Deploy

1. **Performance**
   - Observar tempo de carregamento
   - Verificar uso de memória no Streamlit Cloud dashboard

2. **Funcionalidade**
   - Teste: Upload de arquivo
   - Teste: Comparação de versões
   - Teste: Filtro de histórico
   - Teste: Exportação de TXT

3. **Segurança**
   - Autenticação funcionando (senha bloqueando upload)
   - Dados não são expostos publicamente
   - HTTPS ativado (padrão do Streamlit Cloud)

### Atualizações Futuras

Para atualizar o app em produção:

```bash
# 1. Fazer mudanças localmente
# 2. Testar com: streamlit run app.py
# 3. Commitar e push:
git add .
git commit -m "Descrição da mudança"
git push origin main
# 4. Streamlit Cloud redeploya automaticamente em ~1-2 minutos
```

---

**Versão:** 1.0 | **Data:** 2026-06-10 | **Status:** Pronto para Deploy
