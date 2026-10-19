# Plano de validação

A planilha registra uma prova de conceito futura para PostgreSQL e Parquet. O
roteiro abaixo detalha essa entrega como **plano operacional**, com
responsáveis atribuídos pela Squad G2. Medições que dependem de fonte oficial
continuam explicitamente bloqueadas até a disponibilidade dos arquivos.

## Entregas e critérios de conclusão

| Ordem | Entrega | Evidência para concluir | Dependência |
|---|---|---|---|
| 1 | Inventário verificável de F1–F5 | URL de cada recurso, data de coleta, período coberto, tamanho e esquema real | Acesso às fontes — Ana Joyce / Angélica Campos |
| 2 | Perfilamento e viabilidade dos indicadores | Contagens, chaves, nulos, duplicatas e campos disponíveis para Q1–Q12 | Inventário — Nathan Abreu |
| 3 | Modelo revisado | Dicionário de campos e relacionamentos demonstrados com amostras | Perfilamento — Gabriel Lima da Silva |
| 4 | Recorte completo do pipeline | Uma carga da coleta até um indicador, com relatório de qualidade | Modelo e regras de cálculo — Gustavo Alves |
| 5 | Comparação de armazenamento e consultas | Medições reproduzíveis em CSV, Parquet e PostgreSQL | Recorte validado — Gustavo Alves |
| 6 | Revisão do ADR-001 | Resultados, limitações e decisão da equipe registrados | Prova de conceito — Davi Araújo |

As dependências e os responsáveis estão definidos na tabela. A validação
oficial do Inep permanece bloqueada pelo HTTP 502 registrado no manifesto de
falha; Angélica Campos e Davi Araújo são os responsáveis por repetir o
download quando a fonte voltar.

## Prova de conceito de armazenamento

Usar o mesmo recorte de dados e as mesmas regras de limpeza para comparar formatos. Registrar quantidade de linhas, colunas, períodos e tamanho dos arquivos. Para PostgreSQL, informar também índices e espaço ocupado pelas tabelas.

Selecionar consultas representativas do [catálogo de indicadores](indicadores.md), começando pela contagem de turmas por componente e semestre. Consultas de ocupação só devem entrar se vagas e matrículas estiverem disponíveis e vinculadas.

Registrar ambiente, versões das ferramentas, consulta ou script executado, número de repetições e condição de cache. Separar tempo de leitura, transformação, carga e consulta quando aplicável. Comparar primeiro os resultados retornados; uma consulta mais rápida com totais diferentes não valida a arquitetura.

| Medição | CSV | Parquet | PostgreSQL |
|---|---|---|---|
| Recorte e quantidade de registros | A medir | Mesmo recorte | Mesmo recorte |
| Tamanho armazenado | A medir | A medir | A medir, incluindo índices |
| Tempo da consulta representativa | A medir | A medir com leitor informado | A medir com SQL e índices informados |
| Resultado conferido | Pendente | Pendente | Pendente |

## Verificação operacional

- Reexecutar a mesma carga e conferir que os totais não mudam por duplicação.
- Simular arquivo vazio ou coluna obrigatória ausente e conferir a interrupção da etapa.
- Simular falha antes da publicação e verificar que o consumidor continua vendo uma versão íntegra.
- Conferir manualmente uma amostra dos indicadores e registrar a versão dos dados usada.

## Quando revisitar a escolha

O ADR prevê revisão se consultas analíticas ultrapassarem aproximadamente **5 segundos**, se o volume ou o custo de manutenção crescerem, se as fontes mudarem significativamente ou se surgir necessidade de tempo real.

Esse valor é uma **meta da planilha**, não uma medição já alcançada. A aceitação do ADR depende da avaliação da equipe sobre as evidências; não ocorre automaticamente após a execução da prova de conceito.

## Aceitação da ampliação Inep

1. Baixar F4/F5 e registrar manifesto e dicionário real da edição.
2. Preencher e revisar o mapa de colunas. Rodar normalização sem erro.
3. Cadastrar um pequeno recorte de cursos locais e equivalentes com evidência.
4. Aplicar SQL no PostgreSQL e conferir contagens/chaves; reaplicar e verificar idempotência.
5. Conferir manualmente uma referência ponderada e a exclusão da instituição-alvo.
6. Verificar que grupo vazio e curso sem mapa aparecem como indisponíveis.
7. Integrar Q9–Q12 ao dashboard existente, com filtros e cobertura visíveis.

O pacote inclui testes automatizados com fixtures sintéticas temporárias.
Eles não comprovam cobertura das bases oficiais, desempenho nem integração do dashboard.
