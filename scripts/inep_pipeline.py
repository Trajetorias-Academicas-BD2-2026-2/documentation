#!/usr/bin/env python3
"""Coleta e tratamento de F4/F5. Python 3.10+, biblioteca padrão.

Não cria resultados reais a partir de fixtures. Mapas de colunas exigem revisão
do dicionário publicado com a edição. A carga SQL é aplicada pelo usuário com psql.
"""
import argparse
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from urllib.parse import urlparse
from urllib.request import urlopen
import zipfile

COMMON = ['codigo_ies','nome_ies','codigo_curso','nome_curso','ano','area','grau','modalidade','categoria']
FIELDS = {
 'censo': COMMON + ['matriculas','ingressantes','concluintes','vagas'],
 'trajetoria': COMMON + ['ano_ingresso','ingressantes_coorte','taxa_permanencia','taxa_conclusao','taxa_desistencia']
}
NUMBERS = {'ano','ano_ingresso','matriculas','ingressantes','concluintes','vagas','ingressantes_coorte'}
RATES = {'taxa_permanencia','taxa_conclusao','taxa_desistencia'}

def digest(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
 return h.hexdigest()

def timestamp(): return datetime.now(timezone.utc).isoformat()

def atomic_json(path,obj):
 temp=Path(str(path)+'.tmp')
 temp.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 os.replace(temp,path)

def fetch(args):
 cfg=json.loads(Path(args.config).read_text(encoding='utf-8'))[args.source]
 parsed=urlparse(cfg['url'])
 if parsed.scheme!='https' or parsed.hostname!='download.inep.gov.br':
  raise ValueError('O endereço precisa ser HTTPS no domínio oficial download.inep.gov.br.')
 root=Path(args.output)/cfg['id']/cfg['edicao']; root.mkdir(parents=True,exist_ok=True)
 fd,tmp=tempfile.mkstemp(dir=root,suffix='.part'); os.close(fd)
 try:
  total=0
  with urlopen(cfg['url'],timeout=30) as response, open(tmp,'wb') as out:
   if response.status!=200: raise ValueError(f'Download incompleto: HTTP {response.status}')
   final=urlparse(response.geturl())
   if final.scheme!='https' or final.hostname!='download.inep.gov.br': raise ValueError('Redirecionamento fora do domínio oficial.')
   for chunk in iter(lambda:response.read(1024*1024),b''):
    total+=len(chunk)
    if total>args.max_bytes: raise ValueError('Arquivo excede o limite de bytes configurado.')
    out.write(chunk)
  if not total or not zipfile.is_zipfile(tmp): raise ValueError('Resposta não é um ZIP íntegro.')
  with zipfile.ZipFile(tmp) as z:
   if z.testzip() is not None: raise ValueError('CRC inválido no ZIP.')
  sha=digest(tmp); dest=root/sha; dest.mkdir(exist_ok=True)
  target=dest/Path(parsed.path).name
  os.replace(tmp,target)
  atomic_json(dest/'manifesto.json',{'fonte':args.source,'edicao':cfg['edicao'],'url':cfg['url'],
    'pagina':cfg['pagina'],'coletado_em':timestamp(),'sha256':sha,'bytes':total})
  print(target)
 except Exception as exc:
  atomic_json(root/'ultima_falha.json',{'em':timestamp(),'url':cfg['url'],'erro':str(exc),'status':'falhou'})
  raise
 finally:
  if os.path.exists(tmp): os.unlink(tmp)

def open_csv(path,member,encoding):
 # Lê o membro diretamente. Não extrai nomes de caminhos fornecidos pelo ZIP.
 if zipfile.is_zipfile(path):
  if not member: raise ValueError('Informe --member com o CSV exato mostrado pelo comando inspect.')
  z=zipfile.ZipFile(path)
  info=z.getinfo(member)
  if info.file_size>2_000_000_000: z.close(); raise ValueError('Membro descompactado excede 2 GB.')
  stream=io.TextIOWrapper(z.open(info),encoding=encoding,newline='')
  return stream,z
 return open(path,encoding=encoding,newline=''),None

def inspect_file(args):
 if zipfile.is_zipfile(args.input) and not args.member:
  with zipfile.ZipFile(args.input) as z:
   print(json.dumps([{'arquivo':i.filename,'bytes':i.file_size} for i in z.infolist() if not i.is_dir()],ensure_ascii=False,indent=2))
  return
 f,z=open_csv(args.input,args.member,args.encoding)
 try:
  reader=csv.reader(f,delimiter=args.delimiter)
  header=next(reader)
  print(json.dumps({'colunas':header,'amostra':list(row for _,row in zip(range(3),reader))},ensure_ascii=False,indent=2))
 finally:
  f.close()
  if z: z.close()

def template(args):
 mapping={key:None for key in FIELDS[args.source]}
 atomic_json(Path(args.output),{'fonte':args.source,'revisado':False,'dicionario_url':None,'colunas':mapping})

def numeric(value,integer=False):
 try:
  n=Decimal(str(value).strip().replace(',','.'))
 except InvalidOperation as exc: raise ValueError(f'Número inválido: {value!r}') from exc
 if not n.is_finite() or n<0: raise ValueError(f'Número negativo ou não finito: {value!r}')
 if integer and n!=n.to_integral_value(): raise ValueError(f'Inteiro inválido: {value!r}')
 return str(int(n)) if integer else format(n,'f')

def transform(row,mapping,source):
 result={}
 for key in FIELDS[source]:
  col=mapping.get(key)
  value=row.get(col,'') if col else ''
  value=(value or '').strip()
  if not value and key=='vagas': result[key]=''; continue
  if not value: raise ValueError(f'Valor obrigatório ausente: {key}')
  if key in NUMBERS or key.startswith('codigo_'):
   value=numeric(value,integer=True)
  elif key in RATES:
   value=numeric(value)
   if Decimal(value)>100: raise ValueError(f'Taxa fora de 0–100: {key}')
  result[key]=value
 if not 1900<=int(result['ano'])<=2200: raise ValueError('Ano fora do intervalo suportado.')
 if source=='trajetoria':
  if not 1900<=int(result['ano_ingresso'])<=int(result['ano']): raise ValueError('Coorte posterior ao ano de observação.')
  if int(result['ingressantes_coorte'])<=0: raise ValueError('Coorte sem ingressantes.')
  total=sum(Decimal(result[k]) for k in RATES)
  if abs(total-100)>Decimal('0.2'): raise ValueError('Taxas não somam 100% na tolerância de 0,2 p.p.')
 return result

def literal(value):
 if value=='': return 'NULL'
 return "'"+str(value).replace("'","''")+"'"

def sql_row(table,values,keys):
 columns=list(values)
 changes=','.join(f'{c}=EXCLUDED.{c}' for c in columns if c not in keys)
 return f"INSERT INTO inep.{table} ({','.join(columns)}) VALUES ({','.join(literal(values[c]) for c in columns)}) ON CONFLICT ({','.join(keys)}) DO UPDATE SET {changes};\n"

def normalize(args):
 spec=json.loads(Path(args.mapping).read_text(encoding='utf-8'))
 if spec.get('fonte')!=args.source or spec.get('revisado') is not True or not spec.get('dicionario_url'):
  raise ValueError('Confira o dicionário da edição, preencha dicionario_url e marque revisado=true no mapa.')
 mapping=spec['colunas']; required=set(FIELDS[args.source])-{'vagas'}
 if any(not mapping.get(k) for k in required): raise ValueError('Mapa incompleto: todos os campos obrigatórios precisam de coluna.')
 target=Path(args.output)
 if target.exists(): raise ValueError('Destino já existe. Use outra pasta para preservar a carga anterior.')
 target.parent.mkdir(parents=True,exist_ok=True)
 staging=Path(tempfile.mkdtemp(prefix='inep-',dir=target.parent))
 f=z=None
 try:
  sha=digest(args.input); f,z=open_csv(args.input,args.member,args.encoding)
  reader=csv.DictReader(f,delimiter=args.delimiter)
  if not reader.fieldnames or len(reader.fieldnames)!=len(set(reader.fieldnames)): raise ValueError('Cabeçalho ausente ou duplicado.')
  absent=[v for v in mapping.values() if v and v not in reader.fieldnames]
  if absent: raise ValueError('Colunas não encontradas: '+', '.join(absent))
  seen={}; ies={}; courses={}; processed=duplicates=0
  keys=['codigo_ies','codigo_curso','ano'] if args.source=='censo' else ['codigo_ies','codigo_curso','ano_ingresso','ano']
  csv_out=open(staging/'dados.csv','w',encoding='utf-8',newline='')
  sql_out=open(staging/'carga.sql','w',encoding='utf-8')
  try:
   writer=csv.DictWriter(csv_out,fieldnames=FIELDS[args.source]+['origem_sha256']); writer.writeheader()
   sql_out.write('-- Carga validada. Executar após sql/001_extensao_inep.sql.\nBEGIN;\n')
   for lineno,row in enumerate(reader,2):
    if not any(v for v in row.values()): continue
    if None in row: raise ValueError(f'Linha {lineno}: quantidade de colunas diferente do cabeçalho.')
    try: item=transform(row,mapping,args.source)
    except ValueError as exc: raise ValueError(f'Linha {lineno}: {exc}') from exc
    processed+=1; key=tuple(item[k] for k in keys)
    if key in seen:
     if item!=seen[key]: raise ValueError(f'Linha {lineno}: chave duplicada com valores divergentes {key}.')
     duplicates+=1; continue
    seen[key]=item
    code=item['codigo_ies']; course=(code,item['codigo_curso'])
    if code in ies and ies[code]!=item['nome_ies']: raise ValueError('Nomes de instituição conflitantes na mesma carga.')
    if course in courses and courses[course]!=item['nome_curso']: raise ValueError('Nomes de curso conflitantes na mesma carga.')
    if code not in ies:
     sql_out.write(sql_row('instituicao',{'codigo_ies':code,'nome_ies':item['nome_ies']},['codigo_ies']))
     ies[code]=item['nome_ies']
    if course not in courses:
     sql_out.write(sql_row('curso',{k:item[k] for k in ['codigo_ies','codigo_curso','nome_curso']},['codigo_ies','codigo_curso']))
     courses[course]=item['nome_curso']
    item=dict(item,origem_sha256=sha); writer.writerow(item)
    fact={k:v for k,v in item.items() if k not in {'nome_ies','nome_curso'}}
    table='censo_curso_ano' if args.source=='censo' else 'trajetoria_curso_coorte_ano'
    sql_out.write(sql_row(table,fact,keys))
   if not processed: raise ValueError('Fonte vazia: nenhuma linha de dados.')
   sql_out.write('COMMIT;\n')
  finally: csv_out.close(); sql_out.close()
  atomic_json(staging/'qualidade.json',{'status':'validado','fonte':args.source,'linhas_lidas':processed,
   'linhas_unicas':len(seen),'duplicatas_identicas':duplicates,'instituicoes':len(ies),'cursos':len(courses),
   'anos':sorted({int(k[-1]) for k in seen})})
  atomic_json(staging/'manifesto.json',{'fonte':args.source,'arquivo_entrada':str(Path(args.input).resolve()),
    'membro_zip':args.member,'sha256':sha,'gerado_em':timestamp(),'encoding':args.encoding,'delimiter':args.delimiter,
    'mapeamento':spec,'estado':'tratado; carga PostgreSQL ainda não executada'})
  os.replace(staging,target)
  print(target)
 except Exception:
  shutil.rmtree(staging,ignore_errors=True)
  raise
 finally:
  if f: f.close()
  if z: z.close()

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 sub=parser.add_subparsers(dest='command',required=True)
 p=sub.add_parser('fetch'); p.add_argument('--source',choices=FIELDS,required=True)
 p.add_argument('--config',default='config/fontes-inep.json'); p.add_argument('--output',default='data/raw')
 p.add_argument('--max-bytes',type=int,default=1_000_000_000); p.set_defaults(func=fetch)
 for cmd in ['inspect','normalize']:
  p=sub.add_parser(cmd); p.add_argument('--input',required=True); p.add_argument('--member')
  p.add_argument('--encoding',default='utf-8-sig'); p.add_argument('--delimiter',default=';')
  if cmd=='normalize':
   p.add_argument('--source',choices=FIELDS,required=True); p.add_argument('--mapping',required=True); p.add_argument('--output',required=True)
  p.set_defaults(func=inspect_file if cmd=='inspect' else normalize)
 p=sub.add_parser('template'); p.add_argument('--source',choices=FIELDS,required=True); p.add_argument('--output',required=True); p.set_defaults(func=template)
 args=parser.parse_args()
 try: args.func(args)
 except Exception as exc: print(f'ERRO: {exc}',file=sys.stderr); return 1
 return 0

if __name__=='__main__': sys.exit(main())
