# Fontes de dados

O projeto passa a ter **cinco fontes selecionadas**: F1–F3 da UnB e F4–F5 publicados pelo Inep. F4–F5 ampliam a comparação entre cursos e instituições; sua carga real ainda depende do download e da validação dos arquivos.

!!! note "Inventário declarado na planilha"
    As características abaixo reproduzem o planejamento da equipe. URLs específicas dos recursos, períodos cobertos, esquemas reais e tamanhos ainda não estão registrados. Vazão, pureza e previsibilidade são classificações da planilha, sem medições anexadas.

## Resumo

| ID | Fonte | Tipo | Formato | Frequência | Vazão | Pureza | Previsibilidade | Dado pessoal? |
|---|---|---|---|---|---|---|---|---|
| F1 | Dados de alunos (SIGAA) | Sistema | CSV | Eventual / atualização periódica | Média | Média | Alta | Fora do recorte publicado |
| F2 | Turmas | Sistema | CSV | Semestral / eventual | Média | Alta | Alta | Não no recorte publicado |
| F3 | Componente curricular | Sistema | CSV / JSON | Eventual / atualização periódica | Média | Alta | Alta | Não, se usados só dados curriculares |
| F4 | Censo da Educação Superior | Terceiro | ZIP / CSV após inspeção | Anual / revisões | A medir | A validar | A validar | Agregados de curso/IES |
| F5 | Indicadores de Trajetória | Terceiro | ZIP / tabela a conferir | Anual / revisões | A medir | A validar | A validar | Agregados de curso/coorte |

!!! tip "Como ler as colunas"
    - **Vazão**: quantidade de dado que chega por unidade de tempo.
    - **Pureza**: o quanto o dado chega limpo (sem duplicidade, nulos ou erros).
    - **Previsibilidade**: o quanto o formato/esquema se mantém estável entre entregas.

## F1 — Dados de alunos (SIGAA)

| Item | Descrição |
|---|---|
| **Quem gera** | UnB / SIGAA |
| **Conteúdo** | Histórico acadêmico e informações de ingresso, situação, turno e período |
| **Formato** | CSV |
| **Volume estimado** | Não medido no material publicado |
| **Retenção** | Retido somente durante a execução do projeto |
| **Tratamento no projeto** | Não utilizado no recorte publicado; o observatório trabalha com dados agregados de oferta |
| **O que quebra se falhar** | Impossibilita analisar o tempo médio de formação, o perfil sociodemográfico, o impacto de cotas/ingresso e as taxas de evasão e conclusão |

## F2 — Turmas

| Item | Descrição |
|---|---|
| **Quem gera** | UnB / SIGAA |
| **Conteúdo** | Relação de turmas da instituição, permitindo analisar a oferta de disciplinas por período |
| **Formato** | CSV |
| **Volume estimado** | Não medido no material publicado |
| **Frequência** | Semestral / eventual |
| **Retenção** | Retido somente durante a execução do projeto |
| **Tratamento no projeto** | Usada apenas para informações agregadas de oferta, sem dados de alunos |
| **O que quebra se falhar** | Não será possível analisar quais disciplinas são ofertadas, quantas turmas são abertas e como a oferta varia ao longo dos períodos |

## F3 — Componente curricular

| Item | Descrição |
|---|---|
| **Quem gera** | UnB / SIGAA |
| **Conteúdo** | Relação dos componentes curriculares dos cursos da UnB, com as informações necessárias para identificar e relacionar as disciplinas |
| **Formato** | CSV / JSON |
| **Volume estimado** | Não medido no material publicado |
| **Frequência** | Eventual / atualização periódica |
| **Retenção** | Enquanto necessário ao projeto |
| **Base legal (LGPD)** | Não se aplica |
| **O que quebra se falhar** | Não será possível relacionar corretamente as turmas às disciplinas nem analisar a estrutura curricular |

## Evidências a coletar

| Fonte | Recurso e período | Verificação prioritária |
|---|---|---|
| F1 · Alunos | URL e cobertura temporal a registrar | Confirmar granularidade do vínculo, datas de ingresso/conclusão e existência de relação aluno–turma |
| F2 · Turmas | URL e cobertura temporal a registrar | Confirmar identificador único, vagas, turno, situação e chave do componente |
| F3 · Componentes | URL e cobertura temporal a registrar | Confirmar código, pré-requisitos e vínculo com a matriz de cada curso |

A presença de uma entidade no modelo não comprova que seus campos estejam disponíveis nas fontes. Confira as [dependências dos indicadores](../projeto/indicadores.md#dependencias-que-precisam-ser-confirmadas) antes de definir as consultas finais.

## F4 e F5 — Ampliação nacional

| ID | Fonte | Formato de chegada | Frequência | Volume e qualidade | Dado pessoal no recorte utilizado |
|---|---|---|---|---|---|
| F4 | Censo da Educação Superior, curso/ano | ZIP com arquivos e dicionário; selecionar CSV | Anual e revisões | A medir após download | Somente agregados de curso/instituição |
| F5 | Indicadores de Trajetória, curso/coorte/ano | ZIP; selecionar tabela conforme a edição | Anual e revisões | A medir após download | Somente indicadores agregados |

URLs, edição inicial, chaves e disponibilidade estão na [integração Inep](integracao-inep.md).
Manter originais e manifestos enquanto necessários à reprodução do projeto;
a política definitiva de retenção permanece com a equipe. Não importar
identificadores individuais de estudantes do Inep para essa extensão.
