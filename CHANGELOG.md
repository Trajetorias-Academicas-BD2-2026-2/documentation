# Histórico

## 2.0 — 17/11/2026

O site passa a descrever o projeto implementado, não o plano inicial.

- Removidas as páginas do plano da planilha: alunos, matrícula, ocupação,
  perguntas Q1–Q12, plano de validação e pendências. A pergunta de gestão
  mudou para vagas reservadas na E1 (ADR-0003), porque a série de ocupação
  não é pública.
- Removida a extensão Inep (F4/F5): `scripts/`, `sql/`, `tests/`, `config/`,
  `VALIDACAO.md`. Ela nunca teve carga oficial, porque os ZIPs retornavam
  HTTP 502, e não faz parte do projeto entregue.
- ADRs do site substituídos pelos ADR-0001 a 0006 do repositório do código.
- Novas páginas:
  - entregas E1, E2 e E3, com checklist, evidência e comando;
  - fonte e coleta, modelo OLTP, carga de trabalho e camada analítica;
  - ingestão, orquestração, qualidade e desempenho;
  - painel e governança;
  - diário de bordo.
- Apresentação e glossário atualizados.
- Workflow sem o passo de testes do Inep.


## 1.1 — 05/10/2026

- Acrescentadas F4 e F5 do Inep, com links, edições, granularidades e limites.
- Novas perguntas Q9–Q12 e regras de grupos comparáveis e médias ponderadas.
- Seis tabelas SQL no schema `inep` e visões de evolução, referência e mapa local.
- Coleta com manifesto/SHA-256; inspeção e tratamento com mapa de colunas revisado.
- Carga SQL transacional, validações e testes sintéticos temporários.
- Planilha atualizada, com riscos e exemplos do modelo preservados.
- Carga oficial, aplicação no PostgreSQL e conexão ao dashboard permanecem pendentes.
