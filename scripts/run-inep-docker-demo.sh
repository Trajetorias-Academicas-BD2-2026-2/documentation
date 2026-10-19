#!/usr/bin/env bash
set -euo pipefail

root=/workspace
out="$root/data/staging/docker-demo"
rm -rf "$out"
mkdir -p "$out"

python "$root/scripts/inep_pipeline.py" normalize \
  --source censo \
  --input "$root/fixtures/inep/censo.csv" \
  --mapping "$root/fixtures/inep/mapa-censo.json" \
  --output "$out/censo"

python "$root/scripts/inep_pipeline.py" normalize \
  --source trajetoria \
  --input "$root/fixtures/inep/trajetoria.csv" \
  --mapping "$root/fixtures/inep/mapa-trajetoria.json" \
  --output "$out/trajetoria"

psql -v ON_ERROR_STOP=1 -h "$PGHOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" \
  -f "$root/sql/001_extensao_inep.sql"
psql -v ON_ERROR_STOP=1 -h "$PGHOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" \
  -f "$out/censo/carga.sql"
psql -v ON_ERROR_STOP=1 -h "$PGHOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" \
  -f "$out/trajetoria/carga.sql"
psql -v ON_ERROR_STOP=1 -h "$PGHOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" \
  -f "$root/sql/002_indicadores_inep.sql"

psql -v ON_ERROR_STOP=1 -h "$PGHOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" \
  -c "SELECT 'censo' AS fonte, count(*) AS linhas FROM inep.censo_curso_ano UNION ALL SELECT 'trajetoria', count(*) FROM inep.trajetoria_curso_coorte_ano;"

echo "Demonstração Docker da extensão Inep concluída com fixtures sintéticas."
