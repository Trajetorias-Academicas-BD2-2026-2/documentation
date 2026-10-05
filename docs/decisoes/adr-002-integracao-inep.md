# ADR-002 — Integrar agregados do Inep por curso, ano e coorte

**Data:** 05/10/2026. **Status:** extensão implementada no pacote; carga real e
validação pela equipe pendentes. **Motivação:** acrescentar contexto nacional às
trajetórias da UnB e ampliar o trabalho de integração.

## Decisão

Selecionar F4 (Censo, edição inicial 2024) e F5 (trajetória 2015–2024), preservando
originais e manifestos. Integrar por códigos de instituição/curso e um mapa local
revisado por ano. Separar fatos anuais e de coorte das turmas semestrais.
Comparar grupos da mesma área, grau, modalidade, categoria, coorte e janela;
ponderar taxas pelos ingressantes e excluir a instituição-alvo da referência.

## Alternativas e critério

Relatórios de Perfil e Anuário da UnB ajudam na conferência, mas podem reproduzir
os registros locais e o próprio Censo. Indicadores CPC/Enade acrescentam qualidade,
mas exigem outro alinhamento de ciclos e não entram nesta extensão. O recorte
Inep foi escolhido por acrescentar comparação entre instituições com chaves
institucionais e cobertura anual, mantendo o domínio acadêmico do projeto.

## Consequências e evidências

Novas perguntas Q9–Q12, seis tabelas, duas coletas e consultas de referência.
A equipe precisa revisar correspondências, dicionários e comparabilidade dos grupos.
F5 deriva de F4; não são fontes estatisticamente independentes. Vagas de curso
não medem vagas de disciplinas e desistência de curso não equivale a abandono do sistema.

Páginas oficiais e links foram verificados. Os downloads retornaram HTTP 502.
Testes sintéticos verificam regras de tratamento e consulta, sem alegar resultados reais.
Revisitar a decisão se o dicionário impedir os indicadores, o mapa for ambíguo,
os grupos comparáveis forem vazios ou as edições revisadas alterarem os conceitos.
