# ADR-003 — Mecanismo de ingestão da E2

| Campo | Valor |
|---|---|
| **Status** | Aceito para a E2 |
| **Data** | 19/10/2026 |
| **Quem decidiu** | Squad G2 |

## Contexto

A E2 exige dois caminhos entre a origem e o armazenamento analítico:
ingestão em lote da fonte pública e captura de mudanças no OLTP. O lote
versionado contém 1.786 registros e representa uma fonte de atualização
semestral. O OLTP precisa demonstrar uma mudança atravessando o fluxo.

## Alternativas

### Opção nula: somente recarga periódica

`INSERT ... SELECT` ou substituição agendada é suficiente para a fonte pública:
o custo de uma atualização atrasada é baixo e o volume é moderado. Ela não
atende, sozinha, à demonstração pedagógica de uma mudança no OLTP.

### Debezium lendo WAL e Kafka

É uma solução adequada para maior escala e menor latência, mas introduz
Kafka, Kafka Connect, JVM e operação adicional. Para esta entrega, o custo
operacional dificulta a reprodução pelos colegas e não é justificado pelo
volume observado.

### Outbox transacional

Uma alteração do OLTP grava um evento na mesma transação. Um consumidor lê a
sequência da outbox, publica o estado por chave e salva um checkpoint. É
reproduzível somente com PostgreSQL e demonstra CDC equivalente, mantendo
aberta a evolução para Debezium.

## Decisão

Adotar:

- lote versionado;
- Parquet particionado por `ano/periodo`;
- compressão Zstandard;
- Delta Lake sobre Parquet;
- outbox transacional para `INSERT`, `UPDATE` e `DELETE`;
- consumidor idempotente com checkpoint.

## Garantias e trade-offs

A semântica é **at-least-once com deduplicação determinística**. Uma falha
antes do checkpoint pode causar releitura, mas não duplica a linha lógica
publicada. O fluxo não afirma exactly-once porque a confirmação do evento e a
publicação no destino não são uma única transação distribuída.

Dados atrasados são atribuídos ao período do evento. A janela antiga é
reprocessada e substituída, preservando o resultado correto sem misturar
tempo de evento com tempo de ingestão.

O custo aceito é manter uma etapa de reconstrução/compactação no consumidor.
Se a latência exigida cair para segundos ou o volume crescer
significativamente, a decisão deve ser revisitada e Debezium pode substituir
a outbox demonstrativa.

## Evidências

- [Implementação da E2 no repositório da aplicação](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/tree/feat/e2-ingestao-cdc-parquet)
- [Roteiro e resultados da demonstração](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/blob/feat/e2-ingestao-cdc-parquet/docs/evidencia-e2.md)
