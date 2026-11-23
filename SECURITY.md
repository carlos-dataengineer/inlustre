# Política de segurança

## Versões com suporte

| Versão | Suporte |
|---|---|
| 1.x | Sim |

## Como relatar uma vulnerabilidade

**Não abra uma issue pública.** Use o relato privado do GitHub:

1. Acesse [Security → Report a vulnerability](https://github.com/carlos-dataengineer/inlustre/security/advisories/new).
2. Descreva o problema, como reproduzir e o impacto que você enxerga.

A primeira resposta chega em até 7 dias. Se o problema for confirmado, a correção sai em uma nova versão, com crédito para você se quiser.

## O que está no escopo

- Instaladores e desinstaladores: escrita fora das pastas documentadas ou execução de código inesperado.
- A ferramenta (`src/inlustre.html`): injeção de script por um quadro JSON ou por texto colado.
- A skill (`skills/inlustre/SKILL.md`): instruções que levem o agente a agir além do pedido da pessoa.

## Boas práticas para quem instala

- Leia o script antes de rodar. Ele é curto e comentado.
- Prefira instalar uma versão marcada: `INLUSTRE_REF=v1.0.0`.
- Abra quadros `.json` apenas de fontes em que você confia.
