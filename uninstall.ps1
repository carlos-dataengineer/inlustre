<#
.SYNOPSIS
  Remove a skill do Inlustre do Claude Code e do Codex.
.DESCRIPTION
  Apaga apenas pastas cujo SKILL.md se chama "inlustre". A ferramenta em ~/Inlustre fica,
  a menos que voce use -All. Os desenhos salvos no navegador nao sao tocados.
.EXAMPLE
  irm https://raw.githubusercontent.com/carlos-dataengineer/inlustre/main/uninstall.ps1 | iex
.EXAMPLE
  .\uninstall.ps1 -All
#>
[CmdletBinding()]
param([switch]$All)
$ErrorActionPreference = 'Stop'
if ($env:INLUSTRE_UNINSTALL_ALL -eq '1') { $All = $true }

$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
$targets = @(
  (Join-Path $HOME '.claude/skills/inlustre'),
  (Join-Path $codexHome 'skills/inlustre'),
  (Join-Path $HOME '.agents/skills/inlustre')
)
foreach ($t in $targets) {
  $m = Join-Path $t 'SKILL.md'
  if ((Test-Path $m) -and ((Get-Content $m -Raw -Encoding UTF8) -match '(?m)^name:\s*inlustre\s*$')) {
    Remove-Item -Path $t -Recurse -Force
    Write-Host "  removido: $t"
  }
}
$app = Join-Path $HOME 'Inlustre/inlustre.html'
if ($All -and (Test-Path $app)) {
  Remove-Item -Path $app -Force
  $dir = Split-Path $app -Parent
  if (-not (Get-ChildItem -Path $dir -Force)) { Remove-Item -Path $dir -Force }
  Write-Host "  removido: $app"
} elseif (Test-Path $app) {
  Write-Host "  mantido: $app (use -All para remover)"
}
Write-Host '  Inlustre desinstalado.'
