# ADR-001 — Adotar PostgreSQL como banco principal e Parquet como formato da camada analítica

| Campo | Valor |
|---|---|
| **Status** | Proposto |
| **Data** | 02/09/2026 |
| **Quem decidiu** | Ana Joyce, Gustavo Alves, Gabriel Lima da Silva, Nathan Abreu, Guilherme Evangelista, Angélica e Davi Araújo |

## Contexto

O projeto apoia coordenadores de cursos de graduação da UnB na decisão sobre quais
disciplinas ofertar e quantas turmas abrir em cada semestre. Para isso, é preciso integrar
dados de alunos, turmas e componentes curriculares disponibilizados pela UnB e executar
consultas com relacionamentos, filtros, agrupamentos e comparações históricas.

A decisão de armazenamento é necessária para escolher uma tecnologia capaz de **preservar
esses relacionamentos** e, ao mesmo tempo, permitir análises sobre demanda, oferta,
ocupação e distribuição das disciplinas por período e turno.

## Requisitos e restrições

- Volume esperado **moderado**: datasets públicos da UnB e suas atualizações periódicas.
- **Sem processamento em tempo real**: a oferta de disciplinas é decidida por semestre.
- Consultas com resultado em **poucos segundos** (filtros e agregações por disciplina, semestre e turno).
- **Integridade** dos relacionamentos entre alunos, turmas e componentes curriculares.
- Equipe com **familiaridade em SQL**; custo e complexidade compatíveis com um projeto acadêmico.

## Padrões de acesso previstos

1. Quantas turmas de cada disciplina foram abertas por semestre.
2. Quais disciplinas têm maior demanda ou ocupação.
3. Comparação entre oferta e demanda ao longo dos períodos.
4. Disciplinas que podem funcionar como gargalos na estrutura curricular.
5. Comparação da oferta de disciplinas obrigatórias entre os turnos diurno e noturno.

Todas exigem principalmente **filtros, junções e agregações** sobre alunos, turmas,
componentes curriculares e períodos.

## Decisão

Adotar **PostgreSQL** como banco de dados principal, mantendo os dados brutos e
analíticos em **Parquet** quando isso beneficiar as consultas e o processamento analítico.

!!! note "Alinhamento pendente sobre os brutos"
    A formulação acima preserva o texto da planilha. As etapas de coleta também preveem guardar os arquivos originais. A [arquitetura proposta](../projeto/arquitetura.md#preservacao-dos-dados-brutos) sugere preservar CSV/JSON e gerar Parquet como derivado; essa interpretação depende de validação da equipe.

## Alternativas consideradas

=== "MySQL"

    **Prós:** SGBD relacional consolidado, bom desempenho em cargas estruturadas, suporte a chaves, relacionamentos e SQL. Seria suficiente para o volume inicial.

    **Contras:** não oferece vantagem concreta sobre o PostgreSQL para as necessidades do projeto; a equipe pretende usar recursos SQL bem suportados pelo PostgreSQL.

    **Por que não foi escolhida:** o critério de desempate foi a **adequação ao projeto e a familiaridade da equipe** com o PostgreSQL, sem necessidade de introduzir outra tecnologia relacional sem benefício relevante.

=== "MongoDB"

    **Prós:** flexibilidade de esquema; útil quando os dados têm estruturas variadas ou mudam com frequência; armazena documentos sem modelo relacional tradicional.

    **Contras:** o projeto tem relacionamentos importantes entre alunos, turmas, componentes e períodos. As consultas dependem de cruzamentos e agregações, o que torna o modelo documental menos natural e pode aumentar a complexidade das consultas e da manutenção.

    **Por que não foi escolhida:** o critério foi a **necessidade de representar e consultar relacionamentos estruturados** entre várias entidades. O modelo relacional atende diretamente; o MongoDB ofereceria flexibilidade desnecessária para este problema.

## Evidência que sustenta a decisão

- Análise das **três fontes reais** do Portal de Dados Abertos da UnB (alunos, turmas e componentes curriculares), todas com estrutura tabular e que precisam ser relacionadas para produzir os indicadores.
- Padrões de acesso identificados no [modelo de dados](../dados/modelo-de-dados.md).
- **Prova de conceito planejada** com PostgreSQL e Parquet sobre dados reais, comparando tempo de consulta e volume de armazenamento.

!!! info "Status da evidência"
    A prova de conceito ainda **não foi executada**. Registre aqui os resultados
    (tempos e tamanhos) quando estiverem disponíveis. O [plano de validação](../projeto/plano-de-validacao.md) detalha os recortes, medições e critérios propostos. A disponibilidade efetiva dos vínculos entre as fontes ainda precisa ser comprovada.

## Consequências

### Positivas

- Relacionamentos do domínio representados de forma clara.
- Chaves e restrições preservam a integridade dos dados.
- Consultas SQL complexas de forma direta.
- Parquet na camada analítica reduz a quantidade de dados lidos quando só algumas colunas são usadas.
- Solução relativamente simples, com tecnologias adequadas ao conhecimento da equipe.

### Negativas

- A equipe precisa manter uma **etapa de tratamento e integração** antes do uso nas análises.
- Usar PostgreSQL e Parquet juntos aumenta um pouco a complexidade do pipeline em relação a um único formato.
- O PostgreSQL pode exigir ajustes de índices e consultas se o volume crescer muito.

## Riscos assumidos

- O volume crescer além da estimativa e tornar algumas consultas mais lentas.
- Alterações no formato ou nas colunas dos datasets da UnB quebrarem o pipeline de ingestão.
- Dependência da disponibilidade e da periodicidade de atualização de fontes externas.

Veja também a página de [riscos](../pipeline/riscos.md).

## Como e quando revisitar

A decisão deve ser reaberta se:

- o volume de dados crescer significativamente;
- consultas analíticas ultrapassarem a latência aceitável de ~5 segundos;
- o custo ou a complexidade de manutenção aumentar;
- surgirem requisitos de processamento em tempo real;
- a UnB alterar significativamente o formato ou a estrutura dos datasets.

## Complemento de escopo — 05/10/2026

A versão 1.1 incorpora F4/F5 do Inep ao PostgreSQL em schema próprio. A decisão
de tecnologia permanece proposta até validação com dados reais. CSV tratado e
carga SQL estão implementados; Parquet continua como derivado opcional.
A decisão de integrar agregados anuais por curso está em [ADR-002](adr-002-integracao-inep.md).
