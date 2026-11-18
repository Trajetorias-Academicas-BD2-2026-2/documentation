# Painel

O serviço `dashboard` publica o observatório em `http://localhost:8080`. O painel conta a resposta à pergunta da E1 como uma **história em sete cenas**, que se revelam com a rolagem. O texto é para qualquer pessoa, sem termo técnico.

![Painel do observatório, todas as cenas](../assets/painel.png)

## Linguagem

A metáfora central é a **cadeira de sala de aula**. Uma vaga reservada vira "um lugar que a turma guarda para alunos de um curso". Cada cadeira desenhada vale 20 lugares. A ressalva de honestidade aparece logo na primeira cena: *guardado não é ocupado*.

| No banco | No painel |
|---|---|
| vagas reservadas nas obrigatórias | lugares guardados nas matérias obrigatórias |
| turmas com reserva | turmas que guardaram lugar |
| obrigatórias sem reserva | matérias obrigatórias que nunca guardaram lugar para o curso |
| 2023.2 | 2º semestre de 2023 (texto) ou 2023/2 (eixo) |
| freshness dentro do SLA | "Atualizado em 17 de novembro de 2026, às 22:09" |

## As cenas

| Cena | O que mostra | Dado |
|---|---|---|
| Abertura | A pergunta, o prédio da faculdade desenhado em traço e uma cadeira para cada curso | — |
| 1 · O que é um lugar guardado | Uma turma de exemplo com 60 cadeiras: guardadas para Software, para Energia e livres | ilustrativo |
| 2 · Ponto de partida | Cinco salas com as cadeiras de 2022/1 caindo e contadores que sobem | `mart_observatorio` |
| 3 · Quatro anos depois | As mesmas salas em 2026/1: Software 7× maior, os outros quatro cursos menores, com selos de variação | `mart_observatorio` |
| 4 · Semestre a semestre | Linha do tempo por curso, com um ponto que percorre os nove semestres e o aviso da mudança de registro em 2023/2 | `mart_observatorio` |
| 5 · Quem guarda os lugares | Quanto de cada curso vem da FCTE, da Matemática e da Física | `mart_disciplina_semestre` |
| 6 · O que ficou de fora | Cada matéria obrigatória como um retângulo: colorido se guardou lugar alguma vez, cinza se nunca (169 de 254) | `mart_cobertura_curriculo` |
| 7 · Explore o seu curso | Três números do curso, as matérias que mais ganharam e perderam lugares, e as turmas com 50 lugares ou mais para conferir | marts + `operations.alertas_reserva` |
| Rodapé | De onde vêm os números, o que eles não dizem e quando foram atualizados | `metricas_freshness` |

## Uso

- **Curso inicial:** `?curso=FGA_ELET` abre direto num curso, e o painel lembra o último curso escolhido.
- **Modo estático:** `?modo=estatico` mostra todas as cenas no estado final, sem animação. Serve para imprimir ou gerar evidência; a imagem acima foi feita assim.
- **Acessibilidade:**
  - funciona por teclado;
  - respeita "reduzir movimento" do sistema;
  - cada ilustração tem descrição em texto com o número que mostra;
  - se adapta a partir de 360 px de largura.

## Implementação

- [`dashboard/app.py`](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/blob/main/dashboard/app.py) serve a página e `GET /api/observatorio`, um JSON com os dados das cenas. Ele lê só a camada de consumo.
- [`dashboard/static/index.html`](https://github.com/Trajetorias-Academicas-BD2-2026-2/Trajetorias-academicas/blob/main/dashboard/static/index.html) tem as ilustrações em SVG próprio, e as animações usam só CSS e JavaScript do navegador, sem biblioteca.
- Se o banco ou a camada analítica não estiverem prontos, a API responde 503 e a página explica como iniciar o sistema.
