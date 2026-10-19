# Registro de decisões (ADR)

Um **ADR** (*Architecture Decision Record*) registra uma decisão importante com seu
contexto, alternativas consideradas, evidências e consequências — para que, daqui a
seis meses, alguém entenda **por que** as coisas são como são.

| ADR | Título | Status | Data |
|---|---|---|---|
| [ADR-001](adr-001-postgresql-parquet.md) | Adotar PostgreSQL como banco principal e Parquet como formato da camada analítica | Proposto | 02/09/2026 |
| [ADR-003](adr-003-ingestao-e2.md) | Mecanismo de ingestão da E2 | Aceito | 19/10/2026 |

## Status possíveis

- **Proposto** — em discussão.
- **Aceito** — decisão em vigor.
- **Substituído por ADR-NNN** — trocado por uma decisão mais nova.

## Como criar um novo ADR

1. Copie o arquivo `adr-001-postgresql-parquet.md` para `adr-00N-titulo-curto.md`.
2. Atualize título, data, status e participantes.
3. Preencha todos os campos, principalmente *Consequências negativas* — um ADR sem essa parte está incompleto.
4. Adicione a página em `nav` no `mkdocs.yml` e na tabela acima.

[ADR-002 — Integração com o Inep](adr-002-integracao-inep.md): fontes F4/F5 e comparação entre cursos.

[ADR-003 — Mecanismo de ingestão da E2](adr-003-ingestao-e2.md): lote
idempotente, Parquet/Delta e captura de mudanças por outbox transacional.
