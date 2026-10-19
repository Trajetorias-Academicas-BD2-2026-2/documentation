# Visão geral do projeto

## Identificação

| Campo | Informação |
|---|---|
| **Nome do projeto** | Trajetórias Acadêmicas UnB |
| **Disciplina / turma / semestre** | Sistemas de Banco de Dados 2 / Turma 3 / 2026.2 |
| **O que o sistema faz** | Apresenta trajetórias acadêmicas na UnB: tempo de formação, cotas e formas de ingresso e disponibilidade de turmas |
| **Repositório** | <https://github.com/Trajetorias-Academicas-BD2-2026-2/documentation> |
| **Versão da planilha de referência** | 1.1 — ampliação Inep, 05/10/2026 |
| **Data de preenchimento da planilha** | 02/09/2026 |

## Problema que o sistema resolve

O projeto apoia a coordenação acadêmica na **definição estratégica e preditiva da oferta
de disciplinas** na UnB, reduzindo a dependência de decisões empíricas para:

- combater a **superlotação de turmas**;
- mitigar **gargalos curriculares**;
- diminuir o **tempo de retenção** nos cursos.

Ao mesmo tempo, a solução funciona como uma **fonte transparente de dados** para futuros
ingressantes e para a comunidade externa, permitindo conhecer, antes de iniciar a
trajetória universitária:

- a realidade prática de cada curso;
- o comportamento da taxa de conclusão;
- as formas de ingresso;
- os tempos médios de diplomação.

## Quem usa o sistema

| Ator | Como usa |
|---|---|
| **Coordenadores de cursos de graduação** | Consultam indicadores de oferta, demanda, ocupação e distribuição por turno para decidir a oferta semestral |
| **Interessados em ingressar na UnB** | Consultam informações públicas sobre cursos, ingresso e tempo de formação |

## Perguntas que o sistema precisa responder

Estes são os padrões de acesso mais frequentes, definidos no [ADR-001](../decisoes/adr-001-postgresql-parquet.md):

1. Quantas turmas de cada disciplina foram abertas por semestre?
2. Quais disciplinas têm maior demanda ou ocupação?
3. Como a oferta e a demanda se comparam ao longo dos períodos?
4. Quais disciplinas funcionam como gargalos na estrutura curricular?
5. Como se compara a oferta de disciplinas obrigatórias entre os turnos diurno e noturno?

!!! note "Escala de decisão"
    A oferta de disciplinas é decidida **por semestre**. Por isso o sistema não exige
    processamento em tempo real: todo o pipeline trabalha em **lote**.

## Escopo e estágio atual

A planilha apresenta uma proposta de sistema. O primeiro recorte de validação deve conectar fontes reais, modelo e consultas descritivas antes de avaliar previsões de demanda.

| Frente | Objetivo | Dependência para validar |
|---|---|---|
| Oferta acadêmica | Comparar turmas, vagas e turnos ao longo dos semestres | Identificadores e histórico de turmas e componentes |
| Trajetórias | Analisar tempo de formação e situação acadêmica | Datas, vínculo acadêmico e categorias consistentes |
| Ingresso e cotas | Comparar resultados agregados entre grupos | Dicionário das modalidades e recortes comparáveis |
| Apoio preditivo | Antecipar necessidades de oferta | Histórico adequado e método de avaliação — Nathan Abreu; só iniciar após validar o recorte descritivo |

Veja as definições propostas em [Perguntas e indicadores](indicadores.md), a divisão das camadas na [arquitetura](arquitetura.md) e os critérios de conclusão no [plano de validação](plano-de-validacao.md).

## Equipe

| Integrante |
|---|
| Ana Joyce |
| Gustavo Alves |
| Gabriel Lima da Silva |
| Nathan Abreu |
| Guilherme Evangelista |
| Angélica |
| Davi Araújo |

## Ampliação 1.1 — Comparação entre instituições

O projeto incorpora o Censo da Educação Superior e os Indicadores de Trajetória
para contextualizar os cursos da UnB em relação a cursos equivalentes.
A pergunta adicional central é: **como evoluem o tamanho dos cursos e os resultados
das coortes da UnB em comparação com cursos semelhantes de outras instituições?**

O novo recorte não demonstra que a oferta de uma disciplina causa desistência
ou retenção. Ele acrescenta séries anuais e comparações descritivas ao domínio
semestral existente. Consulte a [integração Inep](../dados/integracao-inep.md).
