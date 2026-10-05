# Perguntas e indicadores

O projeto combina **planejamento da oferta** e **compreensão das trajetórias acadêmicas**. As cinco primeiras perguntas vêm dos padrões de acesso do ADR; as demais desenvolvem os objetivos da aba *Identificação*.

!!! note "Definições para validar com a equipe"
    A planilha não fixa fórmulas, janelas de observação ou regras de contagem. Os critérios desta página são **propostas de especificação**, dependentes da inspeção dos datasets. Nenhum indicador foi calculado nesta documentação.

## Catálogo de perguntas

| ID | Pergunta | Público | Recorte previsto | Dados necessários |
|---|---|---|---|---|
| Q1 | Quantas turmas de cada disciplina foram abertas por semestre? | Coordenação | Componente, período e turno | F2 + F3; identificador e situação da turma |
| Q2 | Quais disciplinas têm maior demanda ou ocupação? | Coordenação | Componente, período e turno | Vagas, matrículas válidas e, para demanda, solicitações ou fila de espera |
| Q3 | Como oferta e demanda variam ao longo dos períodos? | Coordenação | Série por componente e turno | Histórico de Q1 e Q2 com critérios comparáveis |
| Q4 | Quais disciplinas podem ser gargalos curriculares? | Coordenação | Curso, componente e período | Pré-requisitos, matriz curricular e histórico de matrícula/aprovação |
| Q5 | Como a oferta de obrigatórias difere entre diurno e noturno? | Coordenação | Curso, matriz, período e turno | F2 + F3 e classificação de obrigatoriedade por curso |
| Q6 | Qual é o tempo de formação por curso? | Coordenação e ingressantes | Curso e coorte de ingresso | F1; ingresso, conclusão e identificação do vínculo acadêmico |
| Q7 | Como variam conclusão e cancelamento entre coortes? | Coordenação e ingressantes | Curso, coorte e data de corte | F1; situação acadêmica e acompanhamento do vínculo |
| Q8 | Como as trajetórias se distribuem por forma de ingresso e cotas? | Coordenação e ingressantes | Curso, coorte e modalidade | F1; categorias de ingresso e cotas validadas na fonte |

**Uso previsto:** consultas agregadas em dashboard ou relatório, durante o planejamento semestral e sob demanda. A frequência diária de acesso ainda não foi estimada. Os IDs Q1–Q8 são identificadores desta documentação.

## Regras de cálculo propostas

| Indicador | Definição inicial | Condições e limites |
|---|---|---|
| Turmas ofertadas | Contagem de turmas distintas por componente, período e turno | Definir o tratamento de turmas canceladas e a unicidade do identificador |
| Vagas ofertadas | Soma das vagas das turmas incluídas no recorte | Somar antes de juntar com matrículas para evitar multiplicar vagas |
| Taxa de ocupação | `matrículas válidas / vagas ofertadas × 100` | Definir situações válidas; vagas zero ou ausentes resultam em “não disponível”; investigar valores acima de 100% |
| Demanda observada | Contagem de solicitações válidas no recorte | Exige fonte ou campo de solicitações; matrículas efetivadas não medem a demanda reprimida |
| Tempo de formação | Média e mediana do intervalo entre ingresso e conclusão dos vínculos concluídos | Definir unidade; excluir datas inválidas e informar tamanho do grupo; não representa o tempo dos alunos ainda ativos |
| Proporção de conclusão | `vínculos concluídos da coorte / vínculos da coorte × 100`, na data de corte | Coortes recentes tiveram menos tempo para concluir; explicitar janela de acompanhamento |
| Proporção de cancelamento | `vínculos cancelados da coorte / vínculos da coorte × 100`, na data de corte | Não equiparar automaticamente cancelamento a evasão; mapear as situações da fonte |

## Dependências que precisam ser confirmadas

As fontes locais F1–F3 sustentam as análises semestrais. F4–F5 acrescentam agregados nacionais, mas não fornecem o vínculo local aluno–turma. Embora o modelo inclua Matrícula, a planilha não comprova que exista um vínculo aluno–turma disponível nelas. Sem essa relação, ocupação e demanda não podem ser deduzidas apenas do cadastro de alunos e da lista de turmas.

Também precisam ser verificados: datas de conclusão, solicitações de matrícula, pré-requisitos e obrigatoriedade por curso. Um componente pode ser obrigatório em um curso e optativo em outro; a comparação entre turnos depende da matriz curricular correspondente.

## Interpretação e apresentação

- Mostrar período de referência, data de atualização, filtros e quantidade de registros considerados junto de cada resultado.
- Separar forma de ingresso de modalidade de concorrência/cotas conforme o dicionário da fonte; não assumir categorias mutuamente exclusivas.
- Comparações entre grupos descrevem associações; não demonstram que a forma de ingresso causou determinado resultado.
- Publicar informações agregadas para ingressantes, com critérios de divulgação de grupos pequenos a definir pela equipe.
- Tratar “gargalo” como hipótese a investigar. Alta ocupação isolada não comprova retenção nem falta de vagas.

A intenção de apoiar decisões preditivas aparece na planilha, mas não há modelo preditivo, método de avaliação ou resultado documentado. A primeira validação deve verificar se as análises descritivas são viáveis.

**Próximo passo:** executar o [plano de validação](plano-de-validacao.md) e incorporar as regras confirmadas ao [modelo de dados](../dados/modelo-de-dados.md).

## Novas perguntas da versão 1.1

| ID | Pergunta | Dados e granularidade | Produto |
|---|---|---|---|
| Q9 | Como evoluem ingressantes, matrículas e concluintes dos cursos selecionados da UnB e de cursos equivalentes? | F4, curso/ano; mapa local validado | Série anual com período e cobertura |
| Q10 | Após o mesmo acompanhamento, como conclusão e desistência da UnB se comparam às de instituições equivalentes? | F5, curso/coorte/ano; grupos comparáveis | Taxas e diferenças em pontos percentuais |
| Q11 | Como permanência, conclusão e desistência evoluem dentro da mesma coorte? | F5, curso/coorte/ano | Evolução da coorte; sem somar anos |
| Q12 | Quais cursos/anos não têm correspondência ou referência comparável? | Mapa local, F4 e F5 | Relatório de cobertura e ausências |

Taxas da referência são ponderadas pelos ingressantes da coorte. Excluir a
instituição-alvo e manter área, grau, modalidade, categoria, coorte e ano iguais.
Uma variação entre observações com intervalo maior que um ano não deve ser
rotulada como variação anual. Não calcular conclusão usando ingressantes e
concluintes do mesmo ano. As [regras completas](../dados/integracao-inep.md) e
as consultas de `sql/002_indicadores_inep.sql` definem o recorte.

Apresentar duas visões adicionais no dashboard da equipe: **Comparação entre
instituições** (Q9–Q10) e **Trajetória por coorte** (Q11), com cobertura Q12 visível.
Filtros: curso, instituição, área, grau, modalidade, categoria e período/coorte.
Exibir atualização, denominador, número de instituições da referência e origem.
Essas telas são especificadas aqui; não há código do dashboard no ZIP original.
