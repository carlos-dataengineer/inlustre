#!/usr/bin/env python3
"""Teste de fumaça: abre o Inlustre num navegador real e exercita o básico.

Requer: pip install playwright && python -m playwright install chromium
Uso:    python tests/test_smoke.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
APP = (ROOT / "app" / "index.html").as_uri()


def saved_elements(page):
    page.wait_for_timeout(600)  # o salvamento é adiado em 400 ms
    raw = page.evaluate("localStorage.getItem('ilustre:v1')")
    return json.loads(raw)["elements"] if raw else []


def main() -> int:
    failures: list[str] = []
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception:
            browser = p.chromium.launch(channel="msedge")

        # 1. Abre sem erros e mostra o exemplo
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        errors: list[str] = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.goto(APP)
        page.wait_for_timeout(800)
        if page.title() != "Inlustre":
            failures.append(f"título inesperado: {page.title()!r}")
        if page.locator("#toolbar [data-tool]").count() != 12:
            failures.append("a barra de ferramentas não tem 12 botões")

        # 2. Desenha um retângulo
        page.keyboard.press("r")
        page.mouse.move(900, 600); page.mouse.down(); page.mouse.move(1100, 700, steps=6); page.mouse.up()
        els = saved_elements(page)
        rects = [e for e in els if e["type"] == "rect" and e["w"] > 150]
        if not rects:
            failures.append("o retângulo desenhado não foi salvo")
        if page.locator("#props").is_hidden():
            failures.append("o painel de estilo não apareceu com o retângulo selecionado")

        # 3. Muda o fundo pelo painel
        page.locator('#bgSw [data-color="green"]').click()
        if not any(e["bg"] == "green" for e in saved_elements(page)):
            failures.append("o fundo verde não foi aplicado")

        # 4. Desfaz
        before = len(saved_elements(page))
        page.keyboard.press("Control+z"); page.keyboard.press("Control+z")
        if len(saved_elements(page)) != before - 1:
            failures.append("desfazer não removeu o retângulo")

        # 5. Texto com duplo clique
        page.mouse.dblclick(1000, 720)
        page.keyboard.type("teste de texto")
        page.keyboard.press("Escape")
        if not any(e.get("text") == "teste de texto" for e in saved_elements(page)):
            failures.append("o texto digitado não foi salvo")

        # 6. Exportação gera imagem
        page.locator("#menuBtn").click()
        page.locator('[data-menu="export"]').click()
        src = page.locator("#expImg").get_attribute("src") or ""
        if not src.startswith("data:image/png"):
            failures.append("a exportação não gerou um PNG")
        page.keyboard.press("Escape")

        if errors:
            failures.append("erros no console: " + " | ".join(errors[:3]))
        page.close()

        # 7. Quadro já desenhado por window.INLUSTRE_BOARD
        page = browser.new_page()
        board = {"elements": [{"type": "rect", "x": 0, "y": 0, "w": 200, "h": 100, "label": "Origem"},
                              {"type": "arrow", "x": 210, "y": 50, "points": [[0, 0], [80, 0]]}]}
        page.add_init_script(f"window.INLUSTRE_BOARD = {json.dumps(board)};")
        page.goto(APP)
        page.wait_for_timeout(300)
        page.keyboard.press("ArrowRight")  # força um salvamento sem alterar o quadro de forma relevante
        page.keyboard.press("Control+a"); page.keyboard.press("ArrowLeft")
        els = saved_elements(page)
        if [e["type"] for e in els] != ["rect", "arrow"] or els[0].get("label") != "Origem":
            failures.append(f"INLUSTRE_BOARD não foi carregado: {[e['type'] for e in els]}")
        browser.close()

    if failures:
        print("Falhas no teste de fumaça:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("Teste de fumaça ok.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
