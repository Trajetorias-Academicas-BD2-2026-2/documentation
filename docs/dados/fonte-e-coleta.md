# Fonte e coleta

## Fonte

Páginas públicas do **SIGAA da UnB**, sem login e sem dados de alunos:

- **Turmas por curso e semestre:** disciplina, turma, horário, docentes e o campo "Vgs Reservadas", com as vagas que a turma reserva para aquele curso.
- **Catálogo de componentes da FCTE:** código, nome, tipo e carga horária.
- **Estruturas curriculares:** versões de currículo de cada curso, com a natureza (obrigatória ou optativa) de cada componente.
- **Detalhe de componente:** pré-requisitos, coletados para uma amostra.

## Lote de 28/09/2026

A coleta foi feita por navegação nas páginas públicas e salva em [`data/coleta_publica_2026-09-28/`](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/tree/main/data/coleta_publica_2026-09-28). As evidências (JSON) e o `SHA256SUMS.txt` ficam no repositório. O lote ocupa 903 kB, abaixo do limite de 5 MB para versionar.

| Conjunto | Quantidade |
|---|---:|
| Consultas curso × semestre | 45 (5 cursos × 9 semestres), todas com registros |
| Registros curso–turma–semestre | 1.786 |
| Turmas distintas | 735 |
| Componentes do catálogo da FCTE | 585 |
| Versões curriculares | 6 (duas de Automotiva) |
| Vínculos currículo–componente | 625 |
| Componentes com pré-requisitos | 23 (coleta parcial) |

Relatório completo: [`docs/COLETA_SIGAA_2026-09-28.md`](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/blob/main/docs/COLETA_SIGAA_2026-09-28.md).

## Por que um lote versionado

Os primeiros scrapers (Playwright) falharam em quatro pontos do site real, e o formulário geral de turmas não devolveu o histórico da FCTE. Uma carga que depende do SIGAA no ar e com o mesmo layout não se reproduz.

Por isso a carga lê o lote versionado:

1. confere cada arquivo contra `SHA256SUMS.txt`;
2. valida o recorte: 5 cursos × 9 semestres, cada um encerrado segundo o calendário acadêmico oficial antes de ser coletado;
3. carrega tudo numa única transação.

Decisão no [ADR-0004](../decisoes/0004-coleta-publica-versionada.md).

`loader/coletar_ofertas_por_curso.py` (requests + BeautifulSoup) gera lotes novos de reservas. Ele foi validado contra o navegador em Software/2022.1: 60 registros, mesmas disciplinas, turmas, vagas, horários e docentes.

## Calendário acadêmico

`data/calendario_academico.csv` traz as datas oficiais de encerramento de cada semestre, com a URL da fonte. Um semestre está encerrado na data mais tardia entre o último dia de aulas, o último dia letivo e o prazo de consolidação no SIGAA. O banco recusa turma de semestre ainda não encerrado.

## Resultado da carga

- **Inseridas:** 733 turmas e 1.776 reservas.
- **Rejeitadas:** 10 reservas (2 turmas com horário ou docente divergente entre cursos), registradas em `debug/rejeitados.csv`.
- **Reexecução:** rodar o mesmo lote de novo não insere nem altera nada.
