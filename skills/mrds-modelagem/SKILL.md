---
name: mrds-modelagem
description: >
  Use esta skill sempre que Davy estiver na fase de MODELAGEM de um sistema
  para a disciplina "Tópicos em Análise e Desenvolvimento de Sistemas" (4ADS,
  FAETERJ, Prof. Alfredo Boente) ou qualquer projeto que siga a MRDS —
  Metodologia Rápida de Desenvolvimento de Software. Acione esta skill quando
  o pedido envolver: brainstorming/elicitação de requisitos, Modelo/Diagrama
  de Casos de Uso, descrição textual de caso de uso, Matriz de Rastreabilidade
  de Requisitos, Diagrama de Classes, Diagrama de Sequência, Diagrama de
  Estado, Diagrama de Atividades, ou preparação da modelagem que antecede a
  implementação RAD em Python (ver skill "rad-python"). Não usar para escrever
  o código Python do sistema — isso é responsabilidade da skill "rad-python".
---

# MRDS — Metodologia Rápida de Desenvolvimento de Software

## O que é e por que existe

A MRDS sugere o uso de um **subconjunto da UML** — não a UML completa — para
modelar um sistema antes de implementá-lo como RAD (Rapid Application
Development). Foi proposta por Silveira e Schmitz (1999) e deu origem à
ferramenta **FastCase** (dissertação de Denis da Silva Silveira, UFRJ): um
desenhador de diagramas acoplado a um gerador de código que segue uma
arquitetura padrão. A lição prática que isso ensina é: **modele só o
suficiente para gerar/guiar a implementação, sem inflar o trabalho com
artefatos UML que a MRDS não pede.**

O subconjunto de diagramas da MRDS é fixo e é exatamente o que a disciplina
avalia em AV1 e AV2:

1. Modelo de Casos de Uso (lista + diagrama + descrição textual detalhada)
2. Matriz de Rastreabilidade de Requisitos
3. Modelo/Diagrama de Classes
4. Diagrama de Sequência
5. Diagrama de Estado
6. Diagrama de Atividades

Não adicione outros diagramas UML (componentes, implantação, pacotes etc.) a
menos que Davy peça explicitamente — eles não fazem parte do escopo da MRDS
nesta disciplina e podem até ser cobrados como erro em uma banca que segue o
material do professor à risca.

## Fluxo de trabalho (siga nesta ordem)

### 1. Elicitação de requisitos / Brainstorming

Antes de qualquer diagrama, é preciso:
- Escolher o tema do sistema (complexidade média ou alta — sistemas triviais
  de 1-2 entidades não atendem ao critério da disciplina).
- Fazer brainstorming livre: nesta fase **toda ideia tem validade**, mesmo as
  que depois serão descartadas — elas ajudam a delimitar o que entra e o que
  não entra no escopo.
- Consolidar o brainstorming em uma lista de **requisitos funcionais** (o que
  o sistema faz) e **requisitos não-funcionais** (restrições: desempenho,
  usabilidade, plataforma etc.).
- Ferramenta sugerida pelo professor: Miro (miro.com/app/dashboard) para
  registrar o brainstorming, mas papel/lista em markdown funciona igual bem
  se Davy preferir manter tudo versionado em texto.

### 2. Modelo de Casos de Uso

Produza três artefatos, sempre os três juntos:

- **Lista de casos de uso** — nome de cada caso de uso, ligado a um ou mais
  requisitos funcionais.
- **Diagrama de Casos de Uso** — atores fora do sistema, elipses para cada
  caso de uso, dentro de uma fronteira de sistema; use as relações padrão
  (`<<include>>`, `<<extend>>`, generalização de ator) só quando fizerem
  sentido — não force relações que não existem no domínio.
- **Descrição textual detalhada** de cada caso de uso. Use sempre este
  template (é o que costuma ser cobrado em prova/ENADE sobre o assunto):

```
Caso de Uso: <Nome>
Ator(es): <quem dispara o caso de uso>
Pré-condições: <o que precisa ser verdade antes de iniciar>
Fluxo Principal:
  1. ...
  2. ...
Fluxos Alternativos:
  3a. <condição> -> <passos alternativos>
Pós-condições: <estado do sistema ao final>
```

### 3. Matriz de Rastreabilidade de Requisitos

Rastreia cada requisito (funcional e não-funcional) até o(s) caso(s) de uso
que o atende(m) — e, se quiser ir além do mínimo pedido, até a classe e o
método que efetivamente o implementam. Monte como tabela:

| Requisito | Descrição | Caso(s) de Uso | Classe/Método (RAD) |
|---|---|---|---|
| RF01 | ... | UC01, UC03 | `Cliente.cadastrar()` |
| RNF01 | ... | UC02 | — |

Esta matriz é o elo formal entre a modelagem (esta skill) e a implementação
(skill "rad-python") — depois que o sistema RAD estiver pronto, volte aqui e
preencha a última coluna.

### 4. Diagrama de Classes

Extraia as classes candidatas direto dos substantivos do domínio descritos
nos casos de uso. Para cada classe: nome, atributos (com tipo), métodos
públicos relevantes (tipicamente os CRUDs que a skill "rad-python" vai
implementar: incluir, consultar, alterar, remover, listar/relatório).
Represente associações, multiplicidade, agregação/composição e herança com a
notação UML padrão.

### 5. Diagrama de Sequência

Modele pelo menos os fluxos principais dos casos de uso mais relevantes
(tipicamente: cadastro e consulta/relatório). Mostre a troca de mensagens
entre os objetos de interface (tela), de controle/CRUD e o objeto que
representa o banco de dados.

### 6. Diagrama de Estado

Use para qualquer classe cujas instâncias tenham um **ciclo de vida** com
estados e transições relevantes para o negócio (ex.: Pedido: Aberto → Em
Andamento → Concluído/Cancelado). Se nenhuma entidade do domínio tiver
estados de negócio relevantes, é aceitável modelar o estado de um objeto
simples (ex.: registro Ativo/Inativo) — mas não pule o diagrama, ele é
obrigatório na avaliação.

### 7. Diagrama de Atividades

Modele o(s) processo(s) de negócio de ponta a ponta (não apenas um caso de
uso isolado), incluindo decisões, paralelismo (se houver) e os atores
envolvidos em cada raia (swimlane), quando relevante.

## Formato de entrega

- Texto em português, alinhado ao vocabulário do material do professor
  (use os termos exatos: "Modelo de Casos de Uso", "Matriz de Rastreabilidade
  de Requisitos" etc. — não troque por sinônimos em inglês na entrega).
- Diagramas podem ser produzidos como SVG (Davy já tem esse fluxo rodando em
  outros projetos acadêmicos) ou diretamente nos slides do seminário.
- O seminário final exige, no mínimo: Diagrama de Casos de Uso + Diagrama de
  Classes + link de acesso ao sistema funcionando — monte os slides com a
  skill `pptx` quando chegar essa etapa.

## Quando parar e chamar a outra skill

No momento em que a Matriz de Rastreabilidade e os diagramas de Classes
estiverem estáveis, passe para a skill **rad-python**: ela assume a partir
daqui para gerar a aplicação Python (Tkinter + SQLite3 + CRUDs) que
implementa exatamente as classes e casos de uso modelados aqui. Não comece a
escrever código Python dentro desta skill.