# Qualidade e reprocessamento

A aba *5 Pipeline* já prevê validação de arquivos, contagem de registros e verificação de chaves. Esta página transforma esses sinais em uma **proposta de critérios de aceite**, a implementar e validar pela equipe.

!!! success "Critérios demonstrados na E2"
    O lote da E2 processou 1.786 linhas, foi executado novamente sem
    duplicação e publicou Parquet particionado por `ano/periodo` com
    Zstandard. O consumidor CDC atualizou o estado de `E2-DEMO-001` de
    30 para 35 vagas e manteve uma linha lógica por chave.

## Verificações por etapa

| Etapa | Verificação proposta | Evidência registrada | Ação em caso de falha |
|---|---|---|---|
| P1–P3 · Coleta | Arquivo presente, legível e não vazio; colunas obrigatórias disponíveis | Fonte, data, tamanho, checksum e esquema observado | Preservar o diagnóstico e impedir a promoção da coleta inválida |
| P4 · Limpeza | Tipos, datas, identificadores, nulos e duplicatas | Contagens de entrada, aceitos, rejeitados e duplicados | Separar registros inválidos com motivo; revisar regras antes de descartá-los |
| P5 · Integração | Unicidade das chaves e correspondência entre entidades | Quantidade de vínculos válidos e registros órfãos | Bloquear dados que violem relações obrigatórias; investigar cobertura das fontes |
| P6 · Carga analítica | Mesma versão de origem, granularidade e período dos conjuntos | Identificador da execução e contagens por recorte | Não publicar uma combinação de versões incompatíveis |
| P7 · Indicadores | Totais conciliados, denominadores válidos e filtros consistentes | Conferência de uma amostra e totais por período | Marcar indicador indisponível ou bloquear sua publicação |
| P8 · Consumo | Consulta executável e data de atualização visível | Erro, tempo de resposta e versão publicada | Informar indisponibilidade ou usar a última versão validada |

Os limites aceitáveis de nulos, duplicatas e registros sem correspondência serão definidos após o perfilamento. Não há percentuais de tolerância medidos na planilha.

## Contrato mínimo de cada fonte

Antes de automatizar a ingestão, registrar:

1. URL do recurso, período coberto, data de obtenção e versão do arquivo.
2. Codificação, separador, nomes de colunas e tipos observados.
3. Chave candidata e verificações que demonstram sua unicidade.
4. Campos obrigatórios por indicador e tratamento para ausência de cada um.
5. Categorias de situação acadêmica, turno e ingresso encontradas na fonte.

Os nomes de atributos do [modelo conceitual](../dados/modelo-de-dados.md) ainda não constituem um contrato validado com os datasets.

## Reexecutar sem duplicar

Proposta para a implementação:

1. Identificar a entrada por fonte, período e checksum, mantendo o arquivo original.
2. Registrar um identificador de execução e a versão das regras de transformação.
3. Processar a nova carga em área temporária, separada dos dados publicados.
4. Validar chaves, contagens e indicadores antes de substituir o recorte correspondente.
5. Promover a versão aprovada de forma controlada e guardar o resultado da execução.

O aceite deve incluir a repetição da mesma entrada: ela precisa produzir os mesmos totais sem criar duplicatas. Uma falha intermediária não deve alterar a versão disponível ao usuário.

### Resultado da E2

| Teste | Resultado |
|---|---|
| Reexecução do mesmo lote | 1.786 linhas nas duas execuções |
| Particionamento | `ano/periodo` |
| Compressão | Zstandard |
| Alteração no OLTP | `30 → 35` vagas |
| Releitura do CDC | uma linha por chave |
| Dado atrasado | reprocessa a janela do período do evento |

!!! note "Reprocessar não substitui publicação consistente"
    A aba *4 Cargas e Engines* admite abrir mão de atomicidade na base analítica porque a carga pode ser refeita. A recuperação resolve a execução futura, mas não evita a leitura de dados parciais durante a falha. A proposta é validar uma versão completa antes de publicá-la; o mecanismo ainda precisa ser definido.

## Registro de execução proposto

| Grupo | Campos a registrar |
|---|---|
| Identificação | Execução, etapa, fonte, período, versão das regras |
| Entrada | Local do arquivo, checksum, horário de obtenção, quantidade de registros |
| Resultado | Aceitos, rejeitados, duplicatas, registros sem correspondência |
| Operação | Início, fim, duração, status e motivo da falha |
| Publicação | Versão disponibilizada e data da última carga validada |

O responsável, o local de armazenamento desses registros e o canal de alerta permanecem **a definir**. Veja os [riscos](riscos.md) e o [plano de validação](../projeto/plano-de-validacao.md).

## Controles adicionais de F4–F5

Conferir o dicionário e a codificação da edição antes da normalização. Rejeitar
colunas ausentes, coorte posterior à observação, denominador não positivo e
percentuais fora de 0–100. Taxas devem somar 100 com tolerância de 0,2 p.p.
Duplicatas iguais são contadas e removidas; conflitos de chave interrompem a carga.
O destino tratado só aparece depois de todas as validações.

Conferir mapas locais e cobertura da referência antes da publicação. As cargas
SQL fazem atualização por chave em transação e não removem linhas ausentes de
uma edição revisada. Revisões com exclusões exigem substituição do recorte planejada.
Originais e manifestos são preservados. [Execução](execucao-inep.md).
