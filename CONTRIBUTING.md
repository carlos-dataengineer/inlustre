# Como contribuir

Obrigado pelo interesse em melhorar o Inlustre. Este guia mostra o caminho de uma contribuição, do primeiro passo ao pull request.

## Antes de começar

- Procure nas [issues](https://github.com/carlos-dataengineer/inlustre/issues) se o assunto já está sendo tratado.
- Para mudanças grandes (nova ferramenta, mudança no formato do JSON), abra uma issue antes para combinar a abordagem.
- Siga o [código de conduta](CODE_OF_CONDUCT.md).

## Preparar o ambiente

Você precisa de Python 3.9 ou mais novo e de um navegador.

```bash
git clone https://github.com/carlos-dataengineer/inlustre.git
cd inlustre
pip install playwright
python -m playwright install chromium
```

## Fazer a alteração

1. Crie uma branch: `git checkout -b feat/nome-curto`.
2. Edite **`src/inlustre.html`**. Não edite `app/index.html` nem `skills/inlustre/assets/*`: eles são gerados.
3. Gere os arquivos: `python scripts/build.py`.
4. Abra `app/index.html` no navegador e teste a mudança.
5. Rode os testes:
   ```bash
   python tests/validate_repo.py
   python tests/test_smoke.py
   ```
6. Se a mudança altera a aparência, regenere as imagens: `python scripts/screenshots.py`.
7. Registre a mudança em `CHANGELOG.md`, na seção "Não lançado".

## Padrões do projeto

- **Um arquivo só.** A ferramenta continua funcionando como um único HTML, sem servidor e sem bibliotecas carregadas de fora.
- **Texto em português do Brasil**, direto e sem jargão técnico na interface.
- **Cores por variável CSS.** Toda cor nova precisa de valor no tema claro e no escuro.
- **Compatibilidade do JSON.** Campo novo precisa de valor padrão, para que quadros antigos continuem abrindo.
- **Instaladores sem surpresa.** Eles só escrevem nas pastas documentadas no README. Os `.ps1` ficam em ASCII, sem BOM, para funcionar com `irm | iex` no Windows PowerShell 5.1.

## Mensagens de commit

Use o padrão [Conventional Commits](https://www.conventionalcommits.org/pt-br/v1.0.0/):

```text
feat: adiciona ferramenta de nota adesiva
fix: corrige zoom com pinça no Safari
docs: explica o formato de imagem no JSON
```

## Abrir o pull request

- Descreva o que mudou, por quê e como testou.
- Inclua uma captura de tela quando a mudança for visual.
- A CI precisa passar. Ela confere os arquivos gerados, valida a skill e os instaladores, testa a instalação e roda o teste de fumaça.
