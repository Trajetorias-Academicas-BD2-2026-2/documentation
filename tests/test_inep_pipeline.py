"""Fixtures sintéticas temporárias: não são dados da UnB ou do Inep."""
import csv
import importlib.util
import json
from pathlib import Path
import sqlite3
import tempfile
from types import SimpleNamespace
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('pipeline',ROOT/'scripts/inep_pipeline.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)

def row(source='censo',**changes):
 item=dict(codigo_ies='10',nome_ies="Instituição de Teste",codigo_curso='100',nome_curso="Curso D'Água",
           ano='2024',area='0613',grau='1',modalidade='1',categoria='1')
 item.update(dict(matriculas='100',ingressantes='20',concluintes='10',vagas='30') if source=='censo' else
             dict(ano_ingresso='2015',ingressantes_coorte='100',taxa_permanencia='10',taxa_conclusao='60',taxa_desistencia='30'))
 item.update(changes);return item

def sqlite_schema(conn):
 schema=(ROOT/'sql/001_extensao_inep.sql').read_text()
 schema=schema.replace('CREATE SCHEMA IF NOT EXISTS inep;','').replace('inep.','')
 conn.executescript(schema)

class PipelineTests(unittest.TestCase):
 def transform(self,source='censo',**kw):
  r=row(source,**kw);return p.transform(r,{k:k for k in p.FIELDS[source]},source)
 def test_zero_distinto_de_ausencia(self):
  self.assertEqual(self.transform(matriculas='0',vagas='')['matriculas'],'0')
  self.assertEqual(self.transform(vagas='')['vagas'],'')
  with self.assertRaises(ValueError): self.transform(ingressantes='')
 def test_numeros_invalidos(self):
  for v in ['-1','NaN','1.5','abc']:
   with self.subTest(v=v),self.assertRaises(ValueError): self.transform(matriculas=v)
 def test_taxas_escala_total_e_coorte(self):
  self.assertEqual(self.transform('trajetoria',taxa_conclusao='60,1',taxa_desistencia='29,9')['taxa_conclusao'],'60.1')
  for changes in [{'taxa_conclusao':'101'},{'taxa_conclusao':'0.6'},{'ano_ingresso':'2025'},{'ingressantes_coorte':'0'}]:
   with self.subTest(changes=changes),self.assertRaises(ValueError): self.transform('trajetoria',**changes)
 def prepare(self,tmp,rows,source='censo',revised=True):
  base=Path(tmp);inp=base/'input.csv';mapping=base/'map.json'
  with inp.open('w',newline='',encoding='utf-8') as f:
   writer=csv.DictWriter(f,fieldnames=p.FIELDS[source],delimiter=';');writer.writeheader();writer.writerows(rows)
  mapping.write_text(json.dumps({'fonte':source,'revisado':revised,'dicionario_url':'https://example.invalid/dicionario-sintetico',
                                  'colunas':{k:k for k in p.FIELDS[source]}}))
  return SimpleNamespace(input=str(inp),mapping=str(mapping),source=source,output=str(base/'out'),member=None,encoding='utf-8',delimiter=';')
 def test_mapa_nao_revisado_bloqueia(self):
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(ValueError):p.normalize(self.prepare(d,[row()],revised=False))
 def test_duplicatas_iguais_e_reaplicacao_sql(self):
  with tempfile.TemporaryDirectory() as d:
   args=self.prepare(d,[row(),row()]);p.normalize(args)
   report=json.loads((Path(args.output)/'qualidade.json').read_text())
   self.assertEqual((report['linhas_unicas'],report['duplicatas_identicas']),(1,1))
   conn=sqlite3.connect(':memory:');sqlite_schema(conn)
   sql=(Path(args.output)/'carga.sql').read_text().replace('inep.','')
   conn.executescript(sql);conn.executescript(sql)
   self.assertEqual(conn.execute('SELECT count(*) FROM censo_curso_ano').fetchone()[0],1)
   self.assertEqual(conn.execute('SELECT nome_curso FROM curso').fetchone()[0],"Curso D'Água")
 def test_conflito_sem_publicacao(self):
  with tempfile.TemporaryDirectory() as d:
   args=self.prepare(d,[row(),row(matriculas='101')])
   with self.assertRaises(ValueError):p.normalize(args)
   self.assertFalse(Path(args.output).exists())
 def test_vazio_rejeitado(self):
  with tempfile.TemporaryDirectory() as d:
   args=self.prepare(d,[])
   with self.assertRaises(ValueError):p.normalize(args)
 def test_coluna_ausente_rejeitada(self):
  with tempfile.TemporaryDirectory() as d:
   args=self.prepare(d,[row()]);m=json.loads(Path(args.mapping).read_text());m['colunas']['matriculas']='inexistente';Path(args.mapping).write_text(json.dumps(m))
   with self.assertRaises(ValueError):p.normalize(args)
 def test_destino_existente_preservado(self):
  with tempfile.TemporaryDirectory() as d:
   args=self.prepare(d,[row()]);p.normalize(args)
   before=(Path(args.output)/'dados.csv').read_bytes()
   with self.assertRaises(ValueError):p.normalize(args)
   self.assertEqual(before,(Path(args.output)/'dados.csv').read_bytes())
 def test_media_ponderada_e_exclusao_instituicao(self):
  with tempfile.TemporaryDirectory() as d:
   rows=[row('trajetoria'),row('trajetoria',codigo_curso='101',taxa_conclusao='90',taxa_permanencia='0',taxa_desistencia='10'),
         row('trajetoria',codigo_ies='20',nome_ies='Referência A',codigo_curso='200',ingressantes_coorte='10',taxa_conclusao='20',taxa_permanencia='10',taxa_desistencia='70'),
         row('trajetoria',codigo_ies='30',nome_ies='Referência B',codigo_curso='300',ingressantes_coorte='30',taxa_conclusao='90',taxa_permanencia='0',taxa_desistencia='10')]
   args=self.prepare(d,rows,'trajetoria');p.normalize(args)
   c=sqlite3.connect(':memory:');sqlite_schema(c)
   c.executescript((Path(args.output)/'carga.sql').read_text().replace('inep.',''))
   views=(ROOT/'sql/002_indicadores_inep.sql').read_text().replace('CREATE OR REPLACE VIEW','CREATE VIEW').replace('inep.','')
   c.executescript(views)
   result=c.execute("SELECT cursos_referencia,instituicoes_referencia,conclusao_referencia,diferenca_conclusao_pp FROM v_comparacao_trajetoria WHERE codigo_ies='10' AND codigo_curso='100'").fetchone()
   self.assertEqual(result[:2],(2,2));self.assertAlmostEqual(result[2],72.5);self.assertAlmostEqual(result[3],-12.5)
 def test_comparacao_anual_e_intervalo_sem_observacao(self):
  with tempfile.TemporaryDirectory() as d:
   rows=[row(),row(ano='2022',matriculas='90'),row(codigo_ies='20',nome_ies='Referência A',codigo_curso='200',matriculas='110')]
   args=self.prepare(d,rows);p.normalize(args)
   c=sqlite3.connect(':memory:');sqlite_schema(c);c.executescript((Path(args.output)/'carga.sql').read_text().replace('inep.',''))
   c.executescript((ROOT/'sql/002_indicadores_inep.sql').read_text().replace('CREATE OR REPLACE VIEW','CREATE VIEW').replace('inep.',''))
   self.assertEqual(c.execute("SELECT variacao_matriculas,intervalo_anos FROM v_evolucao_censo WHERE codigo_ies='10' AND ano=2024").fetchone(),(10,2))
   self.assertEqual(c.execute("SELECT cursos_referencia,matriculas_medias_por_curso FROM v_comparacao_censo WHERE codigo_ies='10' AND ano=2024").fetchone(),(1,110.0))
 def test_referencia_inexistente_nula(self):
  with tempfile.TemporaryDirectory() as d:
   args=self.prepare(d,[row('trajetoria')],'trajetoria');p.normalize(args)
   c=sqlite3.connect(':memory:');sqlite_schema(c);c.executescript((Path(args.output)/'carga.sql').read_text().replace('inep.',''))
   c.executescript((ROOT/'sql/002_indicadores_inep.sql').read_text().replace('CREATE OR REPLACE VIEW','CREATE VIEW').replace('inep.',''))
   self.assertEqual(c.execute('SELECT cursos_referencia,conclusao_referencia FROM v_comparacao_trajetoria').fetchone(),(0,None))

if __name__=='__main__':unittest.main()
