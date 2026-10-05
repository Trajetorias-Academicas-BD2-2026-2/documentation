# Etapas do pipeline

As etapas P1–P7, P9 e P10 são planejadas em **lote**; o consumo P8 ocorre **sob demanda**. Os responsáveis ainda estão **a definir**. Ferramentas e verificações abaixo são previstas na planilha, sem evidência de execução anexada.

## P1 — Coleta de dados dos alunos

| Item | Descrição |
|---|---|
| Origem → destino | Dataset de alunos da UnB → armazenamento de dados brutos |
| Transformações | Baixar o arquivo; verificar formato, tamanho, colunas e integridade |
| Modo | ELT, em lote |
| Frequência | Semestral / conforme atualização da fonte |
| Custo de 1 h de atraso | Baixo — os dados não precisam ser atualizados em tempo real |
| Ferramenta | Python + requisição HTTP / download do arquivo |
| Como detectar falha | Registro de erro no processo, arquivo ausente ou alteração inesperada nas colunas |

## P2 — Coleta de turmas

| Item | Descrição |
|---|---|
| Origem → destino | Dataset de turmas da UnB → armazenamento de dados brutos |
| Transformações | Baixar os dados, validar a estrutura e preservar o arquivo original |
| Modo | ELT, em lote |
| Frequência | Semestral / conforme atualização da fonte |
| Custo de 1 h de atraso | Baixo — a análise é histórica |
| Ferramenta | Python |
| Como detectar falha | Falha no download, arquivo vazio ou alteração no esquema esperado |

## P3 — Coleta de componentes curriculares

| Item | Descrição |
|---|---|
| Origem → destino | Dataset de componente curricular da UnB → armazenamento de dados brutos |
| Transformações | Baixar, validar o formato e verificar a presença da chave do componente |
| Modo | ELT, em lote |
| Frequência | Eventual / conforme atualização da fonte |
| Custo de 1 h de atraso | Baixo |
| Ferramenta | Python |
| Como detectar falha | Erro de download, arquivo vazio ou ausência das colunas obrigatórias |

## P4 — Validação e limpeza

| Item | Descrição |
|---|---|
| Origem → destino | Dados brutos (alunos, turmas, componentes) → base de dados tratada |
| Transformações | Padronizar nomes e tipos, tratar valores ausentes, remover duplicidades, validar identificadores |
| Modo | ETL, em lote |
| Frequência | Após cada atualização das fontes |
| Custo de 1 h de atraso | Baixo — o processamento pode ser reexecutado |
| Ferramenta | Python + Pandas |
| Como detectar falha | Relatório de validação com quantidade de registros processados, erros e duplicidades |

## P5 — Integração dos dados

| Item | Descrição |
|---|---|
| Origem → destino | Dados tratados → banco PostgreSQL |
| Transformações | Juntar pelas chaves, relacionar turmas aos componentes e alunos às respectivas informações acadêmicas |
| Modo | ETL, em lote |
| Frequência | Após cada atualização das fontes |
| Custo de 1 h de atraso | Baixo |
| Ferramenta | Python + PostgreSQL |
| Como detectar falha | Verificação das chaves estrangeiras, quantidade de registros relacionados e registros sem correspondência |

## P6 — Carga da base analítica

| Item | Descrição |
|---|---|
| Origem → destino | Dados integrados → base analítica PostgreSQL / arquivos Parquet |
| Transformações | Selecionar atributos relevantes, calcular indicadores e preparar os dados para consulta |
| Modo | ELT, em lote |
| Frequência | Após cada atualização dos dados |
| Custo de 1 h de atraso | Baixo |
| Ferramenta | Python + PostgreSQL + Parquet |
| Como detectar falha | Comparação entre registros de entrada e saída e validação dos indicadores gerados |

## P7 — Geração de indicadores

| Item | Descrição |
|---|---|
| Origem → destino | Base analítica → dashboard / sistema de apoio à decisão |
| Transformações | Agregar por disciplina, semestre e turno; calcular demanda, oferta, ocupação e tendências |
| Modo | ELT, em lote |
| Frequência | Semestral / sob demanda |
| Custo de 1 h de atraso | Baixo |
| Ferramenta | SQL + Python |
| Como detectar falha | Testes de consistência dos indicadores e registro de erro na execução das consultas |

## P8 — Consumo dos dados

| Item | Descrição |
|---|---|
| Origem → destino | Indicadores da base analítica → coordenador de curso |
| Transformações | Filtrar e apresentar informações sobre oferta, demanda, ocupação e distribuição por turno |
| Modo | Não se aplica; sob demanda |
| Frequência | Conforme a consulta do usuário |
| Custo de 1 h de atraso | Médio — afeta a experiência do usuário, mas não interrompe a coleta |
| Ferramenta | Aplicação web / dashboard |
| Como detectar falha | Monitoramento da aplicação e mensagens de erro quando os indicadores não puderem ser carregados |

## P9 — Coleta do Censo da Educação Superior

F4 → originais versionados. Download anual em lote, com edição, URL, tamanho,
SHA-256 e horário. ZIP íntegro é requisito; falha interrompe o processo sem
apagar a carga anterior. Executado antes de P4. Ferramenta: Python, comando
`fetch --source censo`. Responsável: a definir.

## P10 — Coleta dos Indicadores de Trajetória

F5 → originais versionados. Download em lote por edição/coorte; registrar a
janela de acompanhamento e evitar união duplicada de coortes sobrepostas.
Executado antes de P4. Ferramenta: Python, `fetch --source trajetoria`.
Responsável: a definir.

## Extensão de P4–P8

- P4: mapear colunas após revisão do dicionário; validar percentuais, anos e chaves.
- P5: gerar carga no schema `inep` e revisar a correspondência curso local–Inep.
- P6: manter tabelas curso/ano e curso/coorte/ano, sem multiplicar contagens por turma.
- P7: calcular Q9–Q12, com médias ponderadas e grupos comparáveis.
- P8: integrar as visões ao dashboard da equipe e mostrar cobertura e atualização.

Coleta/tratamento de F4–F5 e SQL estão incluídos; ligação a P8 depende do código
da aplicação existente. [Execução e tratamento de falhas](execucao-inep.md).
