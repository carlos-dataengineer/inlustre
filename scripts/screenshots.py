#!/usr/bin/env python3
"""Gera as capturas de tela do README em docs/images/.

Requer: pip install playwright && python -m playwright install chromium
Uso:    python scripts/screenshots.py
"""
from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

ROOT = Path(__file__).resolve().parent.parent
APP = (ROOT / "app" / "index.html").as_uri()
OUT = ROOT / "docs" / "images"


# ---------- quadros de exemplo ----------
def rect(x, y, w, h, **k):
    return {"type": "rect", "x": x, "y": y, "w": w, "h": h, **k}


def ell(x, y, w, h, **k):
    return {"type": "ellipse", "x": x, "y": y, "w": w, "h": h, **k}


def dia(x, y, w, h, **k):
    return {"type": "diamond", "x": x, "y": y, "w": w, "h": h, **k}


def arrow(x1, y1, x2, y2, **k):
    return {"type": "arrow", "x": x1, "y": y1, "points": [[0, 0], [x2 - x1, y2 - y1]], **k}


def line(x1, y1, x2, y2, **k):
    return {"type": "line", "x": x1, "y": y1, "points": [[0, 0], [x2 - x1, y2 - y1]], **k}


def text(x, y, t, **k):
    return {"type": "text", "x": x, "y": y, "text": t, **k}


def board_architecture():
    els = [text(0, -70, "Pipeline de dados · arquitetura medalhão", size=32)]
    for i, (name, c) in enumerate([("ERP", "blue"), ("CRM", "blue"), ("APIs", "blue")]):
        y = i * 120
        els.append(ell(0, y, 150, 80, bg=c, label=name))
        els.append(arrow(160, y + 40, 250, 170))
    els += [
        rect(260, 120, 180, 100, bg="orange", fill="hachure", label="Bronze\ndado bruto"),
        arrow(450, 170, 520, 170),
        rect(530, 120, 180, 100, bg="none", label="Prata\nlimpo e tipado"),
        arrow(720, 170, 790, 170),
        dia(800, 100, 170, 140, bg="violet", label="testes\npassaram?", size=18),
        arrow(980, 170, 1050, 170),
        text(990, 135, "sim", size=16, stroke="green"),
        rect(1060, 120, 180, 100, bg="yellow", label="Ouro\nmétricas"),
        arrow(1150, 230, 1150, 300),
        rect(1060, 310, 180, 90, bg="green", fill="solid", label="Painéis de BI"),
        arrow(885, 250, 885, 320, dash="dashed", stroke="red"),
        text(895, 262, "não", size=16, stroke="red"),
        rect(800, 330, 170, 70, stroke="red", dash="dashed", label="alerta para\no time", size=18),
        text(260, 260, "Ingestão diária às 6h\nretenção de 90 dias", size=16, opacity=70),
    ]
    return els


def board_class():
    cols = [("ID_Proj", 100, "green"), ("CPF", 80, "green"), ("Nome", 110, "red"), ("Sexo", 70, "red"),
            ("Cidade", 150, "red"), ("UF", 60, "red"), ("Horas", 80, "red")]
    rows = [["A", "111", "Jean", "M", "Porto Alegre", "RS", "50"],
            ["B", "222", "Lia", "F", "Curitiba", "PR", "80"],
            ["C", "333", "Brenda", "F", "São Paulo", "SP", "60"],
            ["B", "111", "Jean", "M", "Porto Alegre", "RS", "25"]]
    x0, y0 = 460, 60
    els = [text(x0 + 200, 10, "pessoas_projetos", size=24)]
    x = x0
    for name, w, c in cols:
        els.append(rect(x, y0, w, 40, round=False, stroke=c, label=name, size=18))
        for r, row in enumerate(rows):
            els.append(rect(x, y0 + 40 + r * 40, w, 40, round=False, stroke="ink", sw=1, label=row[cols.index((name, w, c))], size=18))
        x += w
    els += [
        text(0, 40, "Segunda Forma Normal (2FN)", size=28),
        text(0, 95, "Uma tabela está na 2FN se:\n• já está na 1FN\n• nenhum atributo que não é chave\n  depende só de parte da chave", size=18),
        text(600, 320, "Nome depende só do CPF:\nviolação da 2FN.", size=18, stroke="red"),
        arrow(690, 312, 690, 270, stroke="red", dash="dashed"),
        ell(450, 48, 200, 64, stroke="green", sw=2, rough=2),
        text(250, -20, "chave composta", size=18, stroke="green"),
        arrow(400, 8, 455, 55, stroke="green"),
    ]
    return els


