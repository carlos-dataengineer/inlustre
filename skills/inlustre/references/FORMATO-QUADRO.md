# Formato do quadro do Inlustre

Um quadro é um objeto `{"type": "ilustre", "version": 1, "elements": [...]}`. A ordem da lista é a ordem das camadas: o último elemento fica por cima. O mesmo formato serve para três coisas:

- o JSON de **☰ → Salvar / carregar JSON**;
- um arquivo `.json` aberto por **☰ → Abrir arquivo…**;
- o valor de `window.INLUSTRE_BOARD`, que faz o quadro abrir já desenhado.

## Campos

Só `type`, `x` e `y` são obrigatórios. O que faltar recebe o padrão da tabela.

| Campo | Tipos | Padrão | Significado |
|---|---|---|---|
| `type` | todos | — | `rect`, `diamond`, `ellipse`, `arrow`, `line`, `draw`, `text`, `image` |
| `x`, `y` | todos | — | canto superior esquerdo, em pixels do quadro |
| `w`, `h` | formas, imagem | 0 | largura e altura. Em `text`, o Inlustre calcula sozinho. |
| `points` | `arrow`, `line`, `draw` | — | lista `[[x, y], ...]` relativa a `x`, `y` |
| `label` | formas | `""` | texto centralizado dentro da forma. Use `\n` para quebrar linha. |
| `text` | `text` | `""` | conteúdo do texto, com `\n` para quebrar linha |
| `stroke` | todos menos imagem | `"ink"` | `ink` (cor do tema), `red`, `green`, `blue`, `orange`, `violet` ou um hex `#rrggbb` |
| `bg` | formas | `"none"` | `none`, `red`, `green`, `blue`, `yellow`, `violet` ou hex |
| `fill` | formas | `"hachure"` | `hachure`, `cross`, `solid` |
| `sw` | traços | `2` | espessura: `1`, `2` ou `4` |
| `dash` | formas, setas, linhas | `"solid"` | `solid`, `dashed`, `dotted` |
| `rough` | formas, setas, linhas | `1` | traço à mão: `0` preciso, `1` esboço, `2` rabisco |
| `round` | `rect`, `diamond` | `true` | cantos arredondados |
| `startHead`, `endHead` | `arrow` | `false`, `true` | pontas da seta |
| `font` | texto, rótulos | `"hand"` | `hand`, `sans`, `mono` |
| `size` | texto, rótulos | `20` | tamanho da fonte em px. Os botões usam 16, 20, 28 e 36. |
| `align` | `text` | `"left"` | `left`, `center`, `right` |
| `opacity` | todos | `100` | de 10 a 100 |
| `src` | `image` | — | imagem em `data:` URL |

As cores com nome (`red`, `blue`…) se ajustam ao tema claro e escuro. Um hex fica fixo.

## Exemplo: pipeline em três etapas

```json
{
  "type": "ilustre",
  "version": 1,
  "elements": [
    {"type": "text", "x": 80, "y": 30, "text": "Pipeline de vendas", "size": 36},
    {"type": "rect", "x": 80, "y": 120, "w": 200, "h": 100, "bg": "blue", "label": "Origem\nERP"},
    {"type": "rect", "x": 380, "y": 120, "w": 200, "h": 100, "bg": "yellow", "label": "Tratamento\nSpark"},
    {"type": "rect", "x": 680, "y": 120, "w": 200, "h": 100, "bg": "green", "label": "Painel\nBI"},
    {"type": "arrow", "x": 290, "y": 170, "points": [[0, 0], [80, 0]]},
    {"type": "arrow", "x": 590, "y": 170, "points": [[0, 0], [80, 0]]}
  ]
}
```

## Dicas de composição

- Formas de 180 a 240 de largura e 90 a 120 de altura, com 80 a 120 de espaço entre elas.
- Rótulos de até três linhas curtas. Com `size` 20, cada linha ocupa 25 px de altura.
- Uma seta começa cerca de 10 px fora da borda da forma de origem e termina 10 px antes da forma de destino.
- Use `dash: "dashed"` para relações opcionais e `bg` para separar grupos por cor.
