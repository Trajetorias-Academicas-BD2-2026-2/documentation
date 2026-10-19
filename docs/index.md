---
hide:
  - toc
---

# Trajetórias Acadêmicas UnB

<div class="project-hero" markdown>

<span class="project-eyebrow">BD2 · FCTE/UnB · 2026.2</span>

## Dados para compreender trajetórias e planejar a oferta acadêmica

Integramos o planejamento de dados de **alunos, turmas e componentes curriculares** para apoiar a coordenação dos cursos e ajudar futuros ingressantes a conhecer a realidade da UnB.

[Conheça o projeto](projeto/visao-geral.md){ .md-button .md-button--primary }
[Explore a arquitetura](projeto/arquitetura.md){ .md-button }

</div>

<div class="grid cards project-stats" markdown>

- **5 fontes selecionadas**

    Alunos, turmas, componentes, Censo e trajetórias do Inep.

- **Modelo ampliado**

    Modelo local e seis tabelas adicionais no schema Inep.

- **10 etapas**

    Da coleta ao consumo dos indicadores.

- **3 registros de decisão**

    PostgreSQL e Parquet, a validar com dados reais.

</div>

!!! info "Estágio do projeto: planejamento, validação e E2"
    Esta documentação consolida a planilha da equipe, versão 1.1. A
    arquitetura geral e a extensão Inep continuam em validação; o recorte da
    E2 tem execução demonstrada para lote, Parquet/Delta e captura de
    mudanças. Consulte a [origem do conteúdo](referencia/planilha.md), o
    [plano de validação](projeto/plano-de-validacao.md) e a
    [evidência da E2](pipeline/ingestao-e2.md).

## Duas perspectivas, uma base de dados

<div class="grid cards" markdown>

- :material-chart-box-outline: **Para a coordenação acadêmica**

    ---

    Comparar oferta de turmas, distribuição por turno e possíveis gargalos para apoiar o planejamento semestral.

    [Perguntas e indicadores](projeto/indicadores.md)

- :material-school-outline: **Para futuros ingressantes**

    ---

    Entender tempo de formação, conclusão e formas de ingresso por meio de informações agregadas dos cursos.

    [Objetivos e escopo](projeto/visao-geral.md)

</div>

## Explore a documentação

<div class="grid cards" markdown>

- :material-database-outline: **Dados e modelagem**

    ---

    Conheça a origem dos dados, os formatos e os relacionamentos que sustentam as análises.

    [Fontes](dados/fontes.md) · [Formatos](dados/formatos.md) · [Modelo](dados/modelo-de-dados.md)

- :material-transit-connection-variant: **Pipeline e qualidade**

    ---

    Acompanhe a coleta, a integração e os critérios propostos para publicar indicadores consistentes.

    [Fluxo](pipeline/visao-geral.md) · [Etapas](pipeline/etapas.md) · [E2 — ingestão](pipeline/ingestao-e2.md) · [Qualidade](pipeline/qualidade.md)

- :material-source-branch: **Decisões de engenharia**

    ---

    Entenda os critérios de escolha de PostgreSQL e Parquet, as alternativas e os riscos aceitos.

    [ADR-001](decisoes/adr-001-postgresql-parquet.md) · [ADR-003 — ingestão E2](decisoes/adr-003-ingestao-e2.md) · [Cargas e engines](dados/cargas-e-engines.md)

- :material-clipboard-check-outline: **Próximas entregas**

    ---

    Veja quais evidências faltam para validar a arquitetura e orientar a implementação.

    [Plano de validação](projeto/plano-de-validacao.md) · [Pendências](pendencias.md)

</div>

## Do dado ao apoio à decisão

```mermaid
flowchart TB
    A[Fontes UnB e Inep] --> B[Coleta e preservação]
    B --> C[Validação e integração]
    C --> D[(PostgreSQL e Parquet)]
    D --> E[Indicadores]
    E --> F[Coordenação e ingressantes]
```

Fluxo planejado; a divisão entre os armazenamentos está descrita na [arquitetura proposta](projeto/arquitetura.md).

## Equipe

Ana Joyce · Gustavo Alves · Gabriel Lima da Silva · Nathan Abreu · Guilherme Evangelista · Angélica · Davi Araújo

*Sistemas de Banco de Dados 2 · Turma 3 · 2026.2 · FCTE/UnB.*

## Comparação entre instituições

A versão 1.1 acrescenta fontes nacionais, séries anuais e comparação de coortes.
[Integração e fontes Inep](dados/integracao-inep.md) ·
[Como executar a extensão](pipeline/execucao-inep.md).
As rotinas e consultas estão incluídas; a carga oficial ainda precisa ser validada.
