# Push SUPER Simples — Passo a Passo Visual

Se o script não funcionou, vamos fazer manualmente, bem devagar.

---

## ANTES DE COMEÇAR

Você precisa de:
1. **Username do GitHub** (não é o email)
   - Exemplo: `joelsoncunha`
   - Encontrar em: https://github.com/seu_username

2. **Token do GitHub** (é como uma senha)
   - Criar em: https://github.com/settings/tokens
   - Clique em "Generate new token (classic)"
   - Marque `repo`
   - Clique "Generate token"
   - **COPIE o token completo**

---

## PASSO 1: Abrir PowerShell

1. Pressione: `Win + R`
2. Digite: `powershell`
3. Aperte: Enter

Vai abrir uma janela preta (PowerShell).

---

## PASSO 2: Colar este comando

Cole no PowerShell (botão direito → Paste):

```
cd "C:\Users\Joelson Cunha\OneDrive - Biancade Engenharia e Construção\CLAUDE AI\plano-de-ação-projetos\dashboard-saneamento"
```

Aperte: **Enter**

Deve aparecer algo como: `PS C:\...dashboard-saneamento>`

---

## PASSO 3: Digitar seu username e token

Execute isto (copie e cole):

```
git config user.name "Joelson Cunha"
```

Aperte: **Enter**

Depois copie e cole isto:

```
git config user.email "joelson.cunha@biancade.com.br"
```

Aperte: **Enter**

---

## PASSO 4: Adicionar repositório GitHub

Copie e cole isto (SUBSTITUA `seu_username`):

```
git remote add origin https://github.com/seu_username/dashboard-saneamento.git
```

Por exemplo, se seu username é `joelsoncunha`:

```
git remote add origin https://github.com/joelsoncunha/dashboard-saneamento.git
```

Aperte: **Enter**

---

## PASSO 5: Renomear a branch

Copie e cole:

```
git branch -M main
```

Aperte: **Enter**

---

## PASSO 6: FAZER O PUSH (enviar código)

Copie e cole:

```
git push -u origin main
```

Aperte: **Enter**

---

## AGORA PRESTA ATENÇÃO!

Vai aparecer algo pedindo **Username** e **Password**:

```
Username for 'https://github.com': 
```

**NÃO é seu email!** É seu username (exemplo: `joelsoncunha`)

Digite seu username e aperte Enter.

---

## Depois vai pedir Password:

```
Password for 'https://joelsoncunha@github.com': 
```

**NÃO é sua senha da conta do GitHub!** 

É o **TOKEN** que você copiou antes!

Cole o token e aperte Enter.

(Não vai aparecer nada sendo digitado, é normal)

---

## PRONTO!

Se não tiver erros vermelhos, funcionou! 🎉

Seu código está agora em:
```
https://github.com/seu_username/dashboard-saneamento
```

---

## Se der erro?

**IMPORTANTE: Me manda a mensagem de erro exata!**

Copia e manda para que eu possa ajudar.

---

## Próximo passo depois disso?

Deploy em Streamlit Cloud:
https://share.streamlit.io/

(Mas só depois que o código estiver no GitHub)
