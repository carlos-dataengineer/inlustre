<#
.SYNOPSIS
  Instala o Inlustre: a skill para Claude Code e Codex, e a ferramenta pronta no computador.

.DESCRIPTION
  1. Baixa o Inlustre do GitHub (ou usa a pasta local, se rodar de um clone).
  2. Instala a skill "inlustre" em:
       ~/.claude/skills/inlustre      (Claude Code)
       ~/.codex/skills/inlustre       (Codex; respeita CODEX_HOME)
       ~/.agents/skills/inlustre      (pasta de skills compartilhada entre agentes)
  3. Gera a ferramenta em ~/Inlustre/inlustre.html e abre no navegador.

.EXAMPLE
  irm https://raw.githubusercontent.com/carlos-dataengineer/inlustre/main/install.ps1 | iex

.EXAMPLE
  .\install.ps1 -NoOpen -SkipCodex

.NOTES
  Quando rodar via "irm | iex", use variaveis de ambiente no lugar dos parametros:
    $env:INLUSTRE_NO_OPEN = '1'; $env:INLUSTRE_SKIP_CODEX = '1'; $env:INLUSTRE_SKIP_CLAUDE = '1'; $env:INLUSTRE_REF = 'v1.0.0'
#>
[CmdletBinding()]
param(
  [switch]$NoOpen,
  [switch]$SkipClaude,
  [switch]$SkipCodex,
  [string]$Ref = ''
)

$ErrorActionPreference = 'Stop'
$Repo = 'carlos-dataengineer/inlustre'

if ($env:INLUSTRE_NO_OPEN -eq '1') { $NoOpen = $true }
if ($env:INLUSTRE_SKIP_CLAUDE -eq '1') { $SkipClaude = $true }
if ($env:INLUSTRE_SKIP_CODEX -eq '1') { $SkipCodex = $true }
if (-not $Ref) { $Ref = if ($env:INLUSTRE_REF) { $env:INLUSTRE_REF } else { 'main' } }

function Write-Step([string]$Text) { Write-Host "  > $Text" -ForegroundColor Cyan }
function Write-Ok([string]$Text) { Write-Host "  ok $Text" -ForegroundColor Green }

Write-Host ''
Write-Host '  Inlustre - quadro de desenho com traco a mao' -ForegroundColor White
Write-Host ''

# 1. Origem dos arquivos ------------------------------------------------------
$temp = $null
$localRoot = if ($PSScriptRoot) { $PSScriptRoot } else { $null }
if ($localRoot -and (Test-Path (Join-Path $localRoot 'skills/inlustre/SKILL.md'))) {
  $root = $localRoot
  Write-Step "Usando os arquivos locais em $root"
} else {
  try { [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12 } catch {}
  $temp = Join-Path ([IO.Path]::GetTempPath()) ("inlustre-" + [guid]::NewGuid().ToString('N'))
  New-Item -ItemType Directory -Path $temp | Out-Null
  $zip = Join-Path $temp 'inlustre.zip'
  $kind = if ($Ref -match '^v\d') { 'tags' } else { 'heads' }
  $url = "https://codeload.github.com/$Repo/zip/refs/$kind/$Ref"
  Write-Step "Baixando $Repo ($Ref)"
  Invoke-WebRequest -Uri $url -OutFile $zip -UseBasicParsing
  Expand-Archive -Path $zip -DestinationPath $temp -Force
  $root = Get-ChildItem -Path $temp -Directory | Where-Object { Test-Path (Join-Path $_.FullName 'skills/inlustre/SKILL.md') } | Select-Object -First 1 -ExpandProperty FullName
  if (-not $root) { throw 'O pacote baixado nao tem skills/inlustre/SKILL.md.' }
}
$skillSrc = Join-Path $root 'skills/inlustre'

# 2. Skill ------------------------------------------------------------------
function Install-Skill([string]$Target, [string]$Label) {
  if (Test-Path $Target) {
    $manifest = Join-Path $Target 'SKILL.md'
    $isOurs = (Test-Path $manifest) -and ((Get-Content $manifest -Raw -Encoding UTF8) -match '(?m)^name:\s*inlustre\s*$')
    if (-not $isOurs) {
      Write-Warning "$Target ja existe e nao parece ser o Inlustre. Pulei $Label para nao apagar nada."
      return
    }
    Remove-Item -Path $Target -Recurse -Force
  }
  New-Item -ItemType Directory -Path (Split-Path $Target -Parent) -Force | Out-Null
  Copy-Item -Path $skillSrc -Destination $Target -Recurse -Force
  Write-Ok "Skill instalada para $Label em $Target"
}

$installed = @()
if (-not $SkipClaude) {
  Install-Skill (Join-Path $HOME '.claude/skills/inlustre') 'Claude Code'
  $installed += 'Claude Code'
}
if (-not $SkipCodex) {
  $codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
  Install-Skill (Join-Path $codexHome 'skills/inlustre') 'Codex'
  Install-Skill (Join-Path $HOME '.agents/skills/inlustre') 'agentes (pasta compartilhada)'
  $installed += 'Codex'
}

# 3. Ferramenta pronta ---------------------------------------------------------
$appDir = Join-Path $HOME 'Inlustre'
New-Item -ItemType Directory -Path $appDir -Force | Out-Null
$appFile = Join-Path $appDir 'inlustre.html'
Copy-Item -Path (Join-Path $skillSrc 'assets/inlustre.html') -Destination $appFile -Force
Write-Ok "Ferramenta gerada em $appFile"

if (-not $NoOpen) {
  try { Start-Process $appFile; Write-Ok 'Aberta no navegador' } catch { Write-Warning "Nao consegui abrir o navegador. Abra manualmente: $appFile" }
}

if ($temp) { Remove-Item -Path $temp -Recurse -Force -ErrorAction SilentlyContinue }

# 4. Proximos passos --------------------------------------------------------------
Write-Host ''
Write-Host '  Pronto. Como usar:' -ForegroundColor White
if ($installed -contains 'Claude Code') { Write-Host '    Claude Code  peca "abrir o Inlustre" ou digite /inlustre' }
if ($installed -contains 'Codex') { Write-Host '    Codex        peca "abra o Inlustre" ou digite $inlustre' }
Write-Host "    Navegador    $appFile"
Write-Host ''
Write-Host '  Abra uma nova conversa para o agente reconhecer a skill.' -ForegroundColor DarkGray
Write-Host ''
