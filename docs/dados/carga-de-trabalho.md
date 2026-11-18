# Carga de trabalho

Passo 1 do Método de Decisão. Os números são medidos por `loader/caracterizar.py` sobre o banco carregado:

```bash
docker compose run --rm -T loader python caracterizar.py > docs/carga-medida.md
```

Saída: [`docs/carga-medida.md`](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/blob/main/docs/carga-medida.md). A interpretação está em [`docs/carga-de-trabalho.md`](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/blob/main/docs/carga-de-trabalho.md).

## Volume

| Tabela | Linhas (lote de 28/09/2026) | Crescimento |
|---|---:|---|
| `turma` | 733 | +71 a +92 por semestre |
| `reserva_vaga` | 1.776 | +155 a +255 por semestre (média 197) |
| `turma_docente` | 773 | acompanha `turma` |
| `disciplina` | 633 | quase estático |
| `curriculo` / `curriculo_componente` | 6 / 625 | a cada revisão de currículo |
| `curso` | 5 | estático |

O banco inteiro ocupa 1,1 MB com índices, e o lote, 903 kB.

## Cardinalidade

- Uma turma reserva vagas para 1 a 5 cursos (média 2,42); 38% atendem mais de um curso.
- As consultas agrupam por curso (5) e semestre (9). Turno não entra na pergunta: 720 das 733 turmas são diurnas.

## Escrita

- **Uma carga em lote por semestre encerrado.** Nada é escrito entre cargas.
- **`turma`, `turma_docente` e `reserva_vaga` só recebem INSERT.** O catálogo e o currículo recebem upsert na mesma carga.

## Leitura

| Parâmetro | Valor |
|---|---|
| Usuários | 5 coordenadores (um por curso) |
| Pico | cerca de 50 consultas por semana, nas 4 semanas de planejamento antes da matrícula |
| Fora do pico | perto de zero |
| Padrão | sempre agregado por curso e semestre; nenhuma busca por registro único |

A taxa de leitura é uma estimativa da Squad, ainda não validada com um coordenador. Mesmo dez vezes maior, ela não pressiona o banco: cada consulta de referência leva menos de 10 ms.

## Latência tolerada

**Até 2 s por consulta.** É apoio à decisão semestral, não tempo real. Medido: todas as consultas de referência ficam abaixo de 10 ms. A consulta da pergunta foi otimizada na E3 ([Desempenho](../pipeline/desempenho.md)).
