# Glossário

| Termo | Significado |
|---|---|
| **ACID** | Garantias de transações: Atomicidade, Consistência, Isolamento e Durabilidade |
| **ADR** | *Architecture Decision Record*: registro de uma decisão de arquitetura, com alternativas e consequências |
| **At-least-once** | Semântica em que cada evento é entregue uma ou mais vezes; precisa de escrita idempotente para não duplicar |
| **Backfill** | Reprocessar um intervalo passado (aqui, um semestre) sem refazer o resto |
| **CDC** | *Change Data Capture*: captura das mudanças (INSERT, UPDATE, DELETE) de um banco para levá-las a outro destino |
| **Checkpoint** | Posição do último evento que o consumidor processou com sucesso |
| **Checksum (SHA-256)** | Valor calculado do arquivo para provar que ele não mudou |
| **Currículo de referência** | Versão curricular em vigor em 2026.1, usada como conjunto fixo de obrigatórias em toda a série |
| **dbt** | Ferramenta que versiona transformações SQL como modelos, com testes e linhagem |
| **Delta Lake** | Formato de tabela aberto sobre Parquet, com log de transações, MERGE e versões (time travel) |
| **Dado atrasado** | Registro que chega depois do período a que pertence; aqui entra na partição do semestre do evento |
| **Freshness** | Quão recente é o dado de uma tabela em relação à origem |
| **Granularidade** | O que uma linha representa; no fato, uma turma reservando vagas para um curso |
| **Idempotência** | Repetir uma execução com a mesma entrada sem duplicar nem alterar o resultado |
| **Insert-only** | Tabela que só recebe INSERT; o passado não é reescrito |
| **LGPD** | Lei Geral de Proteção de Dados Pessoais (Lei nº 13.709/2018) |
| **Lote** | Recorte de coleta versionado (aqui, `coleta_publica_2026-09-28`) |
| **Mart** | Tabela de consumo, já agregada para uma pergunta |
| **MERGE** | Escrita que atualiza a linha se a chave existe e insere se não existe |
| **Outbox** | Tabela que recebe, na mesma transação da mudança, um evento a ser entregue depois |
| **Parquet** | Formato de arquivo colunar, binário e comprimido |
| **Reserva de vaga** | Vagas de uma turma guardadas para um curso ("Vgs Reservadas" no SIGAA); não é ocupação |
| **SCD** | *Slowly Changing Dimension*: dimensão que muda devagar; no tipo 2, cada mudança vira uma versão nova com validade |
| **SIGAA** | Sistema Integrado de Gestão de Atividades Acadêmicas da UnB |
| **SLA** | Compromisso de serviço; aqui, o mart reflete uma carga nova em até 24 h |
| **Snapshot (dbt)** | Mecanismo do dbt que guarda versões de uma tabela a cada execução, base da SCD 2 |
| **zstd** | Zstandard, algoritmo de compressão usado nos arquivos Parquet |

**Referências:** Reis & Housley, *Fundamentos de Engenharia de Dados* (Novatec, 2023); Kleppmann, *Designing Data-Intensive Applications*.
