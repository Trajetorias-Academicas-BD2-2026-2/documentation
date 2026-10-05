# Riscos

!!! warning "Em elaboração"
    O resumo da planilha menciona **Riscos**, mas essa aba não existe no arquivo analisado. Esta página
    consolida os riscos já citados no [ADR-001](../decisoes/adr-001-postgresql-parquet.md)
    e nas etapas do [pipeline](etapas.md). Complete as colunas marcadas como *A definir*.

| ID | Risco | Origem | Impacto | Sinal de detecção | Mitigação | Responsável |
|---|---|---|---|---|---|---|
| R1 | O volume de dados cresce além da estimativa inicial e as consultas ficam lentas | ADR-001 | Consultas acima de ~5 s | Latência das consultas analíticas | Ajuste de índices e consultas no PostgreSQL; revisitar a decisão de armazenamento | A definir |
| R2 | A UnB altera o formato ou as colunas dos datasets e quebra a ingestão | ADR-001 / P1–P3 | Pipeline de ingestão falha | Alteração inesperada nas colunas; esquema fora do esperado | Validação de esquema na coleta; manter os arquivos brutos originais | A definir |
| R3 | Fonte indisponível ou com atualização fora da periodicidade esperada | ADR-001 / P1–P3 | Dados desatualizados ou ausentes | Falha no download; arquivo vazio ou ausente | Reprocessar a partir dos dados brutos já armazenados | A definir |
| R4 | Complexidade extra de manter PostgreSQL e Parquet juntos | ADR-001 | Pipeline mais difícil de manter | — | Documentar cada transformação; manter etapa de tratamento bem definida | A definir |
| R5 | Registros sem correspondência entre alunos, turmas e componentes | P5 | Indicadores incorretos | Verificação de chaves estrangeiras e registros sem correspondência | Relatório de validação a cada carga | A definir |

## Riscos adicionais identificados nesta revisão

Os itens abaixo são **propostas para avaliação da equipe**, derivados das lacunas entre o inventário e os indicadores.

| ID | Risco | Impacto | Verificação / mitigação proposta | Responsável |
|---|---|---|---|---|
| R6 | Ausência de vínculo aluno–turma ou de solicitações de matrícula | Ocupação ou demanda não calculáveis | Confirmar a origem desses dados e restringir indicadores ao que as fontes comprovam | A definir |
| R7 | Publicação de carga parcial ou de versões incompatíveis | Totais inconsistentes no dashboard | Validar a execução completa e promover uma versão identificada | A definir |
| R8 | Comparação de coortes com tempos de acompanhamento diferentes | Interpretação incorreta de conclusão e cancelamento | Exibir data de corte, janela de acompanhamento e população de cada grupo | A definir |

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
