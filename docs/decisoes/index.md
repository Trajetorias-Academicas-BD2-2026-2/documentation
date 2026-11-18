# Registro de decisões (ADR)

Um ADR registra uma decisão com contexto, alternativas, medição e consequências, para que alguém entenda depois **por que** as coisas são como são. Os ADRs abaixo são cópias dos de [`docs/adr/`](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/tree/main/docs/adr), no repositório do código, que é a fonte.

| ADR | Decisão | Entrega | Status |
|---|---|---|---|
| [ADR-0001](0001-modelagem-fonte-origem.md) | Oferta de turmas insert-only, uma linha por turma e semestre encerrado, em 3FN | E1 | Substituído pelo ADR-0003 |
| [ADR-0002](0002-extracao-via-navegador-real.md) | Extração do SIGAA por navegador real | E1 | Substituído pelo ADR-0004 |
| [ADR-0003](0003-reservas-por-curso-e-curriculo-versionado.md) | Turmas e reservas por curso insert-only, currículo versionado | E1 | Aceito |
| [ADR-0004](0004-coleta-publica-versionada.md) | Carga a partir de um lote versionado e conferido por checksum | E1 | Aceito |
| [ADR-0005](0005-ingestao-e2.md) | Lote idempotente por partição e CDC por outbox transacional | E2 | Aceito |
| [ADR-0006](0006-camada-analitica-observatorio-e3.md) | Esquema estrela em dbt, fato por turma e curso, orquestrado por script com cron | E3 | Aceito |

Os ADR-0001 e 0002 foram substituídos antes da carga real e ficam como registro.

## Como criar um novo ADR

1. Escreva o ADR no repositório do código, em `docs/adr/NNNN-titulo-curto.md`, com contexto, alternativas (incluindo a opção nula), medição, decisão, consequências negativas e gatilho de revisão.
2. Copie o arquivo para `docs/decisoes/` deste site e troque os links relativos ao código por links do GitHub.
3. Acrescente a linha na tabela acima e a página em `nav`, no `mkdocs.yml`.
