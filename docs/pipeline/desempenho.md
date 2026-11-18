# Desempenho

## Consulta otimizada a partir do plano

A consulta da pergunta de gestão ([`q0_pergunta_de_gestao.sql`](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/blob/main/db/consultas/q0_pergunta_de_gestao.sql)) foi medida com `EXPLAIN (ANALYZE, BUFFERS)`:

```bash
docker compose exec -T db psql -U g2 -d ofertas_unb -X -f - < db/consultas/q6_explain_reservas.sql
```

| | Plano | Buffers | Tempo |
|---|---|---:|---:|
| [Antes](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/blob/main/docs/evidencias/explain-antes.txt) | nested loop com 1.681 buscas por índice em `reserva_vaga` | 5.721 | 3,0 ms |
| [Depois](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/blob/main/docs/evidencias/explain-depois.txt) | hash joins; agrega antes de juntar `curso` | 188 | 1,9 ms |

**O que o plano mostrou:**

- **Estimativa errada:** a versão original juntava o fato a um CTE agregado (`total`). O planner não tem estatística de colunas de CTE e estimou 5 linhas onde havia 254. Com isso, achou barato fazer uma busca por índice para cada uma das 1.681 linhas de turma.
- **A reescrita:** a consulta agrega primeiro (curso × currículo × semestre) e só depois junta `curso`. A estimativa deixa de importar e o planner troca para hash joins com uma leitura sequencial de `reserva_vaga`, que tem 13 páginas.
- **Resultado:** 30× menos buffers. A saída das duas versões é idêntica, conferida com `diff`.

**Índice redundante:** o plano também mostrou que o índice `idx_reserva_vaga_turma_curso`, criado na V008, era idêntico à chave primária. A V011 o remove: ele só custava escrita e espaço.

**Contexto:** as duas versões ficam muito abaixo da latência tolerada de 2 s. Este exercício mostra como ler o plano e onde está o custo, não um gargalo real neste volume.

## Consultas de referência

As seis consultas de `db/consultas/` ficam abaixo de 10 ms no banco carregado ([`docs/carga-medida.md`](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/blob/main/docs/carga-medida.md)). O painel lê só os marts: 45, 676 e 254 linhas.
