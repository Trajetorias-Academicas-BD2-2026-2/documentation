# Cargas e engines

Cada armazenamento do projeto tem um **tipo de carga** (OLTP ou OLAP), um motor escolhido
e um conjunto de **garantias ACID**. A pergunta central não é "tem ACID?", e sim:
**de qual garantia dá para abrir mão — e quem cobre o buraco?**

## Resumo

| ID | Armazenamento | O que guarda | Carga | Serviço | Latência aceitável | Disponibilidade |
|---|---|---|---|---|---|---|
| S1 | Banco principal | Alunos, componentes curriculares, turmas, períodos e matrículas | OLTP | PostgreSQL | < 1 s | Alta |
| S2 | Base analítica | Dados consolidados e indicadores de oferta e demanda | OLAP | PostgreSQL | < 5 s | Média |
| S3 | Dados brutos | Arquivos originais obtidos dos datasets da UnB | OLAP | Sistema de arquivos | < 30 s | Média |

!!! note "Metas e classificações de planejamento"
    Latências e disponibilidade são requisitos declarados, ainda sem benchmark. A aba 4 classifica S1 como OLTP, mas a caracterização precisa ser confirmada com a carga real. A separação física de S1 e S2 ainda não foi definida; veja a [arquitetura proposta](../projeto/arquitetura.md).

## Garantias ACID

| Armazenamento | Necessárias | Abre mão de | Quem cobre o buraco |
|---|---|---|---|
| **S1 — Banco principal** | A, C, I e D | Nenhuma | — |
| **S2 — Base analítica** | C, I e D | A (atomicidade) | O pipeline pode refazer a carga a partir dos dados brutos |
| **S3 — Dados brutos** | D | A, C e I | Os arquivos podem ser obtidos de novo nas fontes oficiais e reprocessados |

!!! abstract "Legenda ACID"
    **A**tomicidade · **C**onsistência · **I**solamento · **D**urabilidade.

!!! note "Garantias a validar na implementação"
    A tabela preserva as escolhas da planilha. Refazer uma carga não impede leituras parciais durante uma falha; a publicação da base analítica precisa de um mecanismo consistente. Também não há garantia de que uma fonte externa continuará oferecendo uma versão antiga. A proposta é preservar cópias identificadas dos originais e validar a carga antes de publicá-la, conforme [Qualidade e reprocessamento](../pipeline/qualidade.md).

## Detalhes

### S1 — Banco principal

- **Orientação:** linha.
- **Volume estimado em 1 ano:** a confirmar.
- **Justificativa:** o domínio tem muitos relacionamentos e exige integridade entre as entidades. O PostgreSQL oferece chaves primárias e estrangeiras, restrições e transações para manter os dados consistentes.

### S2 — Base analítica

- **Orientação:** linha (PostgreSQL), complementada por arquivos Parquet — veja [Formatos](formatos.md).
- **Volume estimado em 1 ano:** a confirmar.
- **Justificativa:** as consultas são predominantemente analíticas (filtros, agrupamentos e comparações por disciplina, período e turno). Separar a carga analítica evita sobrecarregar as operações principais.

### S3 — Dados brutos

- **Orientação:** não se aplica.
- **Volume estimado em 1 ano:** a confirmar.
- **Justificativa:** manter os dados originais facilita auditoria, reprodução do processamento e recuperação da base analítica.

!!! tip "Relatório pesado não roda no banco de produção"
    Por isso a carga analítica (S2) é separada do banco principal (S1).

## Ampliação de conteúdo

S1 recebe referências institucionais, cursos e correspondências revisadas;
S2 recebe Censo anual, trajetórias de coortes e visões de comparação;
S3 preserva também ZIPs oficiais do Inep e manifestos. Não se acrescenta outro
SGBD. A carga SQL da extensão exige atomicidade, consistência, isolamento e
durabilidade: reprocessar não autoriza expor uma carga parcial.
