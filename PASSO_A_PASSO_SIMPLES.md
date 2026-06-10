# Guia SUPER Simples — Push para GitHub

**Para quando você travou no passo 2**

---

## O que você tem agora?

✅ Repositório criado no GitHub  
✅ Código pronto no seu computador  
❌ Código ainda não está no GitHub

---

## O que precisa fazer

Apenas 4 linhas de comando. Nada mais.

---

## PASSO 1: Abra o PowerShell

1. Pressione `Win + R`
2. Digite `powershell`
3. Aperte Enter

Vai abrir uma janela preta.

---

## PASSO 2: Vá para a pasta do projeto

Cole isto (com Botão direito → Paste):

```powershell
cd "C:\Users\Joelson Cunha\OneDrive - Biancade Engenharia e Construção\CLAUDE AI\plano-de-ação-projetos\dashboard-saneamento"
```

Aperte Enter.

---

## PASSO 3: Execute estas 4 linhas (uma por uma)

### Linha 1:
```powershell
git remote add origin https://github.com/seu_usuario/dashboard-saneamento.git
```
(Trocar `seu_usuario` pelo seu username do GitHub)

Aperte Enter.

---

### Linha 2:
```powershell
git branch -M main
```

Aperte Enter.

---

### Linha 3:
```powershell
git config --global user.email "joelson.cunha@biancade.com.br"
git config --global user.name "Joelson Cunha"
```

Aperte Enter.

---

### Linha 4:
```powershell
git push -u origin main
```

Aperte Enter.

Vai pedir GitHub credentials (usuário e senha ou token).

---

## Pronto!

Se não teve erros vermelhos, funcionou!

Seu código está agora no GitHub em:
```
https://github.com/seu_usuario/dashboard-saneamento
```

---

## Se der erro?

**Erro: "fatal: not a git repository"**
- Significa você não está na pasta correta
- Execute de novo o PASSO 2

**Erro: "fatal: remote origin already exists"**
- Significa que já tentou antes
- Execute: `git remote remove origin`
- Depois execute de novo a Linha 1

**Erro de autenticação (Username/Password)**
- GitHub não aceita mais senha simples
- Criar token: https://github.com/settings/tokens
- Usar token no lugar da senha

---

## Depois disso?

Ir para: **DEPLOY_STREAMLIT_CLOUD.md**

Que é igualmente simples.

---

**Você consegue! 🎉**
