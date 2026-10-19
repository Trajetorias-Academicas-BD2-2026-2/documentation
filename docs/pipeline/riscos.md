# Riscos

| ID | Risco | Origem | Impacto | Sinal de detecção | Mitigação | Responsável |
|---|---|---|---|---|---|---|
| R1 | O volume de dados cresce além da estimativa inicial e as consultas ficam lentas | ADR-001 | Consultas acima de ~5 s | Latência das consultas analíticas | Ajuste de índices e consultas no PostgreSQL; revisitar a decisão de armazenamento | Gustavo Alves |
| R2 | A UnB altera o formato ou as colunas dos datasets e quebra a ingestão | ADR-001 / P1–P3 | Pipeline de ingestão falha | Alteração inesperada nas colunas; esquema fora do esperado | Validação de esquema na coleta; manter os arquivos brutos originais | Ana Joyce |
| R3 | Fonte indisponível ou com atualização fora da periodicidade esperada | ADR-001 / P1–P3 | Dados desatualizados ou ausentes | Falha no download; arquivo vazio ou ausente | Reprocessar a partir dos dados brutos já armazenados | Angélica Campos |
| R4 | Complexidade extra de manter PostgreSQL e Parquet juntos | ADR-001 | Pipeline mais difícil de manter | — | Documentar cada transformação; manter etapa de tratamento bem definida | Gustavo Alves |
| R5 | Registros sem correspondência entre alunos, turmas e componentes | P5 | Indicadores incorretos | Verificação de chaves estrangeiras e registros sem correspondência | Relatório de validação a cada carga | Gabriel Lima da Silva |

## Riscos adicionais identificados nesta revisão

Os itens abaixo são **propostas para avaliação da equipe**, derivados das lacunas entre o inventário e os indicadores.

| ID | Risco | Impacto | Verificação / mitigação proposta | Responsável |
|---|---|---|---|---|
| R6 | Ausência de vínculo aluno–turma ou de solicitações de matrícula | Ocupação ou demanda não calculáveis | Confirmar a origem desses dados e restringir indicadores ao que as fontes comprovam | Nathan Abreu |
| R7 | Publicação de carga parcial ou de versões incompatíveis | Totais inconsistentes no dashboard | Validar a execução completa e promover uma versão identificada | Gustavo Alves |
| R8 | Comparação de coortes com tempos de acompanhamento diferentes | Interpretação incorreta de conclusão e cancelamento | Exibir data de corte, janela de acompanhamento e população de cada grupo | Davi Araújo |

Os controles propostos estão em [Qualidade e reprocessamento](qualidade.md); as dependências analíticas, em [Perguntas e indicadores](../projeto/indicadores.md).

## Riscos da ampliação Inep

| Risco | Efeito | Tratamento |
|---|---|---|
| Servidor de download indisponível | F4/F5 não chegam | Encerrar com erro e registrar falha; download manual oficial como alternativa |
| Mudança de schema ou unidade da taxa | Indicador incorreto | Mapa de colunas revisado por edição; validação bloqueante |
| Correspondência errada de curso | Comparação mistura cursos/campi | Mapa por ano com evidência e revisão manual |
| Coortes ou períodos diferentes | Referência não comparável | Chave curso/coorte/ano e filtros iguais |
| Duplicação de coortes em edições | Contagens infladas | Rejeitar conflitos e manter uma revisão por chave |
| Revisão remove registros | Registros antigos permanecem | Conferir diferenças e planejar substituição transacional do recorte |
| F4 e F5 tratados como fontes independentes | Validação circular | Registrar que F5 deriva do Censo |
