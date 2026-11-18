# Entrega 3 — Observatório analítico

## Visão geral

A Entrega 3 transforma os dados de reservas de vagas em informação analítica
reprodutível, com métricas por curso e semestre, dashboard, testes de
qualidade, governança e busca semântica.

| Componente | Implementação |
|---|---|
| Transformação | dbt |
| Banco | PostgreSQL |
| Fato | `fct_reservas` (uma linha por turma e curso, incremental por semestre) |
| Dimensões | `dim_curso`, `dim_semestre`, `dim_disciplina` (SCD 2), `dim_curriculo_componente` (SCD 2) |
| Marts | `mart_observatorio`, `mart_disciplina_semestre`, `mart_cobertura_curriculo` |
| Dashboard | Observatório de reservas |
| Vetores | pgvector |

## Pergunta de gestão

> Como evoluíram, entre 2022.1 e 2026.1, as vagas reservadas publicadas para
> cada curso da FCTE nas disciplinas obrigatórias do currículo de referência
> selecionado para 2026.1?

O indicador representa **vagas reservadas publicadas**, não ocupação real nem
oferta total de vagas.

## Dados analisados

| Indicador | Resultado |
|---|---:|
| Turmas | 733 |
| Reservas | 1.776 |
| Semestres | 9 |
| Período | 2022.1 a 2026.1 |
| Disciplinas com vetor | 72 |

## Arquitetura

```text
Dados públicos → PostgreSQL → dbt → mart_observatorio
                                      ├── Dashboard
                                      ├── ETL reverso
                                      └── Busca vetorial
```

## Métricas do observatório

| Métrica | Significado |
|---|---|
| `vagas_reservadas` | Soma das vagas reservadas |
| `obrigatorias_com_reserva` | Disciplinas obrigatórias com reserva |
| `turmas_com_reserva` | Turmas que reservaram vagas |

| Curso | Semestre | Vagas reservadas | Obrigatórias com reserva | Turmas |
|---|---|---:|---:|---:|
| `FGA_SOFT` | `2026.1` | 3.816 | 30 | 79 |

Em 2026.1, as reservas publicadas para `FGA_SOFT` somaram 3.816 vagas em 30
disciplinas obrigatórias e 79 turmas. Isso não significa 3.816 alunos.

## Qualidade e governança

| Controle | Resultado |
|---|---|
| Testes dbt | 45 testes; `dbt build` com PASS=57 WARN=1 ERROR=0 |
| Dimensões de variação lenta | `dim_disciplina` (snapshot) e natureza curricular por versão |
| Freshness | `metricas_freshness`, SLA de 24 h testado |
| Retry | Banco derrubado de propósito: falha, nova tentativa, sucesso |
| Backfill | Só a janela 2024.1 reprocessada (174 linhas), contagens iguais |
| ETL reverso | 113 registros |
| Acesso | `dashboard_reader` com privilégio mínimo |
| Performance | `EXPLAIN (ANALYZE, BUFFERS)` do q0: 5.721 → 188 buffers |

## Camada vetorial

A camada vetorial usa pgvector para encontrar disciplinas semanticamente
parecidas.

| Validação | Resultado |
|---|---:|
| Textos vetorizados | 638 |
| Disciplinas com vetor | 100% de 72 |
| Dimensão | 384 |
| Vetores fora da norma | 0 |
| Testes | Código 0 |

Resultados próximos incluíram Sistemas de Banco de Dados 1, Sistemas de
Bancos de Dados e Estruturas de Dados 2.

## Arquitetura em camadas

O fluxo segue o padrão Bronze, Prata e Ouro:

| Camada | Papel | Conteúdo |
|---|---|---|
| **Bronze** | Preservar a origem | Lote público versionado e checksums |
| **Prata** | Validar e estruturar | PostgreSQL relacional e histórico operacional |
| **Ouro** | Apoiar decisões | dbt, fato, mart, métricas e dashboard |

Na Bronze, os arquivos originais são preservados para permitir
reprocessamento. Na Prata, turmas, reservas, disciplinas, currículos e
semestres são relacionados e validados no PostgreSQL. Na Ouro, o dbt aplica
as regras de negócio e entrega o `mart_observatorio` para consumo.

```text
Bronze → Prata → Ouro
arquivos → PostgreSQL → dbt/mart/dashboard
```

## Linhagem e qualidade

| Origem | Transformação | Produto |
|---|---|---|
| Arquivos do SIGAA | Checksum e preservação | Lote Bronze |
| Lote versionado | Carga e integridade | PostgreSQL Prata |
| Tabelas operacionais | Modelos dbt | `fct_reservas` |
| Fato analítica | Agregações | `mart_observatorio` |
| Nomes de disciplinas | Embeddings e HNSW | Busca vetorial |

Foram validados checksums, chaves, unicidade, volume, distribuição,
freshness, dimensão dos vetores e norma unitária. Os 45 testes dbt passaram, com um aviso esperado de salto de série; a camada vetorial cobriu 100% das 72 disciplinas do fato.

## Operação e governança

O projeto inclui retry para falhas transitórias, backfill por semestre, ETL
reverso para 113 alertas, catálogo, linhagem e acesso mínimo pelo papel
`dashboard_reader`. O `EXPLAIN (ANALYZE, BUFFERS)` da consulta da pergunta
mostrou um erro de estimativa num CTE; a reescrita reduziu a leitura de 5.721
para 188 buffers com o mesmo resultado, e um índice duplicado da chave
primária foi removido.

As decisões de arquitetura estão documentadas nos ADRs de modelagem, coleta,
ingestão e camada analítica.

## Limitações e conclusão

O projeto mede reservas publicadas, não ocupação real. O currículo de
referência é o de 2026.1, o dashboard é uma demonstração local e a camada
vetorial complementa, mas não substitui, o modelo relacional.

A Entrega 3 disponibiliza um observatório analítico reproduzível, com
transformações testadas, histórico de dimensões, orquestração com retry e
backfill, métricas documentadas, governança e busca semântica. Detalhes por
entrega em [E1](entregas/e1.md), [E2](entregas/e2.md) e [E3](entregas/e3.md).
