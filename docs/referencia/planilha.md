# Origem e rastreabilidade

Esta documentação usa como referência o arquivo **`referencias/projetoengenhariadedadosbd2-grupo-2.xlsx`**, mantido na pasta de referências do repositório. A aba *Identificação* registra a versão **1.1**, a disciplina **Sistemas de Banco de Dados 2 / Turma 3 / 2026.2** e os sete integrantes.

## Como o conteúdo foi incorporado

As respostas da equipe são a base do conteúdo. Cabeçalhos, instruções de preenchimento e exemplos fictícios de empréstimos de bicicletas pertencem ao modelo da atividade e não descrevem o projeto Trajetórias Acadêmicas UnB.

Os IDs F1–F5, D1–D7, S1–S3 e P1–P10 são convenções desta documentação. A numeração da planilha começa em 2 nas respostas porque a primeira linha é um exemplo. P9/P10 são coletas novas que ocorrem antes de P4; os IDs originais foram mantidos.

| Aba | Conteúdo da equipe | Local na documentação |
|---|---|---|
| Identificação | Problema, público, equipe e contexto acadêmico | [Visão geral](../projeto/visao-geral.md) |
| 1 Fontes | Cinco fontes e suas características | [Fontes de dados](../dados/fontes.md) |
| 2 Formatos | Sete conjuntos e proposta de Parquet | [Formatos](../dados/formatos.md) |
| 3 Modelos | Treze entidades e perguntas Q9–Q12 | [Modelo de dados](../dados/modelo-de-dados.md) |
| 4 Cargas e Engines | Três armazenamentos, latências e garantias | [Cargas e engines](../dados/cargas-e-engines.md) |
| 5 Pipeline | Dez etapas, ferramentas e sinais de falha | [Etapas](../pipeline/etapas.md) |
| Riscos | Sete riscos da extensão Inep e mitigação | [Riscos](../pipeline/riscos.md) |
| ADR | Decisão proposta, alternativas, consequências e revisão | [ADR-001](../decisoes/adr-001-postgresql-parquet.md) |

## Lacunas observadas na versão original recebida

- **Consultas:** a tabela da aba *3 Modelos* contém apenas o exemplo fictício. As perguntas sobre oferta foram recuperadas do ADR; as perguntas de trajetórias foram desenvolvidas a partir da identificação do projeto.
- **Riscos:** o resumo da aba *Instruções* faz referência a “Riscos”, mas **não existe uma aba com esse nome no arquivo analisado**. A página de riscos reúne os itens do ADR e do pipeline, com propostas adicionais identificadas.
- **Progresso:** o resumo mostra “5 de 7” e mínimos do modelo da atividade. Isso não comprova implantação nem conclusão do projeto; as três fontes reais foram preservadas sem inventar uma quarta para atender ao contador.
- **Medições:** volumes e tamanhos permanecem “A confirmar”. As latências são metas e os ganhos com Parquet são expectativas.
- **Implementação:** a planilha não apresenta código do pipeline, benchmark ou evidência de um dashboard implantado.

## Complementos desta revisão

[Arquitetura](../projeto/arquitetura.md), [indicadores](../projeto/indicadores.md), [qualidade](../pipeline/qualidade.md) e [plano de validação](../projeto/plano-de-validacao.md) detalham o planejamento com **propostas a validar**. Eles não devem ser interpretados como decisões já aceitas pela equipe.

Ao revisar o projeto, registrar no ADR o que foi aprovado e atualizar as [pendências](../pendencias.md). Resultados medidos devem informar fonte, recorte, método e data da execução.

## Alterações da versão 1.1

A planilha de referência foi atualizada em 05/10/2026: cinco fontes, sete conjuntos,
treze entidades, dez etapas, Q9–Q12 e riscos da integração. A aba Riscos foi
incluída para registrar esses riscos e atender à referência existente no contador.
Cabeçalhos e exemplos fictícios do modelo da atividade foram preservados.
O registro original de tecnologia permanece proposto e foi complementado com
o escopo Inep; não se atribui decisão de aprovação a integrantes da equipe.
O pipeline Python, SQL e testes desta revisão são novos; não estavam no ZIP original.
