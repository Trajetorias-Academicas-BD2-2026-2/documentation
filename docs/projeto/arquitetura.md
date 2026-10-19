# Arquitetura proposta

A planilha propõe **PostgreSQL** para os relacionamentos e consultas SQL, **Parquet** para conjuntos analíticos e **Python** para coleta e transformação. O processamento acompanha as atualizações das fontes, em lote.

!!! note "Proposta de organização"
    A separação abaixo concilia os blocos da planilha e explicita pontos ainda abertos. Não representa infraestrutura implantada nem altera o status **proposto** do [ADR-001](../decisoes/adr-001-postgresql-parquet.md).

!!! success "Implementação da E2"
    O recorte da E2 validou a camada aberta com Parquet particionado e Delta
    Lake. O caminho de mudanças usa outbox transacional no PostgreSQL e
    consumidor com checkpoint. A implementação e os resultados estão na
    [página da E2](../pipeline/ingestao-e2.md) e no
    [ADR-003](../decisoes/adr-003-ingestao-e2.md).

## Camadas e responsabilidades

```mermaid
flowchart TB
    subgraph fontes[Fontes externas]
        F1[F1 · Alunos]
        F2[F2 · Turmas]
        F3[F3 · Componentes]
        F4[F4 · Censo Inep]
        F5[F5 · Trajetória Inep]
    end
    F1 --> C[P1–P3 e P9–P10 · Coleta]
    F2 --> C
    F3 --> C
    F4 --> C
    F5 --> C
    C --> S3[(S3 · Originais CSV / JSON)]
    S3 --> P4[P4 · Validação e limpeza]
    P4 --> P5[P5 · Integração]
    P5 --> S1[(S1 · PostgreSQL principal)]
    S1 --> P6[P6 · Preparação analítica]
    P6 --> S2[(S2 · PostgreSQL analítico)]
    P6 --> PQ[Conjuntos Parquet]
    S2 --> P7[P7 · Indicadores]
    PQ -. Leitura a validar na PoC .-> P7
    P7 --> P8[P8 · Dashboard]
    P8 --> U[Coordenação / ingressantes]
```

| Camada | Responsabilidade | Critério de saída proposto |
|---|---|---|
| Bruta — S3 | Preservar o arquivo recebido e sua identificação de origem | Download íntegro, versão e data da coleta registradas |
| Tratamento — P4 | Padronizar tipos, identificar duplicatas e separar inconsistências | Relatório de qualidade por fonte |
| Integrada — S1 | Representar as entidades e preservar vínculos validados | Chaves e relacionamentos verificados |
| Analítica — S2 e Parquet | Preparar recortes e agregações para as perguntas do projeto | Indicadores conciliados com os dados de entrada |
| Consumo — P8 | Apresentar filtros, resultados e atualização dos dados | Exibir somente uma versão validada da carga |

## PostgreSQL e Parquet: divisão proposta

**PostgreSQL principal (S1)** mantém os dados integrados e suas restrições. A aba 4 o classifica como OLTP; a carga real ainda precisa ser avaliada, pois o pipeline descrito é predominantemente em lote.

**PostgreSQL analítico (S2)** é o destino proposto para tabelas ou visões usadas pelo dashboard. A separação é lógica neste desenho: schemas, bancos ou instâncias separados ainda precisam ser escolhidos conforme a prova de conceito e os recursos disponíveis.

**Parquet** armazena conjuntos tratados e exportações analíticas para processamento em Python e comparação de desempenho. O leitor e as consultas que acessarão esses arquivos diretamente ainda estão a definir. O formato, por si só, não define o serviço de consulta.

## Preservação dos dados brutos

O bloco de cargas e as etapas de coleta pedem preservação dos originais; o texto do ADR também menciona brutos em Parquet. A proposta desta documentação é **manter o original em CSV/JSON e produzir Parquet como derivado**, permitindo repetir a transformação. Esse alinhamento precisa ser confirmado pela equipe antes da aceitação do ADR.

## Atualização e falhas

Uma nova coleta deve gerar uma versão identificável dos dados. As validações de P4–P7 precedem a disponibilização ao dashboard. Se uma execução falhar, a proposta é manter a última versão validada e informar sua data, em vez de expor uma carga parcial.

Os controles estão em [Qualidade e reprocessamento](../pipeline/qualidade.md). As metas de latência da planilha estão em [Cargas e engines](../dados/cargas-e-engines.md) e ainda não são resultados medidos.

### Ingestão e publicação da E2

| Caminho | Entrada | Destino | Garantia demonstrada |
|---|---|---|---|
| Lote | Coleta pública versionada | Parquet + Delta, por `ano/periodo` | Reexecução sem duplicação |
| Mudanças | OLTP → outbox transacional | Delta sobre Parquet | At-least-once com deduplicação por chave |

O dado atrasado é atribuído ao período do evento. A janela correspondente é
reprocessada, em vez de usar a data de consumo como partição.

## Integração da extensão Inep

F4 e F5 entram por P9 e P10 e convergem em P4–P7, sem mudar os IDs originais.
`scripts/inep_pipeline.py` implementa coleta, inspeção, normalização, manifesto,
relatório de qualidade e geração de SQL. As cargas no PostgreSQL são transacionais.
O schema `inep` preserva a separação entre agregados anuais e dados locais semestrais.
CSV e SQL são produzidos nesta versão; Parquet continua como exportação opcional.
[Como executar](../pipeline/execucao-inep.md).

A extensão foi verificada com dados sintéticos. Cargas oficiais, benchmark e
conexão às telas do dashboard da equipe permanecem pendentes por falta de dados
e código do dashboard no pacote recebido.
