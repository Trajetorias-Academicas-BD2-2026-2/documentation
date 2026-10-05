-- Executar depois de 001. Taxas em percentual; diferenças em pontos percentuais.
CREATE OR REPLACE VIEW inep.v_evolucao_censo AS
SELECT codigo_ies,codigo_curso,ano,matriculas,ingressantes,concluintes,vagas,
 matriculas-lag(matriculas) OVER(PARTITION BY codigo_ies,codigo_curso ORDER BY ano) AS variacao_matriculas,
 ano-lag(ano) OVER(PARTITION BY codigo_ies,codigo_curso ORDER BY ano) AS intervalo_anos
FROM inep.censo_curso_ano;

CREATE OR REPLACE VIEW inep.v_comparacao_censo AS
SELECT a.codigo_ies,a.codigo_curso,a.ano,a.matriculas,a.ingressantes,a.concluintes,
 count(b.codigo_curso) AS cursos_referencia,
 count(DISTINCT b.codigo_ies) AS instituicoes_referencia,
 avg(b.matriculas) AS matriculas_medias_por_curso,
 avg(b.ingressantes) AS ingressantes_medios_por_curso,
 avg(b.concluintes) AS concluintes_medios_por_curso
FROM inep.censo_curso_ano a
LEFT JOIN inep.censo_curso_ano b ON b.codigo_ies<>a.codigo_ies AND b.ano=a.ano
 AND b.area=a.area AND b.grau=a.grau AND b.modalidade=a.modalidade AND b.categoria=a.categoria
GROUP BY a.codigo_ies,a.codigo_curso,a.ano,a.matriculas,a.ingressantes,a.concluintes;

-- Uma linha por curso/coorte/ano. Referência exclui TODA a instituição-alvo.
-- Cada integrante deve ter a mesma área, grau, modalidade, categoria e janela.
CREATE OR REPLACE VIEW inep.v_comparacao_trajetoria AS
SELECT a.codigo_ies,a.codigo_curso,a.ano_ingresso,a.ano,
 a.ano-a.ano_ingresso AS anos_desde_ingresso,
 a.ingressantes_coorte,a.taxa_permanencia,a.taxa_conclusao,a.taxa_desistencia,
 count(b.codigo_curso) AS cursos_referencia,
 count(DISTINCT b.codigo_ies) AS instituicoes_referencia,
 sum(b.ingressantes_coorte) AS ingressantes_referencia,
 1.0*sum(b.taxa_conclusao*b.ingressantes_coorte)/nullif(sum(b.ingressantes_coorte),0) AS conclusao_referencia,
 1.0*sum(b.taxa_desistencia*b.ingressantes_coorte)/nullif(sum(b.ingressantes_coorte),0) AS desistencia_referencia,
 a.taxa_conclusao-1.0*sum(b.taxa_conclusao*b.ingressantes_coorte)/nullif(sum(b.ingressantes_coorte),0) AS diferenca_conclusao_pp,
 a.taxa_desistencia-1.0*sum(b.taxa_desistencia*b.ingressantes_coorte)/nullif(sum(b.ingressantes_coorte),0) AS diferenca_desistencia_pp
FROM inep.trajetoria_curso_coorte_ano a
LEFT JOIN inep.trajetoria_curso_coorte_ano b
 ON b.codigo_ies<>a.codigo_ies AND b.ano_ingresso=a.ano_ingresso AND b.ano=a.ano
 AND b.area=a.area AND b.grau=a.grau AND b.modalidade=a.modalidade AND b.categoria=a.categoria
GROUP BY a.codigo_ies,a.codigo_curso,a.ano_ingresso,a.ano,a.ingressantes_coorte,
 a.taxa_permanencia,a.taxa_conclusao,a.taxa_desistencia;

CREATE OR REPLACE VIEW inep.v_censo_curso_local AS
SELECT m.codigo_local,c.* FROM inep.mapa_curso m
JOIN inep.censo_curso_ano c ON c.codigo_ies=m.codigo_ies AND c.codigo_curso=m.codigo_curso AND c.ano=m.ano;

-- Q9: filtrar o curso pela correspondência revisada, nunca apenas pelo nome.
-- SELECT * FROM inep.v_censo_curso_local WHERE codigo_local='CODIGO_VALIDADO' ORDER BY ano;
-- Q10/Q11: consultar a coorte explicitamente; não somar edições sobrepostas.
-- SELECT * FROM inep.v_comparacao_trajetoria
-- WHERE codigo_ies='CODIGO_IES_VALIDADO' AND ano_ingresso=2015 ORDER BY codigo_curso,ano;
-- Q12: mapas incompletos precisam ser informados ao usuário, sem transformar ausência em zero.
-- SELECT l.codigo_local FROM inep.curso_local l WHERE NOT EXISTS
-- (SELECT 1 FROM inep.mapa_curso m WHERE m.codigo_local=l.codigo_local AND m.ano=2024);
