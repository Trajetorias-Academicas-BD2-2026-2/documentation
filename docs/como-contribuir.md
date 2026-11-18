# Como contribuir com a documentação

## 1. Rodar o site localmente

1. Clone o repositório:
    ```bash
    git clone https://github.com/Trajetorias-Academicas-BD2-2026-2/documentation.git
    cd documentation
    ```
2. Crie e ative um ambiente virtual:
    ```bash
    python -m venv .venv
    source .venv/bin/activate      # Windows: .venv\Scripts\activate
    ```
3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
4. Inicie o servidor de desenvolvimento:
    ```bash
    mkdocs serve
    ```
5. Abra <http://127.0.0.1:8000>. O site recarrega sozinho a cada arquivo salvo.

## 2. Editar ou criar páginas

1. Os arquivos ficam em `docs/`, em Markdown.
2. Para criar uma página nova, adicione o `.md` na pasta adequada.
3. Registre a página em `nav`, no `mkdocs.yml`, para que apareça no menu.
4. Use o botão de lápis no topo de cada página para editar direto no GitHub.

## 3. Validar antes do commit

```bash
mkdocs build --strict
```

O modo `--strict` transforma avisos (links quebrados, páginas fora do `nav`) em erros.

## 4. Manter o conteúdo consistente

- O repositório do código é a fonte: ADRs, evidências e números vêm de lá. Ao mudar um ADR no código, copie-o para `docs/decisoes/` (veja o [índice de ADRs](decisoes/index.md)).
- Número sem fonte não entra: aponte o script, a evidência em `docs/evidencias/` ou a consulta que o gerou.
- Atualize a página da entrega correspondente ([E1](entregas/e1.md), [E2](entregas/e2.md), [E3](entregas/e3.md)) quando uma evidência mudar.
- Confira páginas e diagramas no modo claro, no modo escuro e em uma janela estreita.

## 5. Publicar

1. Faça commit e push na branch `main`.
2. O workflow `.github/workflows/docs.yml` gera o site e publica na branch `gh-pages`.
3. Na **primeira vez**, ative o GitHub Pages: *Settings → Pages → Source: Deploy from a branch → `gh-pages` / `(root)`*.

## Recursos de escrita

=== "Aviso"

    ```markdown
    !!! warning "Título"
        Texto do aviso.
    ```

=== "Diagrama Mermaid"

    ````markdown
    ```mermaid
    flowchart LR
        A --> B
    ```
    ````

=== "Abas"

    ```markdown
    === "Aba 1"
        Conteúdo 1
    === "Aba 2"
        Conteúdo 2
    ```

=== "Lista de tarefas"

    ```markdown
    - [x] Feito
    - [ ] Pendente
    ```