def board_brainstorm():
    els = [ell(380, 220, 240, 130, bg="yellow", fill="solid", label="Lançamento\ndo app", size=28)]
    ideas = [(80, 40, "Vídeo curto\nnas redes", "blue"), (420, 0, "Lista de\nespera", "green"),
             (760, 40, "Parcerias com\ncriadores", "violet"), (800, 320, "Cupom de\nprimeira compra", "red"),
             (420, 460, "Pesquisa com\n20 usuários", "green"), (60, 330, "Página de\nperguntas", "blue")]
    for x, y, t, c in ideas:
        els.append(rect(x, y, 190, 90, bg=c, label=t, size=18))
        cx, cy = x + 95, y + 45
        els.append(line(500 + (cx - 500) * 0.38, 285 + (cy - 285) * 0.38, cx + (500 - cx) * 0.42, cy + (285 - cy) * 0.42, sw=1))
    els += [
        text(0, -60, "Ideias para a semana 1", size=32),
        text(1010, 60, "prioridade!", size=20, stroke="red"),
        arrow(1030, 95, 960, 330, stroke="red"),
        ell(770, 300, 250, 130, stroke="red", bg="none", rough=2, sw=2),
    ]
    return els


def board_wireframe():
    els = [
        text(0, -60, "Tela de cadastro · rascunho v1", size=30),
        rect(0, 0, 340, 620, round=True, sw=2),
        rect(20, 20, 300, 50, bg="blue", label="Criar conta", size=20),
        rect(20, 100, 300, 140, round=False, dash="dashed"),
        line(20, 100, 320, 240, sw=1), line(320, 100, 20, 240, sw=1),
        text(30, 260, "Nome", size=16), rect(20, 285, 300, 44, round=False, sw=1),
        text(30, 345, "E-mail", size=16), rect(20, 370, 300, 44, round=False, sw=1),
        text(30, 430, "Senha", size=16), rect(20, 455, 300, 44, round=False, sw=1),
        rect(20, 530, 300, 56, bg="green", fill="solid", label="Cadastrar", size=20),
        text(420, 150, "ilustração ou foto\ndo produto", size=20, stroke="red"),
        arrow(410, 175, 330, 175, stroke="red"),
        text(420, 380, "validar e-mail\nenquanto digita", size=20, stroke="red"),
        arrow(410, 395, 330, 392, stroke="red"),
        text(420, 545, "botão desabilitado\naté preencher tudo", size=20, stroke="red"),
        arrow(410, 560, 330, 558, stroke="red"),
    ]
    return els


# ---------- capturas ----------
def open_app(page: Page, board=None):
    if board is not None:
        page.add_init_script(f"window.INLUSTRE_BOARD = {json.dumps({'elements': board}, ensure_ascii=False)};")
    page.goto(APP)
    page.wait_for_function("document.fonts && document.fonts.status === 'loaded'")
    page.wait_for_timeout(900)


def shot(page: Page, name: str):
    OUT.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(OUT / name))
    print("ok", name)


def main():
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception:
            browser = p.chromium.launch(channel="msedge")

        def ctx(scheme="light", w=1440, h=900, mobile=False):
            return browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=2 if not mobile else 3,
                                       color_scheme=scheme, is_mobile=mobile, has_touch=mobile, locale="pt-BR")

        c = ctx(); pg = c.new_page(); open_app(pg); shot(pg, "inicio.png")
        pg.locator("#toolbar").screenshot(path=str(OUT / "barra-ferramentas.png")); print("ok barra-ferramentas.png")
        pg.keyboard.press("r")
        pg.mouse.move(1110, 640); pg.mouse.down(); pg.mouse.move(1330, 760, steps=8); pg.mouse.up()
        pg.locator('#bgSw [data-color="violet"]').click()
        pg.locator('#props [data-prop="fill"] [data-val="cross"]').click()
        shot(pg, "painel-estilo.png")
        pg.locator("#props").screenshot(path=str(OUT / "painel.png")); print("ok painel.png")
        pg.keyboard.press("Escape")
        pg.locator("#menuBtn").click(); pg.wait_for_timeout(150); shot(pg, "menu.png")
        pg.locator('[data-menu="export"]').click(); pg.wait_for_timeout(400); shot(pg, "exportar.png")
        pg.keyboard.press("Escape")
        pg.locator("#helpBtn").click(); pg.wait_for_timeout(150); shot(pg, "atalhos.png")
        c.close()

        c = ctx("dark"); pg = c.new_page(); open_app(pg); shot(pg, "tema-escuro.png"); c.close()

        for name, board, scheme in [("caso-arquitetura.png", board_architecture(), "light"),
                                    ("caso-aula.png", board_class(), "dark"),
                                    ("caso-brainstorm.png", board_brainstorm(), "light"),
                                    ("caso-wireframe.png", board_wireframe(), "light")]:
            c = ctx(scheme); pg = c.new_page(); open_app(pg, board); shot(pg, name); c.close()

        c = ctx("light", 390, 844, mobile=True); pg = c.new_page(); open_app(pg); shot(pg, "celular.png"); c.close()
        browser.close()


if __name__ == "__main__":
    main()
