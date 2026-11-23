#!/usr/bin/env python3
"""Gera os arquivos distribuídos do Inlustre a partir de src/inlustre.html.

Saídas:
  app/index.html                              documento completo, abre direto no navegador
  skills/inlustre/assets/inlustre.html        cópia do documento completo (usada pela skill)
  skills/inlustre/assets/inlustre-artifact.html  fragmento para publicar como artefato no Claude

Uso:
  python scripts/build.py          gera os arquivos
  python scripts/build.py --check  falha se os arquivos gerados estiverem desatualizados
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "inlustre.html"
LIB = ROOT / "vendor" / "rough.min.js"
CDN_TAG = '<script src="https://cdn.jsdelivr.net/npm/roughjs@4.6.6/bundled/rough.js"></script>'

OUT_APP = ROOT / "app" / "index.html"
OUT_SKILL = ROOT / "skills" / "inlustre" / "assets" / "inlustre.html"
OUT_ARTIFACT = ROOT / "skills" / "inlustre" / "assets" / "inlustre-artifact.html"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def build() -> dict[Path, str]:
    src = read(SRC)
    if CDN_TAG not in src:
        raise SystemExit(f"Tag do rough.js não encontrada em {SRC}")
    inline = "<script>\n" + read(LIB).strip() + "\n</script>"
    fragment = src.replace(CDN_TAG, inline)

    head_end = fragment.index("</style>\n") + len("</style>\n")
    full = (
        "<!doctype html>\n<html lang=\"pt-BR\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
        + fragment[:head_end]
        + "</head>\n<body>\n"
        + fragment[head_end:].rstrip()
        + "\n</body>\n</html>\n"
    )
    return {OUT_APP: full, OUT_SKILL: full, OUT_ARTIFACT: fragment.rstrip() + "\n"}


def main() -> int:
    check = "--check" in sys.argv
    stale = []
    for path, content in build().items():
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current == content:
            continue
        if check:
            stale.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
            print(f"gerado: {path.relative_to(ROOT).as_posix()}")
    if stale:
        print("Arquivos desatualizados. Rode: python scripts/build.py")
        for s in stale:
            print(f"  - {s}")
        return 1
    if check:
        print("Arquivos gerados em dia.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
