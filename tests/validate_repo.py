#!/usr/bin/env python3
"""Validações estáticas do repositório (sem navegador).

Confere: manifesto da skill, manifestos do plugin, versão consistente,
arquivos gerados presentes, instaladores em ASCII sem BOM e imagens do README.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors: list[str] = []


def check(cond: bool, msg: str) -> None:
    if not cond:
        errors.append(msg)


# Skill
skill = (ROOT / "skills/inlustre/SKILL.md").read_text(encoding="utf-8")
m = re.match(r"^---\n(.*?)\n---\n", skill, re.S)
check(bool(m), "SKILL.md sem frontmatter YAML")
if m:
    front = dict(re.findall(r"^(\w+):\s*(.+)$", m.group(1), re.M))
    check(front.get("name") == "inlustre", "SKILL.md: name deve ser 'inlustre'")
    desc = front.get("description", "")
    check(20 <= len(desc) <= 1024, "SKILL.md: description deve ter entre 20 e 1024 caracteres")
for ref in re.findall(r"`((?:assets|references)/[^`]+)`", skill):
    check((ROOT / "skills/inlustre" / ref).exists(), f"SKILL.md cita {ref}, que não existe")

# Plugin e versão
version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
plugin = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
check(plugin.get("name") == "inlustre", "plugin.json: name deve ser 'inlustre'")
check(plugin.get("version") == version, f"plugin.json: versão {plugin.get('version')} difere de VERSION {version}")
entries = [p for p in market.get("plugins", []) if p.get("name") == "inlustre"]
check(len(entries) == 1, "marketplace.json: precisa de uma entrada 'inlustre'")
if entries:
    check(entries[0].get("version") == version, "marketplace.json: versão difere de VERSION")
check(f"[{version}]" in (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"), f"CHANGELOG.md sem a versão {version}")

# Arquivos gerados
for rel in ["app/index.html", "skills/inlustre/assets/inlustre.html", "skills/inlustre/assets/inlustre-artifact.html"]:
    p = ROOT / rel
    check(p.exists(), f"{rel} não existe (rode python scripts/build.py)")
    if p.exists():
        html = p.read_text(encoding="utf-8")
        check("cdn.jsdelivr.net" not in html, f"{rel} ainda carrega o rough.js de fora")
        check("var rough=" in html, f"{rel} sem o rough.js embutido")
        check("<title>Inlustre</title>" in html, f"{rel} sem o título Inlustre")
artifact = (ROOT / "skills/inlustre/assets/inlustre-artifact.html").read_text(encoding="utf-8")
check(not re.search(r"<!doctype|<html|<body", artifact, re.I), "inlustre-artifact.html não pode ter doctype/html/body")

# Instaladores
for rel in ["install.ps1", "uninstall.ps1"]:
    raw = (ROOT / rel).read_bytes()
    check(not raw.startswith(b"\xef\xbb\xbf"), f"{rel} não pode ter BOM (quebra o irm | iex)")
    check(all(b < 128 for b in raw), f"{rel} precisa ser ASCII puro (Windows PowerShell 5.1)")
for rel in ["install.sh", "uninstall.sh"]:
    raw = (ROOT / rel).read_bytes()
    check(raw.startswith(b"#!/usr/bin/env bash"), f"{rel} sem shebang")
    check(b"\r\n" not in raw, f"{rel} precisa de quebras de linha LF")

# Imagens do README
readme = (ROOT / "README.md").read_text(encoding="utf-8")
for img in re.findall(r'src="(docs/images/[^"]+)"', readme):
    check((ROOT / img).exists(), f"README cita {img}, que não existe")
for link in re.findall(r"\]\(((?!https?://|#)[^)]+)\)", readme):
    check((ROOT / link.split("#")[0]).exists(), f"README aponta para {link}, que não existe")

if errors:
    print("Falhas:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
print("Repositório válido.")
