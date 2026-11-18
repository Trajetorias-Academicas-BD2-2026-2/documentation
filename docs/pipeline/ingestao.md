# Ingestão

Dois caminhos levam o dado da origem ao armazenamento analítico aberto. Eles falham de jeitos diferentes, e por isso existem os dois. Decisão no [ADR-0005](../decisoes/0005-ingestao-e2.md); saída executada em [`e2-roteiro.txt`](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/blob/main/docs/evidencias/e2-roteiro.txt).

```bash
docker compose run --rm --build e2-cdc bash ingestion/run_e2.sh   # roteiro completo
```

## Caminho em lote

[`ingestion/batch_to_delta.py`](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/blob/main/ingestion/batch_to_delta.py) lê o lote público versionado e grava em `analytical/batch/ofertas/`:

- **Saídas:** Parquet particionado por `ano/periodo` e uma tabela Delta.
- **Idempotência:** overwrite determinístico, nunca append. Duas execuções seguidas dão as mesmas 1.786 linhas.
- **Janela:** `--semestre 2023.1` sobrescreve só aquela partição, por `write_deltalake(mode="overwrite", predicate=...)`, sem tocar as outras.

### Dado atrasado

O semestre do **evento** define a partição, não a data de ingestão. `ingestion/demo_atraso.py` acrescenta uma reserva de 2023.1 "coletada" em novembro e reprocessa a janela 2023.1:

- **Partição:** 2023.1 passa de 192 para 193 linhas.
- **Outras partições:** as 8 restantes mantêm os mesmos arquivos.
- **Auditoria:** o Delta guarda a versão anterior.

Por fim, a janela é restaurada a partir da fonte original.

## Caminho de mudanças (CDC)

A migração V010 instala triggers `AFTER` que gravam cada mudança numa **outbox transacional** (`e2_cdc_outbox`), na mesma transação da escrita:

| Tabela | Eventos | Por quê |
|---|---|---|
| `reserva_vaga` | INSERT | insert-only: cada carga vira eventos |
| `disciplina` | INSERT, UPDATE, DELETE | correções do catálogo chegam por upsert |
| `curriculo_componente` | INSERT, UPDATE, DELETE | mudanças de natureza ou grupo |

UPDATE que não muda valor nenhum não gera evento. Isso cobre o loader reprocessando o mesmo lote.

[`ingestion/cdc_consumer.py`](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/blob/main/ingestion/cdc_consumer.py) segue quatro passos:

1. lê os eventos com `id > checkpoint`;
2. fica com o último evento de cada `(tabela, chave)`;
3. faz **MERGE** no Delta `analytical/cdc/oltp`, substituindo a linha só se o evento for mais novo;
4. **depois** avança o checkpoint.

## Semântica de entrega

**At-least-once na leitura, com escrita idempotente.** O efeito no Delta é o de exactly-once. Demonstração no roteiro:

| Passo | O que acontece | Eventos lidos | Linhas no Delta | Checkpoint |
|---|---|---:|---:|---:|
| Primeiro consumo | INSERTs da carga + 23 UPDATEs do próprio loader | 3.057 | 3.034 | 0 → 3.057 |
| Mudança no OLTP | FGA0137 renomeada, 60 h → 90 h | — | — | — |
| Queda simulada (`FAIL_BEFORE_CHECKPOINT=1`) | MERGE feito, checkpoint **não** avançado | 1 | 3.034 | 3.057 |
| Reexecução | relê o mesmo evento; o MERGE não duplica | 1 | 3.034 | 3.058 |
| De novo | nada novo | 0 | 3.034 | 3.058 |

`ingestion/verify_e2.py` confere, contra o OLTP, uma linha por chave e as contagens por tabela iguais às do banco.

## Armazenamento aberto

**Delta Lake sobre Parquet**, não Iceberg:

- **Sem catálogo:** o Delta faz commit atômico com o `_delta_log` no próprio diretório, sem serviço novo no Compose.
- **No cliente Python:** MERGE e overwrite por predicado funcionam com a biblioteca `deltalake`, sem Spark.
- **Arquivos comuns:** os dados são Parquet comum, que o pyarrow, o DuckDB e o Spark leem sem a biblioteca Delta.

## Serialização e compressão

Medido por `ingestion/medir_formatos.py`: mediana de 20 leituras do padrão de acesso real (ler um semestre ou a série e agregar vagas por curso). Tabela completa em [`e2-formatos.txt`](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/blob/main/docs/evidencias/e2-formatos.txt).

| Formato | Tamanho | Ler 2024.1 + agregar | Ler série + agregar |
|---|---:|---:|---:|
| CSV | 240 kB | ~1,0 ms | ~0,9 ms |
| Parquet snappy, 1 arquivo | 16 kB | 0,58 ms | 0,42 ms |
| Parquet zstd, 1 arquivo | 13 kB | 0,41 ms | 0,32 ms |
| Parquet zstd, por `ano/periodo` | 51 kB | 0,42 ms | 0,94 ms |

- **Colunar:** toda leitura usa 2 a 4 das 11 colunas.
- **zstd:** o dado é escrito uma vez por semestre e lido muitas vezes. É o menor arquivo e o mais rápido de ler.
- **Partição por semestre:** neste volume, custa 3,8× mais bytes e deixa a leitura da série 3× mais lenta. Mesmo assim fica, porque a **escrita** é por semestre: o dado atrasado e o reprocessamento reescrevem ~200 linhas, não a tabela inteira.

## Por que não Debezium

A opção nula, recarga agendada, responde à pergunta: a recarga completa leva menos de 3 s, e o dado muda uma vez por semestre. A outbox mostra a mudança atravessando o fluxo sem somar JVM, Kafka e Connect ao Compose.

O gatilho para trocar por Debezium + Kafka:

- latência exigida abaixo de 1 minuto; ou
- mais de um consumidor da mesma mudança.
