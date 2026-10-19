# Fontes de dados

O projeto passa a ter **cinco fontes selecionadas**: F1–F3 da UnB e F4–F5 publicados pelo Inep. F4–F5 ampliam a comparação entre cursos e instituições; sua carga real ainda depende do download e da validação dos arquivos.

!!! note "Inventário declarado na planilha"
    As características abaixo reproduzem o planejamento da equipe. Ana Joyce
    é responsável por completar o inventário F1–F3; Angélica Campos e Davi
    Araújo são responsáveis pelo inventário F4–F5. Enquanto os ZIPs oficiais
    não estiverem disponíveis, os campos dependentes de medição permanecem
    explicitamente bloqueados, sem serem tratados como resultados.

## Resumo

| ID | Fonte | Tipo | Formato | Frequência | Vazão | Pureza | Previsibilidade | Dado pessoal? |
|---|---|---|---|---|---|---|---|---|
| F1 | Dados de alunos (SIGAA) | Sistema | CSV | Eventual / atualização periódica | Média | Média | Alta | Sim |
| F2 | Turmas | Sistema | CSV | Semestral / eventual | Média | Alta | Alta | Ana Joyce — confirmar |
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
| **Conteúdo** | Histórico acadêmico, forma de ingresso (PAS, Enem, Cotas), status (concluído/cancelado), turno, sexo, raça/cor, data de nascimento e de ingresso |
| **Formato** | CSV |
| **Volume estimado** | Ana Joyce — medir |
| **Retenção** | Ana Joyce — propor e registrar |
| **Base legal (LGPD)** | Ana Joyce — revisar com a equipe |
| **O que quebra se falhar** | Impossibilita analisar o tempo médio de formação, o perfil sociodemográfico, o impacto de cotas/ingresso e as taxas de evasão e conclusão |

!!! warning "Atenção à LGPD"
    Esta fonte contém atributos como **sexo, raça/cor e data de nascimento**. Raça/cor é
    classificada como dado pessoal sensível pela LGPD (art. 5º, II). A base legal e a forma
    de tratamento (por exemplo, confirmar se o dataset público já vem anonimizado)
    ainda precisam ser definidas — veja as [Pendências](../pendencias.md).

## F2 — Turmas

| Item | Descrição |
|---|---|
| **Quem gera** | UnB / SIGAA |
| **Conteúdo** | Relação de turmas da instituição, permitindo analisar a oferta de disciplinas por período |
| **Formato** | CSV |
| **Volume estimado** | Gustavo Alves — medir |
| **Frequência** | Semestral / eventual |
| **Retenção** | Gustavo Alves — propor e registrar |
| **Base legal (LGPD)** | Ana Joyce — revisar com a equipe |
| **O que quebra se falhar** | Não será possível analisar quais disciplinas são ofertadas, quantas turmas são abertas e como a oferta varia ao longo dos períodos |

## F3 — Componente curricular

| Item | Descrição |
|---|---|
| **Quem gera** | UnB / SIGAA |
| **Conteúdo** | Relação dos componentes curriculares dos cursos da UnB, com as informações necessárias para identificar e relacionar as disciplinas |
| **Formato** | CSV / JSON |
| **Volume estimado** | Gabriel Lima da Silva — medir |
| **Frequência** | Eventual / atualização periódica |
| **Retenção** | Enquanto necessário ao projeto |
| **Base legal (LGPD)** | Não se aplica |
| **O que quebra se falhar** | Não será possível relacionar corretamente as turmas às disciplinas nem analisar a estrutura curricular |

!!! note "Dado comportamental também conta"
    Dado emitido por um sistema, mas que descreve uma pessoa (cliques, tempo de uso,
    trajeto), é considerado dado de usuário para efeito de LGPD.

## Evidências a coletar

| Fonte | Recurso e período | Verificação prioritária |
|---|---|---|
| F1 · Alunos | Ana Joyce — URL e cobertura temporal | Confirmar granularidade do vínculo, datas de ingresso/conclusão e existência de relação aluno–turma |
| F2 · Turmas | Gustavo Alves — URL e cobertura temporal | Confirmar identificador único, vagas, turno, situação e chave do componente |
| F3 · Componentes | Gabriel Lima da Silva — URL e cobertura temporal | Confirmar código, pré-requisitos e vínculo com a matriz de cada curso |

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
