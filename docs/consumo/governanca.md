# Governança

## Métricas oficiais

| Métrica | Definição | Origem |
|---|---|---|
| `vagas_reservadas` | soma de `reserva_vaga.vagas_reservadas`; não é ocupação nem oferta total | SIGAA, "Vgs Reservadas" |
| `obrigatorias_com_reserva` | obrigatórias distintas com ao menos uma reserva no curso e semestre | `curriculo_componente.natureza` |
| `turmas_com_reserva` | turmas distintas com reserva | `turma.id` |
| `atraso_horas` | quanto a última carga da origem está à frente do mart | `metricas_freshness` |

As definições ficam versionadas nos modelos dbt. O painel e o ETL reverso leem as mesmas tabelas, o que evita métricas divergentes.

## Linhagem

```text
SIGAA -> lote CSV com SHA-256 -> OLTP PostgreSQL (fonte, lote, coletado_em, ingerido_em)
      -> snapshot + staging dbt -> fct_reservas -> marts
      -> painel / operations.alertas_reserva / camada vetorial
```

## ETL reverso

`operations.alertas_reserva` é uma fila operacional. A cada execução, `analytics/etl_reverso.py` copia para ela as reservas obrigatórias de 50 vagas ou mais: hoje são 113. A coordenação usa a fila para revisar reservas grandes antes de renegociar o semestre seguinte. O ETL nunca escreve de volta nas tabelas de origem.

## Controle de acesso

O papel `dashboard_reader` (V007) recebe só `SELECT` no schema `analytics` e na fila `operations.alertas_reserva`. Ele não acessa as tabelas do OLTP nem as colunas de docente. Evidência em [`controle-acesso.txt`](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/blob/main/docs/evidencias/controle-acesso.txt).

## LGPD

- **Dados pessoais:** o lote não coleta estudantes nem identificadores de alunos. Nomes de docentes aparecem na origem, mas não entram em nenhum mart nem no painel.
- **Finalidade:** apoiar o planejamento acadêmico. A base legal para uso institucional deve ser confirmada pela UnB antes de uso real.
- **Risco residual:** semestre, turma e docente combinados podem reidentificar alguém. Por isso o painel mostra só agregados por curso, disciplina e semestre.

Detalhes em [`docs/observatorio-e-governanca.md`](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/blob/main/docs/observatorio-e-governanca.md).
