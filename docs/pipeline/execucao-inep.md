# Executar a extensão Inep

Executar a partir da raiz do repositório com **Python 3.10 ou posterior**.
Coleta, inspeção, normalização e geração de SQL não exigem pacotes Python externos.
PostgreSQL e `psql` são necessários para aplicar a carga. Não publicar indicadores
antes de conferir os dados reais e o mapa dos cursos.

## 1. Coletar os recursos oficiais

```bash
python scripts/inep_pipeline.py fetch --source censo
python scripts/inep_pipeline.py fetch --source trajetoria
```

O comando imprime o caminho do ZIP. Cada download é preservado em
`data/raw/F4/EDICAO/SHA256/` ou `data/raw/F5/EDICAO/SHA256/`, com manifesto.
Arquivo vazio, HTML no lugar de ZIP, erro HTTP ou integridade inválida interrompem
a coleta e geram `ultima_falha.json`. Não há repetição infinita de download.
Se o servidor continuar indisponível, baixe manualmente pelo link oficial e
utilize o ZIP como `--input`. O tratamento registrará seu hash e caminho.

## 2. Identificar o CSV e conferir o dicionário

```bash
python scripts/inep_pipeline.py inspect --input CAMINHO_DO_ZIP
python scripts/inep_pipeline.py inspect --input CAMINHO_DO_ZIP --member CAMINHO_INTERNO_DO_CSV --encoding cp1252
python scripts/inep_pipeline.py template --source censo --output config/mapa-censo.json
python scripts/inep_pipeline.py template --source trajetoria --output config/mapa-trajetoria.json
```

`--encoding cp1252` é um exemplo: selecione a codificação real após conferência.
O padrão é `utf-8-sig`, com delimitador `;`; `--delimiter` permite alterá-lo.
Preencha as colunas e a URL do dicionário nos mapas e só então marque
`revisado` como `true`. Nomes originais, unidade das taxas e denominadores devem
ser conferidos no arquivo, não presumidos a partir de outra edição.

## 3. Tratar sem publicar carga parcial

```bash
python scripts/inep_pipeline.py normalize --source censo --input CAMINHO_DO_ZIP --member CAMINHO_INTERNO_DO_CSV --mapping config/mapa-censo.json --encoding cp1252 --output data/staging/censo-2024-v1
python scripts/inep_pipeline.py normalize --source trajetoria --input CAMINHO_DO_ZIP --member CAMINHO_INTERNO_DO_CSV --mapping config/mapa-trajetoria.json --encoding cp1252 --output data/staging/trajetoria-2015-2024-v1
```

Cada pasta recebe `dados.csv`, `carga.sql`, `qualidade.json` e `manifesto.json`.
Só aparece ao final de uma execução válida. Destino existente não é sobrescrito.
Duplicatas inteiramente iguais são removidas e contadas; a mesma chave com valores
divergentes bloqueia a carga. Nulos obrigatórios, valores negativos, datas
incompatíveis, cabeçalhos duplicados e taxas inválidas também bloqueiam a carga.

Para Parquet, exporte **o CSV normalizado**, preservando os nomes e tipos do
contrato. As dependências opcionais estão em `requirements-data.txt`. A exportação
Parquet ainda não é executada pelo comando acima; CSV e SQL são os produtos desta versão.

## 4. Aplicar no PostgreSQL

Defina `PGHOST`, `PGPORT`, `PGDATABASE` e `PGUSER` no seu ambiente e utilize
solicitação de senha ou `.pgpass` local. Não coloque credenciais no projeto.

```bash
psql -v ON_ERROR_STOP=1 -f sql/001_extensao_inep.sql
psql -v ON_ERROR_STOP=1 -f data/staging/censo-2024-v1/carga.sql
psql -v ON_ERROR_STOP=1 -f data/staging/trajetoria-2015-2024-v1/carga.sql
psql -v ON_ERROR_STOP=1 -f sql/002_indicadores_inep.sql
```

Cada `carga.sql` usa uma transação e `ON CONFLICT DO UPDATE`: reaplicar a mesma
carga não multiplica linhas. A importação atualiza apenas as chaves presentes
no arquivo. **Ela não remove registros que desapareceram em uma revisão.**
Antes de aplicar uma edição corrigida com remoções, conferir o escopo e planejar
a substituição transacional do recorte; não misturar edições silenciosamente.

## 5. Revisar a correspondência local e publicar

Cadastrar `curso_local` e `mapa_curso` com identificadores reais e evidência
da equivalência. Conferir os totais do Censo e as coortes da trajetória,
inclusive a quantidade de cursos sem mapa e sem grupo de referência.
Só depois expor as visões no dashboard existente da equipe.
Esta extensão entrega consultas e documentação de apresentação; o ZIP original
não contém código do dashboard para conectar essas visões diretamente.

## 6. Verificar a implementação

```bash
python -m unittest discover -s tests -v
mkdocs build --strict
```

Os testes usam dados sintéticos apenas em memória/pastas temporárias. Verificam
validação, rejeição de conflitos, reaplicação e ponderação. O SQL é exercitado com
SQLite em modo de compatibilidade para tabelas/visões; isso não substitui o teste
da carga e das visões no PostgreSQL real da equipe.
