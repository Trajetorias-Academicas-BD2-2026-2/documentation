# Qualidade e testes

Três camadas de verificação, todas falham com código diferente de zero.

## 1. Origem: `tests/sanity_checks.sql`

```bash
docker compose run --rm tests
```

São 23 verificações sobre o OLTP. A lista por grupo está em [E1](../entregas/e1.md#testes-de-dados-da-origem):

- esquema;
- volume;
- currículo;
- distribuição;
- dado faltante;
- histórico.

## 2. Camada analítica: testes dbt

Rodam dentro do `dbt build`. Resultado atual: `PASS=57 WARN=1 ERROR=0` (58 nós).

| Tipo | Testes |
|---|---|
| Esquema | `not_null` nas chaves e métricas; `accepted_values` em natureza (`OBRIGATORIA`, `OPTATIVA`) e tipo (`DISCIPLINA`, `ATIVIDADE`) |
| Unicidade | chaves das dimensões; granularidade do fato (`turma_id`, `curso_id`); granularidade dos marts |
| Integridade referencial | `relationships` do fato para `dim_curso`, `dim_disciplina` (versão) e `dim_semestre`; dos marts e da dimensão curricular para `dim_curso` |
| SCD | exatamente uma versão corrente por disciplina |
| Volume | fato ≥ 1.500 linhas **e** nenhum semestre abaixo de 50% da mediana (pega carga parcial de um semestre) |
| Distribuição | vagas entre 1 e 200; nenhum curso some de um semestre; **salto de série** (curso que mais que dobra ou cai pela metade), com `severity: warn` |
| Freshness | `dbt source freshness` (200/400 dias) e `test_sla_freshness_mart` (24 h) |

O aviso do salto de série é esperado. Ele acusa 4 saltos a partir de 2023.2, quando as reservas grandes ficam comuns. É aviso, e não erro, porque o semestre precisa ser olhado, mas a carga não deve parar.

## 3. Consumo: `tests/analytics_checks.sql`

```bash
docker compose --profile test run --rm analytics-tests
```

| Verificação | Resultado atual |
|---|---|
| fato com linhas | 1.776 |
| unicidade turma–curso | 0 duplicadas |
| freshness registrada | ok |
| SLA: mart até 24 h atrás da origem | 0 h |
| SCD: uma versão corrente por disciplina | 0 problemas |
| integridade fato → `dim_semestre` | 0 órfãs |
| ETL reverso populado | 113 |

## Reprocessar sem duplicar

| Onde | Mecanismo | Evidência |
|---|---|---|
| Carga do OLTP | compara cada linha com o banco; lote divergente é recusado inteiro | resumo `idêntica (reprocessamento)` |
| Lote Parquet/Delta | overwrite determinístico | 1.786 linhas em duas execuções |
| CDC | MERGE com `last_event_id`; checkpoint só depois da escrita | 3.034 linhas antes e depois da reexecução |
| Fato dbt | `delete+insert` por semestre | backfill de 2024.1 com contagens iguais |
