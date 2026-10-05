# Trajetórias Acadêmicas UnB — Documentação

Documentação de engenharia de dados do projeto **Trajetórias Acadêmicas UnB**,
desenvolvido na disciplina Sistemas de Banco de Dados 2 (BD2) — FCTE/UnB, 2026.2.

O site é gerado com [MkDocs](https://www.mkdocs.org/) e o tema
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

**Endereço público previsto:** [Trajetórias Acadêmicas UnB](https://trajetorias-academicas-bd2-2026-2.github.io/documentation/).
O endereço passa a funcionar após a primeira publicação e a ativação do GitHub Pages.

## Rodar localmente

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
mkdocs serve
```

Abra <http://127.0.0.1:8000>. Veja mais detalhes em `docs/como-contribuir.md`.

## Conteúdo e origem

A documentação foi ampliada a partir de `referencias/projetoengenhariadedadosbd2-grupo-2.xlsx`.
Além dos cinco blocos de engenharia de dados e do ADR, inclui perguntas e indicadores,
arquitetura proposta, qualidade do pipeline e plano de validação. A rastreabilidade
entre abas e páginas está em `docs/referencia/planilha.md`.

As propostas complementares são identificadas no texto; medições e decisões pendentes
permanecem em aberto. A planilha original foi preservada.

Valide conteúdo, navegação e links antes de publicar:

```bash
mkdocs build --strict
```

## Publicação

A cada push na branch `main`, o workflow `.github/workflows/docs.yml`
publica o site no GitHub Pages (branch `gh-pages`).

Na primeira publicação:

1. Aguarde o workflow **Publicar documentação** concluir na aba **Actions**.
2. Em **Settings → Pages**, selecione **Deploy from a branch**.
3. Selecione a branch **gh-pages**, pasta **/(root)**, e salve.
4. Aguarde a publicação do Pages e abra o endereço público acima.

O MkDocs gera o site; o GitHub Pages o hospeda. O endereço `127.0.0.1:8000`
serve apenas para visualizar alterações no computador de quem executa `mkdocs serve`.
Pull requests também passam pela validação do site, sem publicação.

## Estrutura

```
.
├── mkdocs.yml
├── requirements.txt
├── .github/workflows/docs.yml
├── referencias/
│   ├── README.md
│   └── projetoengenhariadedadosbd2-grupo-2.xlsx
└── docs/
    ├── index.md
    ├── projeto/
    ├── dados/
    ├── pipeline/
    ├── decisoes/
    ├── referencia/
    ├── stylesheets/
    ├── pendencias.md
    ├── glossario.md
    └── como-contribuir.md
```

`docs/` contém as páginas publicadas. `referencias/` preserva o material de origem.
`site/` e `.venv/` são gerados localmente e não entram no Git; arquivos
`Zone.Identifier` também são ignorados.

## Versão 1.1 — Extensão Inep

F4 — Censo da Educação Superior e F5 — Indicadores de Trajetória foram
acrescentados ao inventário, modelo, pipeline, perguntas Q9–Q12 e planilha.
O pacote contém `scripts/inep_pipeline.py`, `config/fontes-inep.json`, DDL e
visões em `sql/` e testes em `tests/`. O tratamento usa a biblioteca padrão do Python.

```bash
python scripts/inep_pipeline.py --help
python -m unittest discover -s tests -v
```

Siga `docs/pipeline/execucao-inep.md` para baixar, mapear colunas, normalizar e
carregar no PostgreSQL. As páginas oficiais foram verificadas em 05/10/2026,
mas os ZIPs retornaram HTTP 502; não há carga oficial do Inep no pacote.
Os testes sintéticos não representam indicadores reais da UnB. A conexão ao
dashboard existente depende de seu código, ausente no ZIP recebido.
