# Diário de bordo

Registro semanal da Squad: o que foi medido, o que surpreendeu, o que foi decidido. O diário completo está em [`docs/diario/`](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/tree/main/docs/diario), no repositório do código. Abaixo, o resumo.

| Semana | Período | Destaque | Registro |
|---|---|---|---|
| 7 · **E1** | 22/09 a 28/09 | Coleta real do SIGAA: 1.786 reservas, nenhuma série de ocupação pública. A pergunta passa de lotação para vagas reservadas (ADR-0003); lote versionado em vez de scraper (ADR-0004) | [semana-07](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/blob/main/docs/diario/semana-07.md) |
| 8 | 29/09 a 05/10 | Separação entre lote para Parquet/Delta e caminho de mudanças; Debezium/Kafka julgado desproporcional | [semana-08](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/blob/main/docs/diario/semana-08.md) |
| 9 | 06/10 a 12/10 | Partição por `ano/periodo`, zstd, at-least-once com deduplicação; dado atrasado volta à partição do evento | [semana-09](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/blob/main/docs/diario/semana-09.md) |
| 10 · **E2** | 13/10 a 19/10 | Outbox, checkpoint e consumidor. A revisão de 17/11 levou o CDC às tabelas reais e mediu formatos | [semana-10](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/blob/main/docs/diario/semana-10.md) |
| 11 | 20/10 a 26/10 | Granularidade do fato: uma linha por turma e curso | [semana-11](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/blob/main/docs/diario/semana-11.md) |
| 12 | 27/10 a 02/11 | Marts com freshness; retry no script do pipeline | [semana-12](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/blob/main/docs/diario/semana-12.md) |
| 13 · **E3** | 03/11 a 09/11 | Observatório publicado. A revisão de 17/11 acrescentou SCD, backfill real, retry com o banco derrubado e o EXPLAIN de 5.721 para 188 buffers | [semana-13](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/blob/main/docs/diario/semana-13.md) |
| 14 | 10/11 a 16/11 | Camada vetorial na main; roteiro da E3 | [semana-14](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/blob/main/docs/diario/semana-14.md) |
| 15 | 17/11 a 23/11 | Revisão de E1–E3; painel no Pages; E4: semântica, Pauta, RLS, LGPD (achou nomes de docente no Delta) | [semana-15](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/blob/main/docs/diario/semana-15.md) |
| 16 · **E4** | 24/11 | Entrega e defesa (registro após a defesa) | [semana-16](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/blob/main/docs/diario/semana-16.md) |

A [retrospectiva do ciclo de vida](retrospectiva.md) fecha o diário.
