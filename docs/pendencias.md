# Pendências

Itens marcados como **"A confirmar"** ou **"A definir"** na planilha de acompanhamento,
mais pontos de alinhamento entre as abas. Marque as caixas conforme forem resolvidos.

## Prioridades para a próxima entrega

| Prioridade | Pendência | Critério para concluir |
|---|---|---|
| 1 | Registrar recursos reais de F1–F3 | URLs, versões, períodos e esquemas documentados |
| 2 | Confirmar viabilidade dos indicadores | Vínculo aluno–turma, vagas, datas de conclusão e categorias verificados |
| 3 | Validar um recorte completo | Coleta, integração e indicador com totais conferidos |
| 4 | Medir e revisar a arquitetura | Prova de conceito e avaliação do ADR registradas |

## E2 — itens concluídos

- [x] Ingestão em lote idempotente da fonte pública
- [x] Parquet particionado com compressão Zstandard
- [x] Tabela Delta sobre Parquet
- [x] Captura de mudanças por outbox transacional
- [x] Semântica at-least-once com deduplicação demonstrada
- [x] Política para dado atrasado e reprocessamento de janela
- [x] ADR-003 sobre o mecanismo de ingestão
- [x] Diário das semanas 8 a 10

O [plano de validação](projeto/plano-de-validacao.md) detalha a ordem das entregas. Responsáveis e prazos permanecem a definir.

## Dados

- [ ] Volume estimado por dia/mês das fontes F1, F2 e F3 ([Fontes](dados/fontes.md))
- [ ] Frequência de chegada da fonte F1 (alunos)
- [ ] Retenção dos dados de alunos e de turmas
- [ ] Tamanho estimado em 1 ano de cada conjunto de dados ([Formatos](dados/formatos.md))
- [ ] Volume estimado em 1 ano de cada armazenamento ([Cargas e engines](dados/cargas-e-engines.md))

## Modelo e indicadores

- [ ] Comprovar a fonte de Matrícula e a relação aluno–turma
- [ ] Confirmar disponibilidade de vagas, solicitações, datas de conclusão e pré-requisitos
- [ ] Validar a chave de Oferta de Disciplina considerando o turno
- [ ] Definir curso/matriz e obrigatoriedade dos componentes
- [ ] Definir coortes, data de corte, situações válidas e denominadores de Q1–Q8 ([Indicadores](projeto/indicadores.md))
- [ ] Revisar as classificações OLTP/OLAP e ETL/ELT a partir da implementação

## LGPD

- [ ] Definir a base legal para os dados de alunos (F1) e de turmas (F2)
- [ ] Confirmar se os datasets públicos já vêm anonimizados (sexo, raça/cor e data de nascimento)
- [ ] Confirmar se `matrícula` como chave de Aluno é o identificador real ou um código anonimizado

## Pipeline e responsáveis

- [ ] Definir o responsável de cada etapa P1–P8 ([Etapas](pipeline/etapas.md))
- [ ] Registrar os riscos na planilha (a aba mencionada no resumo está ausente) e revisar [Riscos](pipeline/riscos.md)

## Decisão (ADR-001)

- [ ] Executar a prova de conceito PostgreSQL + Parquet com dados reais
- [ ] Registrar tempos de consulta e volume de armazenamento (CSV × Parquet)
- [ ] Avaliar as evidências com a equipe e registrar a decisão de aceitar ou revisar o ADR

## Pontos a alinhar entre as abas

- [ ] **Camada analítica:** a planilha descreve a base analítica como PostgreSQL orientado a linha (aba 4) e também como Parquet (abas 2, 5 e ADR). Definir quais consultas rodam no PostgreSQL e quais leem Parquet.
- [ ] **Dados brutos:** a aba 4 guarda os brutos em sistema de arquivos; o ADR fala em brutos em Parquet. Definir se os brutos ficam no formato original (CSV/JSON) ou convertidos.
- [ ] **Tabela de consultas** da aba 3 (Modelos): só tem o exemplo; transferir as consultas do ADR para lá.

## Pendências específicas da versão 1.1

- [ ] Obter ZIPs F4/F5: tentativa de 05/10/2026 retornou HTTP 502.
- [ ] Conferir dicionário, membro CSV, codificação, unidade das taxas e colunas.
- [ ] Validar os mapas de colunas e a correspondência de cursos reais da UnB.
- [ ] Definir cursos equivalentes e medir cobertura por ano/coorte.
- [ ] Executar carga e visões no PostgreSQL da equipe, com conferência de totais.
- [ ] Integrar Q9–Q12 ao código do dashboard existente.
- [ ] Medir armazenamento, tempo de consulta e eventual exportação Parquet.

O smoke test Docker com fixtures sintéticas foi concluído; ele valida o
pipeline e o schema, mas não encerra os itens que dependem dos ZIPs oficiais.

Coleta/tratamento, DDL e consultas, documentação, atualização da planilha e
testes sintéticos foram acrescentados. Esses itens não encerram as pendências
de coleta real e integração da aplicação.
