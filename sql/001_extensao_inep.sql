-- PostgreSQL. Schema isolado: não altera as tabelas existentes da UnB.
BEGIN;
CREATE SCHEMA IF NOT EXISTS inep;
CREATE TABLE IF NOT EXISTS inep.instituicao (
 codigo_ies text PRIMARY KEY, nome_ies text NOT NULL
);
CREATE TABLE IF NOT EXISTS inep.curso (
 codigo_ies text NOT NULL REFERENCES inep.instituicao,
 codigo_curso text NOT NULL, nome_curso text NOT NULL,
 PRIMARY KEY (codigo_ies,codigo_curso)
);
CREATE TABLE IF NOT EXISTS inep.curso_local (
 codigo_local text PRIMARY KEY, nome text NOT NULL, campus text NOT NULL,
 grau text NOT NULL, modalidade text NOT NULL
);
CREATE TABLE IF NOT EXISTS inep.mapa_curso (
 codigo_local text NOT NULL REFERENCES inep.curso_local,
 ano integer NOT NULL CHECK(ano BETWEEN 1900 AND 2200),
 codigo_ies text NOT NULL, codigo_curso text NOT NULL,
 evidencia text NOT NULL CHECK(length(trim(evidencia))>0),
 PRIMARY KEY(codigo_local,ano),
 FOREIGN KEY(codigo_ies,codigo_curso) REFERENCES inep.curso
);
CREATE TABLE IF NOT EXISTS inep.censo_curso_ano (
 codigo_ies text NOT NULL, codigo_curso text NOT NULL,
 ano integer NOT NULL CHECK(ano BETWEEN 1900 AND 2200),
 area text NOT NULL, grau text NOT NULL, modalidade text NOT NULL,
 categoria text NOT NULL,
 matriculas bigint NOT NULL CHECK(matriculas>=0),
 ingressantes bigint NOT NULL CHECK(ingressantes>=0),
 concluintes bigint NOT NULL CHECK(concluintes>=0),
 vagas bigint CHECK(vagas>=0), origem_sha256 text NOT NULL,
 PRIMARY KEY(codigo_ies,codigo_curso,ano),
 FOREIGN KEY(codigo_ies,codigo_curso) REFERENCES inep.curso
);
CREATE TABLE IF NOT EXISTS inep.trajetoria_curso_coorte_ano (
 codigo_ies text NOT NULL, codigo_curso text NOT NULL,
 ano_ingresso integer NOT NULL CHECK(ano_ingresso BETWEEN 1900 AND 2200),
 ano integer NOT NULL CHECK(ano BETWEEN ano_ingresso AND 2200),
 area text NOT NULL, grau text NOT NULL, modalidade text NOT NULL,
 categoria text NOT NULL,
 ingressantes_coorte bigint NOT NULL CHECK(ingressantes_coorte>0),
 taxa_permanencia numeric(7,3) NOT NULL CHECK(taxa_permanencia BETWEEN 0 AND 100),
 taxa_conclusao numeric(7,3) NOT NULL CHECK(taxa_conclusao BETWEEN 0 AND 100),
 taxa_desistencia numeric(7,3) NOT NULL CHECK(taxa_desistencia BETWEEN 0 AND 100),
 origem_sha256 text NOT NULL,
 PRIMARY KEY(codigo_ies,codigo_curso,ano_ingresso,ano),
 FOREIGN KEY(codigo_ies,codigo_curso) REFERENCES inep.curso,
 CHECK(abs(taxa_permanencia+taxa_conclusao+taxa_desistencia-100)<=0.2)
);
CREATE INDEX IF NOT EXISTS censo_grupo ON inep.censo_curso_ano(ano,area,grau,modalidade,categoria);
CREATE INDEX IF NOT EXISTS trajetoria_grupo ON inep.trajetoria_curso_coorte_ano(ano_ingresso,ano,area,grau,modalidade,categoria);
COMMIT;
