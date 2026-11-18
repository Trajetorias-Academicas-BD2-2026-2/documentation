# Observatório de reservas da FCTE · Documentação

Site de documentação do projeto da **Squad G2** em Sistemas de Banco de Dados 2 (FCTE/UnB, 2026.2).

> Como evoluíram, entre 2022.1 e 2026.1, as vagas reservadas publicadas para cada curso da FCTE nas disciplinas obrigatórias do currículo de referência selecionado para 2026.1?

- **Site:** <https://trajetorias-academicas-bd2-2026-2.github.io/documentation/>
- **Código, dados e evidências:** <https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas>

O site descreve o que foi implementado nas entregas E1 (fonte transacional), E2 (ingestão em lote e CDC) e E3 (camada analítica e painel). Também traz os ADRs, que são cópias dos do repositório do código. Os números citados vêm do banco carregado e das evidências em `docs/evidencias/` do repositório do código.

## Rodar localmente

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
mkdocs serve                     # http://127.0.0.1:8000
mkdocs build --strict            # valida links e navegação antes de publicar
```

## Publicação

A cada push na `main`, o workflow `.github/workflows/docs.yml` valida o site com `mkdocs build --strict` e publica no GitHub Pages (branch `gh-pages`). Pull requests só passam pela validação.

## Estrutura

```
docs/
├── index.md
├── projeto/      visão geral e arquitetura
├── entregas/     E1, E2, E3: checklist, evidência e comando
├── dados/        fonte e coleta, modelo OLTP, carga de trabalho, camada analítica
├── pipeline/     ingestão, orquestração, qualidade, desempenho
├── consumo/      painel e governança
├── decisoes/     ADR-0001 a ADR-0006
├── referencia/   diário de bordo
├── assets/       imagens
├── glossario.md, como-contribuir.md, apresentacao.md
referencias/      planilha original do planejamento (material da disciplina)
```
