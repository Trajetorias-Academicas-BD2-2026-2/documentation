# Formatos de armazenamento

Segundo a planilha, as fontes fornecem **CSV ou JSON**. A equipe propõe
padronizar o armazenamento analítico em **Apache Parquet**, um formato **binário e colunar**.

## Por que Parquet?

As análises do projeto raramente precisam de todas as colunas: filtram por período,
disciplina, turno ou situação e leem só alguns atributos de muitos registros. Nesse padrão,
o formato colunar:

1. lê **somente as colunas necessárias**, em vez do registro inteiro;
2. **comprime melhor** valores repetidos (ex.: turno, situação, código de curso);
3. mantém um **padrão único** entre as diferentes fontes.

## Conjuntos de dados

| ID | Conjunto | Fonte | Formato atual | Orientação | Formato proposto |
|---|---|---|---|---|---|
| D1 | Dados dos alunos | F1 | CSV (texto) | Linha | **Parquet** |
| D2 | Turmas | F2 | CSV (texto) | Linha | **Parquet** |
| D3 | Componentes curriculares | F3 | CSV / JSON (texto) | Linha | **Parquet** |
| D4 | Dados integrados para análise de oferta | F1, F2 e F3 | Parquet (binário) | Coluna | **Parquet** (mantido) |

!!! note "Original e derivado"
    A proposta de arquitetura mantém o arquivo recebido em CSV/JSON e gera Parquet como derivado tratado ou analítico. D4 é o conjunto integrado previsto na planilha; seu formato descrito não comprova uma implementação existente. O alinhamento com o texto do ADR permanece pendente.

## Justificativas

=== "D1 — Alunos"

    - **Como é lido:** poucas colunas, conforme os indicadores analisados.
    - **Frequência de leitura:** semestral / durante as análises.
    - **Justificativa:** o sistema não usa todas as colunas em cada análise; o formato colunar seleciona só os atributos necessários e comprime bem grandes volumes tabulares.
    - **Ganho esperado:** menor uso de armazenamento e menos dados lidos.

=== "D2 — Turmas"

    - **Como é lido:** poucas colunas, com filtros por período, disciplina e turma.
    - **Frequência de leitura:** semestral / durante as análises.
    - **Justificativa:** as consultas selecionam atributos específicos (período, código da disciplina, turno, vagas, situação da turma).
    - **Ganho esperado:** menor volume lido e melhor desempenho nas consultas analíticas.

=== "D3 — Componentes"

    - **Como é lido:** poucas colunas / busca por chave (código do componente).
    - **Frequência de leitura:** semestral / durante as análises.
    - **Justificativa:** usados para relacionar códigos de disciplinas à estrutura curricular; o formato permite selecionar só as colunas necessárias e unifica o padrão com as demais fontes.
    - **Ganho esperado:** padronização do armazenamento e menor volume de leitura.

=== "D4 — Dados integrados"

    - **Como é lido:** poucas colunas, com filtros por período/disciplina.
    - **Frequência de leitura:** sob demanda / semanal.
    - **Justificativa:** é o conjunto principal para gerar indicadores; Parquet filtra períodos, disciplinas e turnos sem carregar todas as colunas.
    - **Ganho esperado:** melhor desempenho nas consultas e menos armazenamento que o CSV.

!!! info "Tamanho estimado em 1 ano"
    Ainda **a confirmar** para todos os conjuntos. Os números serão medidos na
    [prova de conceito](../decisoes/adr-001-postgresql-parquet.md#evidencia-que-sustenta-a-decisao),
    comparando volume em CSV e em Parquet com os dados reais.

## Linha × coluna em uma frase

- **Linha** favorece quem lê registros inteiros.
- **Coluna** favorece quem lê poucos atributos de muitos registros.
- **Texto** é legível e volumoso; **binário** é compacto e opaco.

## Conjuntos da ampliação

| ID | Conjunto | Origem | Preservação e derivado |
|---|---|---|---|
| D5 | Censo curso/ano | F4 | ZIP original; CSV normalizado e carga SQL; Parquet opcional |
| D6 | Trajetória curso/coorte/ano | F5 | ZIP original; CSV normalizado e carga SQL; Parquet opcional |
| D7 | Correspondência de cursos | Revisão da equipe | Tabela relacional curso local/ano com evidência |

Volume, pureza e ganho de Parquet permanecem a medir. A implementação fornecida
não converte dados para Parquet automaticamente. [Contrato](integracao-inep.md).
