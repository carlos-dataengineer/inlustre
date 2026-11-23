# Arquitetura

O Inlustre é um único arquivo HTML com CSS e JavaScript próprios, sem framework. Este documento explica como as partes se encaixam.

## Do código ao que a pessoa recebe

```text
src/inlustre.html ─┐
                   ├─ scripts/build.py ─┬─ app/index.html                       documento completo
vendor/rough.min.js┘                    ├─ skills/inlustre/assets/inlustre.html  cópia para a skill
                                        └─ skills/inlustre/assets/inlustre-artifact.html  fragmento para artefato
```

- **`src/inlustre.html`** é o código-fonte. Ele carrega o Rough.js por CDN, o que facilita testar como artefato durante o desenvolvimento.
- **`scripts/build.py`** troca essa tag pelo Rough.js embutido. O resultado funciona sem internet e dentro do claude.ai, que bloqueia scripts externos.
- O **documento completo** tem `<!doctype>`, `<head>` e `<body>`, e abre direto no navegador.
- O **fragmento** não tem essas tags, porque a ferramenta Artifact do Claude envolve a página no próprio esqueleto.

## Como a skill entrega a ferramenta

| Ambiente | Arquivo | Resultado |
|---|---|---|
| Claude com a ferramenta Artifact | `inlustre-artifact.html` | Artefato publicado na conta da pessoa |
| claude.ai sem a ferramenta Artifact | `inlustre.html` | Artefato HTML criado na conversa |
| Codex, terminal, outros agentes | `inlustre.html` | Cópia em `~/Inlustre/` aberta no navegador |

Para um quadro já desenhado, a skill insere `<script>window.INLUSTRE_BOARD = {...}</script>` antes do script principal. Na inicialização, se não houver quadro salvo no navegador, o Inlustre completa os campos que faltam em cada elemento (`hydrate`) e enquadra o desenho.

## Organização do script

O script principal fica dentro de uma função anônima, para não vazar variáveis para a página. As seções seguem esta ordem:

| Seção | Responsabilidade |
|---|---|
| constantes | fontes, paletas, relação entre propriedades e tipos, ícones, atalhos |
| estado | lista `elements`, seleção, visão (`zoom`, `sx`, `sy`), ferramenta atual, padrões de estilo |
| tema | lê as variáveis CSS e resolve as cores com nome para o tema atual |
| elementos | criação, medição de texto, normalização de linhas, limites |
| desenho | geração com Rough.js (com cache por elemento), texto, imagens, grade e seleção |
| acerto | detecção de clique em contorno, área e alças |
| histórico e armazenamento | pilhas de desfazer e refazer com instantâneos JSON, salvamento adiado no `localStorage` |
| interface | barra, painel de estilo, menu, diálogos |
| ponteiro e teclado | eventos de mouse, toque, pinça e atalhos |

## Modelo de dados

Cada elemento é um objeto simples, documentado em [`FORMATO-QUADRO.md`](../skills/inlustre/references/FORMATO-QUADRO.md). Coordenadas ficam no espaço do quadro. A conversão para a tela é `tela = (quadro + scroll) × zoom`.

Linhas, setas e traços de lápis guardam `points` relativos a `x`, `y`. Depois de cada edição, `normalizeLinear` move a origem para o canto superior esquerdo e recalcula `w` e `h`, para que seleção e redimensionamento tratem todos os elementos do mesmo jeito.

## Desenho com Rough.js

O Rough.js gera traços com variação aleatória. Para que um elemento não "trema" a cada quadro, cada um guarda uma `seed` fixa. Os traços gerados ficam em cache, com uma chave que junta forma, tamanho, cores resolvidas e estilo. Mudar o tema muda as cores resolvidas e invalida o cache sozinho.

## Armazenamento

- O quadro é salvo 400 ms depois da última mudança, na chave `ilustre:v1` do `localStorage`.
- Cada artefato ou arquivo tem a própria origem no navegador, então cada um guarda um quadro separado.
- Imagens são reduzidas para no máximo 1600 px antes de entrar no quadro.
- Se o navegador recusar o armazenamento, o Inlustre avisa uma vez e continua funcionando.

A chave mantém o nome original `ilustre:v1` para preservar quadros salvos antes da troca de nome do projeto.
