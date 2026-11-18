# Visão geral

## Domínio e persona

O coordenador de um curso de graduação da FCTE (Campus Gama) negocia, a cada semestre, quantas vagas cada turma reserva para o seu curso. Isso vale para as turmas da própria FCTE e para as de outros institutos, como Cálculo (Matemática) e Física. Hoje ele faz isso sem ver como essas reservas evoluíram.

## Pergunta de gestão

> Como evoluíram, entre 2022.1 e 2026.1, as vagas reservadas publicadas para cada curso da FCTE nas disciplinas obrigatórias do currículo de referência selecionado para 2026.1?

- **Vagas reservadas:** campo "Vgs Reservadas" da página pública de turmas de cada curso no SIGAA.
- **Currículo de referência:** a versão curricular em vigor em 2026.1. É um conjunto **fixo**, aplicado a toda a série. A pergunta é sobre as disciplinas que hoje são obrigatórias, não sobre o que era obrigatório em cada semestre.
- **Recorte:** os 5 cursos de engenharia da FCTE e 9 semestres encerrados, de 2022.1 a 2026.1.

Perguntas derivadas, com consultas no repositório ([`db/consultas/`](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/tree/main/db/consultas)):

- Quais obrigatórias nunca tiveram reserva para o curso no recorte?
- Quanto das reservas vem de disciplinas da FCTE e quanto de outras unidades?
- Quantas turmas atendem mais de um curso?
- Quais obrigatórias mais ganharam ou perderam reserva entre 2022 e 2025?

## Por que a pergunta mudou

A primeira pergunta do projeto era sobre **lotação** das turmas. Na coleta de 28/09/2026 não conseguimos a série de vagas ocupadas nas fontes públicas testadas:

- a consulta geral de turmas não devolveu o histórico da FCTE;
- a página do curso só traz as vagas reservadas;
- o conjunto "Turmas" do portal de dados abertos é um retrato de 2022.

A troca está registrada no [ADR-0003](../decisoes/0003-reservas-por-curso-e-curriculo-versionado.md).

## O que os dados mostram

- **Recorte:** 1.776 reservas de 733 turmas.
- **Turmas compartilhadas:** 38% das turmas reservam vagas para mais de um curso (média de 2,42 cursos por turma).
- **Cobertura:** só 85 dos 254 pares curso × obrigatória tiveram alguma reserva no recorte.
- **Software × demais cursos:** Software multiplicou por 7 as reservas nas obrigatórias. Os outros quatro cursos caíram entre 29% e 74%.

## O que os dados não respondem

- Se uma turma lotou ou faltou vaga: as fontes públicas consultadas não trazem ocupação.
- Qual foi a oferta total de turmas: só aparecem turmas que reservam vagas para algum dos cinco cursos.
- Como a reserva mudou durante o semestre: só entra o retrato de semestres encerrados.
- O que era obrigatório em cada semestre passado: as versões curriculares de 2022 a 2024 não foram coletadas para 4 dos 5 cursos.
- A partir de 2023.2, as reservas de 50 vagas ou mais saltam de 4 para 17 a 41 por semestre, sobretudo em Software. Isso parece mudança na forma de registrar a reserva e pede cautela ao comparar com 2022.
- Pré-requisitos foram coletados para 23 dos 585 componentes da FCTE.

## Equipe

Ana Joyce · Gustavo Alves · Gabriel Lima da Silva · Nathan Abreu · Guilherme Evangelista · Angélica Campos · Davi Araújo
