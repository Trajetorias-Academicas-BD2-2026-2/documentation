# Roteiro de apresentação

Use esta página como guia da defesa:

**problema → dados → pipeline → camada analítica → dashboard → camada
vetorial → evidências e limites**.

## 1. Problema

O projeto analisa a evolução das vagas reservadas publicadas para os cursos
da FCTE entre 2022.1 e 2026.1, considerando as disciplinas obrigatórias do
currículo de referência de 2026.1. Vaga reservada não significa vaga ocupada
nem oferta total de vagas.

## 2. Dados e pipeline

Apresente o fluxo:

```text
coleta → validação → PostgreSQL → transformações → indicadores → consumo
```

Consulte a [visão geral](projeto/visao-geral.md), as
[fontes de dados](dados/fontes.md) e as
[etapas do pipeline](pipeline/etapas.md).

## 3. E3: camada analítica

```text
OLTP → staging → fct_reservas → mart_observatorio → dashboard
```

O modelo calcula vagas reservadas, disciplinas obrigatórias com reserva e
turmas com reserva. A decisão está na
[ADR-003](decisoes/adr-003-camada-analitica-observatorio-e3.md).

## 4. Dashboard

O dashboard depende do PostgreSQL, das migrações, da carga e do dbt. No
repositório principal:

```bash
docker compose up --build
```

Depois abra `http://localhost:8080` e filtre um curso e um semestre.

## 5. Camada vetorial

A camada vetorial usa pgvector para encontrar disciplinas semanticamente
parecidas. Ela gera embeddings de 384 dimensões e usa índice HNSW.

```bash
docker compose --profile ml run --rm ml
docker compose --profile ml run --rm ml-tests
```

Resultado validado:

- 638 textos vetorizados;
- 100% das 72 disciplinas do fato com vetor;
- vetores com 384 dimensões e norma 1;
- testes finalizados com código 0.

Os scripts completos estão no
[repositório principal](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas).

## 6. Fechamento

Destaque que o projeto mede reservas publicadas, não ocupação real; que o
dashboard é uma demonstração local; e que a camada vetorial apoia busca
semântica sem substituir o modelo analítico relacional.
