#!/usr/bin/env bash
# Remove a skill do Inlustre do Claude Code e do Codex.
# Apaga apenas pastas cujo SKILL.md se chama "inlustre". Use --all para remover também ~/Inlustre/inlustre.html.
#   curl -fsSL https://raw.githubusercontent.com/carlos-dataengineer/inlustre/main/uninstall.sh | bash
set -euo pipefail
ALL="${INLUSTRE_UNINSTALL_ALL:-0}"
[ "${1:-}" = "--all" ] && ALL=1
for t in "$HOME/.claude/skills/inlustre" "${CODEX_HOME:-$HOME/.codex}/skills/inlustre" "$HOME/.agents/skills/inlustre"; do
  if [ -f "$t/SKILL.md" ] && grep -Eq '^name:[[:space:]]*inlustre[[:space:]]*$' "$t/SKILL.md"; then
    rm -rf "$t"; echo "  removido: $t"
  fi
done
APP="$HOME/Inlustre/inlustre.html"
if [ "$ALL" = "1" ] && [ -f "$APP" ]; then
  rm -f "$APP"; rmdir "$HOME/Inlustre" 2>/dev/null || true; echo "  removido: $APP"
elif [ -f "$APP" ]; then
  echo "  mantido: $APP (use --all para remover)"
fi
echo "  Inlustre desinstalado."
