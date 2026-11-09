# ADR-003 — Camada analítica dbt e observatório de reservas da E3

**Data:** 08/11/2026. **Status:** aceito. **Decisores:** Squad G2 — Ana
Joyce, Gustavo Alves, Gabriel Lima da Silva, Nathan Abreu, Guilherme
Evangelista, Angélica Campos e Davi Araújo.

## Contexto

A E3 transforma os dados carregados na E2 em uma camada analítica
reproduzível, validada e consumível por uma aplicação. O projeto responde à
pergunta sobre a evolução, entre 2022.1 e 2026.1, das vagas reservadas
publicadas para cada curso da FCTE nas disciplinas obrigatórias do currículo
de referência selecionado para 2026.1.

O banco transacional é a fonte operacional. O dashboard não deve recalcular
regras diretamente sobre o OLTP, pois isso espalharia lógica de negócio e
poderia produzir métricas diferentes das usadas pelo ETL reverso.

## Alternativas consideradas

| Alternativa | Descrição | Resultado |
|---|---|---|
| A | Consultar diretamente as tabelas operacionais no dashboard | Rejeitada: acopla a apresentação ao OLTP |
| B | Criar tabelas analíticas manualmente por scripts SQL | Rejeitada: dificulta testes e reprocessamento |
| C | Usar dbt com staging, dimensões, fato e marts | Escolhida: centraliza regras e torna as transformações reproduzíveis |

## Decisão

Adotar a alternativa C:

1. O dbt será a camada entre o OLTP e os consumidores analíticos.
2. A fato terá uma linha por turma, curso, disciplina e semestre.
3. O mart filtrará as disciplinas obrigatórias do currículo de referência de
   2026.1 e definirá as métricas de vagas reservadas, disciplinas com reserva
   e turmas com reserva.
4. O dashboard lerá apenas o mart e oferecerá filtros por curso e semestre.
5. O ETL reverso usará as mesmas regras e publicará alertas agregados em
   `operations.alertas_reserva`.
6. Testes de unicidade, volume, distribuição e freshness protegerão a
   execução, juntamente com retry e backfill.
7. O dashboard usará o papel `dashboard_reader`, com acesso mínimo de leitura.

## Evidências

- 18 testes dbt executados com `PASS=18 WARN=0 ERROR=0 SKIP=0`.
- 1.776 linhas na fato do recorte carregado.
- 113 registros agregados no ETL reverso.
- Dashboard respondendo em `http://localhost:8080`.
- Evidências de retry, backfill, controle de acesso e `EXPLAIN` no repositório
  principal do projeto.

## Consequências

### Positivas

- As regras ficam centralizadas e testáveis.
- Dashboard e ETL reverso compartilham as mesmas métricas.
- A linhagem OLTP → staging → fato → mart → consumidores fica explícita.
- Um semestre pode ser reprocessado sem alterar a fonte operacional.

### Negativas

- A equipe mantém uma camada adicional de modelos e a ferramenta dbt.
- O mart precisa ser atualizado após novas cargas.
- O recorte mede vagas reservadas publicadas, não ocupação real nem oferta
  total de vagas.

## Gatilhos de revisão

- Nova fonte de ocupação ou demanda de matrícula.
- Mudança da granularidade das reservas ou do currículo de referência.
- Consultas acima do SLA de 2 segundos ou atualização acima de 24 horas.
- Necessidade de atualização em tempo real em vez de processamento em lote.
