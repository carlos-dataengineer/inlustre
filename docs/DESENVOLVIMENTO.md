# Desenvolvimento

## Ciclo de uma alteração

1. Edite `src/inlustre.html`.
2. Gere os arquivos distribuídos:
   ```bash
   python scripts/build.py
   ```
3. Abra `app/index.html` no navegador e teste. Para começar com o exemplo de novo, limpe o armazenamento do site nas ferramentas do navegador.
4. Rode os testes:
   ```bash
   python tests/validate_repo.py
   python tests/test_smoke.py
   ```
5. Se a interface mudou, regenere as imagens do README:
   ```bash
   python scripts/screenshots.py
   ```

## Testar a skill sem publicar

Rode o instalador de dentro do clone. Ele usa os arquivos locais em vez de baixar do GitHub:

```bash
./install.sh --no-open      # macOS / Linux
.\install.ps1 -NoOpen       # Windows
```

Abra uma nova conversa no Claude Code ou no Codex e peça "abrir o Inlustre".

## Testar o plugin do Claude Code localmente

```text
/plugin marketplace add ./caminho/para/inlustre
/plugin install inlustre@inlustre
```

## Lançar uma versão

1. Atualize `VERSION`, a versão em `.claude-plugin/plugin.json` e em `.claude-plugin/marketplace.json`.
2. Mova as entradas de "Não lançado" para uma nova seção no `CHANGELOG.md`.
3. Faça o commit e crie a tag:
   ```bash
   git tag v1.1.0
   git push origin main --tags
   ```
4. O workflow `release.yml` confere a versão, empacota `inlustre-skill.zip` (para o claude.ai) e `inlustre.html`, e cria a release com as notas do CHANGELOG.

## Regras para os instaladores

- Escrevem apenas nas pastas documentadas no README.
- Só apagam uma pasta de skill existente quando o `SKILL.md` dela tem `name: inlustre`.
- Os `.ps1` ficam em ASCII puro, sem BOM e com CRLF. Um BOM quebra o `irm | iex`, e acentos sem BOM aparecem errados no Windows PowerShell 5.1. O `tests/validate_repo.py` confere isso.
