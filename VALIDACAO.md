# Validação da revisão 1.1

Data: 05/10/2026.

- Testes Python: 12 casos, com fixtures sintéticas e banco temporário SQLite.
- Cobertura: mapas revisados, colunas, nulos/zero, números, coortes, taxas,
  duplicatas, conflitos, destino preservado, carga reaplicável, referência
  ponderada, exclusão da instituição-alvo e intervalos anuais sem observação.
- Documentação: `mkdocs build --strict` concluído.
- Planilha: conteúdos atualizados, áreas alteradas renderizadas e conferidas,
  fórmulas de acompanhamento recalculadas, sem erros detectados na verificação.
- Cabeçalhos e exemplos fictícios do modelo da planilha preservados.

Limitações: ZIPs oficiais do Inep retornaram HTTP 502. Nenhuma carga oficial
foi processada. DDL/cargas e visões ainda precisam ser aplicadas no PostgreSQL
da equipe e conectadas ao dashboard, cujo código não consta no pacote original.
Não há benchmark de desempenho nem ganho Parquet medido nesta revisão.
