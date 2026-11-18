# Governança e acesso

## Métricas oficiais

Definidas uma vez na [camada semântica](../dados/camada-semantica.md) e lidas por todos os consumidores. O painel mostra a definição de cada número no rodapé.

## Controle de acesso: privilégio mínimo, recorte de linha e de coluna

Papéis criados na [V012](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/blob/main/db/migrations/V012__acesso_e4.sql):

| Papel | Vê | Não vê |
|---|---|---|
| `painel` | toda a camada de consumo (`analytics`) | nada do OLTP (`public`) |
| `etl_reverso` | métricas e marts; escreve só a fila `operations.envio_pauta` | não altera a camada analítica |
| `coord_soft`, `coord_elet` (`coordenador`) | **só as linhas do próprio curso** (RLS) | outros cursos, OLTP |
| `auditor_lgpd` | `docente.id`, `turma_docente` | **a coluna `docente.nome`** (dado pessoal) |

- **RLS e o dbt:** o dbt recria as tabelas a cada execução, o que apagaria as políticas de RLS. A função `operations.aplicar_acesso_analytics()` as reaplica no `on-run-end`, e o teste confere as políticas depois do build.
- **Painel e ETL:** deixaram de usar o superusuário `g2`.

Verificação: `tests/acesso_checks.sql`, com 16 verificações, todas passando ([evidência](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/blob/main/docs/evidencias/e4-acesso.txt)).

## LGPD, catálogo e linhagem

- [Análise de LGPD do que foi construído](../governanca/lgpd.md)
- [Catálogo e linhagem, da fonte ao consumo](../governanca/catalogo-e-linhagem.md)

## Freshness e SLA

A view `analytics.metricas_freshness` mede o atraso do mart frente à última carga da origem. O SLA é de 24 h, testado em `test_sla_freshness_mart` e mostrado no painel.
