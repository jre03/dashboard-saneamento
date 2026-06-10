# Script Automático - Push para GitHub
# Copie e cole isto no PowerShell

Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║          PUSH AUTOMÁTICO PARA GITHUB                      ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# PASSO 1: Ir para a pasta
Write-Host "PASSO 1: Navegando para a pasta do projeto..." -ForegroundColor Yellow
cd "C:\Users\Joelson Cunha\OneDrive - Biancade Engenharia e Construção\CLAUDE AI\plano-de-ação-projetos\dashboard-saneamento"
Write-Host "OK - Pasta correta ✓" -ForegroundColor Green
Write-Host ""

# PASSO 2: Configurar Git
Write-Host "PASSO 2: Configurando Git..." -ForegroundColor Yellow
git config user.email "joelson.cunha@biancade.com.br"
git config user.name "Joelson Cunha"
Write-Host "OK - Git configurado ✓" -ForegroundColor Green
Write-Host ""

# PASSO 3: Adicionar repositório
Write-Host "PASSO 3: Adicionando repositório GitHub..." -ForegroundColor Yellow
Write-Host ""
Write-Host "⚠️  ATENÇÃO: Digite seu username do GitHub!" -ForegroundColor Red
Write-Host "Exemplo: joelsoncunha" -ForegroundColor Yellow
Write-Host ""
$username = Read-Host "Seu username do GitHub"

if ($username -eq "") {
    Write-Host "❌ Erro: Username não pode estar vazio!" -ForegroundColor Red
    exit
}

$repo_url = "https://github.com/$username/dashboard-saneamento.git"
Write-Host "URL do repositório: $repo_url" -ForegroundColor Cyan

git remote remove origin 2>$null
git remote add origin $repo_url

Write-Host "OK - Repositório adicionado ✓" -ForegroundColor Green
Write-Host ""

# PASSO 4: Renomear branch
Write-Host "PASSO 4: Preparando branch..." -ForegroundColor Yellow
git branch -M main
Write-Host "OK - Branch main criada ✓" -ForegroundColor Green
Write-Host ""

# PASSO 5: Push
Write-Host "PASSO 5: Fazendo push para GitHub..." -ForegroundColor Yellow
Write-Host ""
Write-Host "⚠️  ATENÇÃO: GitHub pedirá credenciais!" -ForegroundColor Red
Write-Host "Se usar token, copie e cole no campo de senha." -ForegroundColor Yellow
Write-Host ""

git push -u origin main

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║              ✅ PUSH CONCLUÍDO COM SUCESSO!               ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "Seu código está agora em:" -ForegroundColor Cyan
Write-Host "https://github.com/$username/dashboard-saneamento" -ForegroundColor Cyan
Write-Host ""
Write-Host "Próximo passo: Deploy em Streamlit Cloud" -ForegroundColor Yellow
Write-Host "Ver: DEPLOY_STREAMLIT_CLOUD.md" -ForegroundColor Yellow
