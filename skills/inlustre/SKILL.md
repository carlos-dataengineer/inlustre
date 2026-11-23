---
name: inlustre
description: Abre o Inlustre, um quadro de desenho com traço à mão (formas, setas, linhas, lápis, texto, imagens, camadas, zoom e exportação PNG). Use quando a pessoa pedir "inlustre", "abrir o Inlustre", "/inlustre", um quadro branco, um rascunho, um esboço de diagrama, um desenho à mão livre ou um whiteboard para desenhar e explicar ideias. Use também quando ela pedir para desenhar um diagrama simples (fluxo, arquitetura, tabela, mapa de ideias) "no Inlustre".
---

# Inlustre

O Inlustre é uma ferramenta pronta, em um único arquivo HTML. **Nunca reescreva a ferramenta de memória e nunca gere uma versão "parecida"**: use sempre os arquivos da pasta `assets/` ao lado deste `SKILL.md`, sem alterar o código.

| Arquivo | Para quê |
|---|---|
| `assets/inlustre-artifact.html` | Publicar como artefato no Claude (ferramenta Artifact). Fragmento sem `<html>`/`<body>`, como o artefato exige. |
| `assets/inlustre.html` | Documento completo. Abrir no navegador (Codex, terminal) ou colar como artefato HTML no claude.ai. |
| `references/FORMATO-QUADRO.md` | Formato JSON dos elementos, para entregar o quadro já desenhado. |

## 1. Escolha como entregar

Siga a primeira opção que o ambiente permitir.

**A. Claude com a ferramenta Artifact** (Claude Code no app desktop, claude.ai com artefatos publicados)

1. Antes de criar outro, liste os artefatos da pessoa (`action: "list"`). Se já existir um chamado **Inlustre**, ofereça abrir esse (`action: "open"`) em vez de duplicar. Cada artefato guarda o desenho em separado.
2. Para criar: publique `assets/inlustre-artifact.html` com `icon: "pencil"` e a descrição "Quadro de desenho com traço à mão". Se a ferramenta pedir um passo de design, o arquivo já está pronto: não mude o visual.
3. Entregue o link.

**B. claude.ai sem a ferramenta Artifact** (chat com artefatos HTML)

Crie um artefato do tipo HTML cujo conteúdo é **exatamente** o arquivo `assets/inlustre.html`, sem resumir nem cortar.

**C. Codex, Claude Code no terminal ou qualquer agente sem artefatos**

1. Copie `assets/inlustre.html` para `~/Inlustre/inlustre.html`. Crie a pasta se faltar e não sobrescreva um arquivo diferente sem perguntar.
2. Abra no navegador padrão:
   - Windows: `Start-Process "$HOME\Inlustre\inlustre.html"`
   - macOS: `open ~/Inlustre/inlustre.html`
   - Linux: `xdg-open ~/Inlustre/inlustre.html`
3. Diga o caminho do arquivo. O desenho fica salvo no navegador, e pelo menu dá para salvar o JSON.

## 2. Quadro já desenhado (opcional)

Quando a pessoa pedir um desenho pronto ("desenhe meu pipeline no Inlustre"):

1. Monte o JSON dos elementos seguindo `references/FORMATO-QUADRO.md`. Use poucas formas grandes, rótulos curtos e setas entre as formas.
2. Faça uma cópia do arquivo escolhido no passo 1 e insira, logo antes da última `<script>` do arquivo, a linha:
   `<script>window.INLUSTRE_BOARD = {"elements": [ ... ]};</script>`
   Não altere mais nada no arquivo.
3. Entregue a cópia da forma escolhida no passo 1. O quadro abre com o desenho, e a pessoa edita à vontade.

Se não der para entregar um arquivo, passe o JSON para a pessoa colar em **☰ → Salvar / carregar JSON → Carregar**.

## 3. Depois de entregar

Explique em poucas linhas:

- Ferramentas no topo, com atalhos: `V` seleciona, `R` retângulo, `D` losango, `O` elipse, `A` seta, `L` linha, `P` lápis, `T` texto, `E` borracha, `H` move o quadro.
- Duplo clique dentro de uma forma escreve nela. Duplo clique no vazio cria um texto.
- O painel da esquerda muda cor, fundo, espessura, traço, fonte, camadas e alinhamento.
- No menu ☰: abrir e salvar JSON, exportar PNG, grade, tema e limpar o quadro.
- O desenho fica salvo só no navegador da pessoa. Para guardar ou compartilhar, use "Salvar / carregar JSON" ou exporte a imagem.
