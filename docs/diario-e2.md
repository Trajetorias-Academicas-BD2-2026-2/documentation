# Diário da E2

## Semana 08 — Sistemas e abstrações de armazenamento

### O que foi medido

O lote público versionado foi escolhido como entrada reproduzível. A camada
analítica passou a usar Parquet particionado e Delta Lake.

### O que surpreendeu

Debezium e Kafka acrescentariam uma infraestrutura maior que a necessária para
uma fonte semestral e um volume moderado.

### O que foi decidido

A opção nula continua válida para a fonte pública, mas a E2 terá um caminho de
mudanças separado. A comparação está no
[ADR-003](decisoes/adr-003-ingestao-e2.md).

## Semana 09 — Ingestão

### O que foi medido

O lote processou 1.786 registros, com partições por ano e período e
compressão Zstandard. A reexecução preservou os totais.

### O que surpreendeu

Reprocessar a janela é mais simples e seguro para este volume do que editar
arquivos individuais, principalmente quando há dados atrasados.

### O que foi decidido

O período do evento determina a partição. Uma carga posterior reabre e
substitui a janela afetada.

## Semana 10 — Consultas

### O que foi medido

Uma alteração `30 → 35` no OLTP foi capturada pela outbox e publicada no Delta.
A releitura do consumidor não duplicou a linha lógica.

### O que surpreendeu

O checkpoint e a reconstrução por chave permitem demonstrar at-least-once sem
expor duplicatas ao consumidor.

### O que foi decidido

A entrega usa outbox transacional como CDC equivalente, com possibilidade de
migração futura para Debezium se os requisitos mudarem.
