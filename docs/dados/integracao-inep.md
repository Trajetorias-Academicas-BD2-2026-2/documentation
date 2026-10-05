# Integração com o Inep

## Objetivo da ampliação

A versão 1.1 incorpora **F4 — Censo da Educação Superior** e **F5 — Indicadores de Trajetória**.
O novo recorte compara cursos da UnB com cursos equivalentes de outras instituições.
O Inep consolida registros fornecidos pelas instituições. F5 deriva do Censo;
as duas publicações não são observações estatisticamente independentes.

As páginas e os links oficiais foram consultados em **05/10/2026**. Os ZIPs de
2024 e 2015–2024 retornaram HTTP 502 no ambiente desta revisão. Portanto, há
implementação de coleta/tratamento e testes com dados sintéticos, mas **nenhuma
carga oficial nem resultado numérico real do Inep foi produzido nesta entrega**.

## Recursos selecionados

| Fonte | Edição inicial | Página | Recurso publicado |
|---|---|---|---|
| F4 | 2024 | [Censo](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-da-educacao-superior) | [ZIP 2024](https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_2024.zip) |
| F5 | Coorte 2015 acompanhada até 2024 | [2015–2024](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/indicadores-de-trajetoria-da-educacao-superior/2015-2023) | [ZIP 2015–2024](https://download.inep.gov.br/informacoes_estatisticas/indicadores_educacionais/indicadores_trajetoria_es_2015_2024.zip) |

O endereço da página de F5 termina em `2015-2023`, mas o título publicado é
2015–2024. Isso foi preservado em `config/fontes-inep.json`.
O recorte de 2020–2024 para F4 é uma expansão de coleta prevista, não uma série já carregada.

## Granularidade e correspondência

| Conjunto | Uma linha representa | Chave lógica |
|---|---|---|
| Censo | Curso de uma instituição em um ano | instituição + curso + ano |
| Trajetória | Curso, coorte de ingresso e ano de observação | instituição + curso + coorte + ano |
| Mapa de cursos | Correspondência revisada do curso local em um ano | curso local + ano |

Mapear o código local ao código do curso no Inep/e-MEC com evidência documental.
Conferir nome, campus/local de oferta, grau acadêmico e modalidade. Um nome igual
não prova equivalência. Cursos sem mapa ficam explicitamente sem correspondência.
Se um curso local tiver mais de uma correspondência válida no mesmo ano, revisar
o modelo antes de carregar; o mapa atual exige correspondência única por ano.

Os metadados usados para formar grupos de comparação ficam nas tabelas anuais,
preservando mudanças de classificação entre anos. Os nomes nas dimensões são os
últimos aplicados. Não juntar registros de aluno ou turmas ao Inep por nome.

## Regras para comparações

- Mesma área/classificação CINE no nível selecionado, grau, modalidade e categoria administrativa.
- Para trajetórias: mesma coorte, ano de observação e duração do acompanhamento.
- Excluir todos os cursos da instituição-alvo da referência.
- Ponderar taxas pelo número de ingressantes da coorte. Exibir também cursos,
  instituições e ingressantes usados na referência.
- Grupo vazio gera taxa de referência indisponível, nunca zero.
- Desistência do curso de ingresso pode incluir transferência. Permanência pode
  incluir trancamento. Usar as definições do dicionário da edição.
- Não somar estoques de matrículas entre anos nem somar taxas.
- `concluintes / ingressantes` do mesmo ano é uma razão entre fluxos, não taxa
  de conclusão de uma coorte. Essa razão não é implementada como conclusão.
- Dados anuais de curso não representam ocupação nem demanda de disciplinas.
- Diferenças observadas são descritivas, sem atribuir causalidade a cotas,
  vagas, formas de ingresso ou características institucionais.

## Contrato canônico de dados

O comando `template` gera um mapa vazio de nomes canônicos para colunas originais.
Não há inferência silenciosa de colunas. Cada mapa precisa de `fonte`,
`dicionario_url`, `revisado: true` e `colunas` preenchidas após leitura do dicionário.
O dicionário usado deve ser da mesma edição do ZIP.

| Campos canônicos | Tipo e regra |
|---|---|
| codigo_ies, codigo_curso | Identificadores numéricos convertidos a texto canônico; obrigatórios |
| nome_ies, nome_curso | Texto obrigatório; não são chave |
| ano | Inteiro entre 1900 e 2200 |
| area, grau, modalidade, categoria | Códigos de classificação da fonte; obrigatórios; preservar o mesmo nível de área entre cargas |
| matriculas, ingressantes, concluintes | Inteiros não negativos em F4 |
| vagas | Inteiro não negativo ou ausente em F4; não inferir a partir de matrículas |
| ano_ingresso | Inteiro entre 1900 e o ano observado em F5 |
| ingressantes_coorte | Denominador positivo da coorte em F5 |
| taxa_permanencia, taxa_conclusao, taxa_desistencia | Percentuais de 0 a 100, total de 100 com tolerância de 0,2 ponto percentual |
| origem_sha256 | Hash do CSV ou ZIP utilizado; incluído pelo tratamento |

Ausência de taxa ou denominador em uma edição bloqueia F5. Não reconstruir uma
coorte a partir de totais anuais de F4. Se o arquivo trouxer taxas de 0 a 1,
convertê-las explicitamente para 0–100 em uma transformação documentada antes
da normalização. A rotina não faz essa conversão automaticamente.

## Modelo físico incluído

`sql/001_extensao_inep.sql` cria seis tabelas no schema `inep`, sem modificar as
tabelas locais existentes: `instituicao`, `curso`, `curso_local`, `mapa_curso`,
`censo_curso_ano` e `trajetoria_curso_coorte_ano`.
`sql/002_indicadores_inep.sql` cria as visões de evolução, comparação e vínculo local.
`v_comparacao_censo` compara contagens anuais à média por curso do grupo equivalente,
mostrando o tamanho da referência. Essa média descreve a dimensão dos cursos;
não é taxa de conclusão nem indicador de qualidade. `v_comparacao_trajetoria`
calcula taxas ponderadas e diferenças em pontos percentuais.
O mapeamento local é revisado e carregado pela equipe, não gerado automaticamente.

## Fontes conceituais

- [Apresentação do Censo](https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/censo-da-educacao-superior).
- [Metodologia de trajetória](https://download.inep.gov.br/informacoes_estatisticas/indicadores_educacionais/2017/metodologia_indicadores_trajetoria_curso.pdf).
- [Perfil dos Estudantes da UnB](https://dpo.unb.br/avaliacao/perfil-do-estudantes/) e
  [Anuário 2025](https://repositoriodpo.unb.br/anuarios/anuario-estatistico-2025/)
  ficam como referências auxiliares para conferência. Não foram contabilizados
  como fontes já integradas, pois podem se sobrepor aos dados locais e ao Censo.
