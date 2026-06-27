---
name: entrega-4ads
description: >
  Use esta skill quando Davy mencionar a disciplina "Tópicos em Análise e
  Desenvolvimento de Sistemas" (4ADS, FAETERJ, Prof. Alfredo Boente), ou as
  avaliações AV1, AV2, AVS/AVF dela, ou pedir para organizar/planejar a
  entrega completa de um sistema "MRDS/RAD com Python", ou montar o
  seminário de apresentação (slides + diagramas + link do sistema). Esta
  skill não modela nem programa por si só — ela organiza o trabalho e aciona
  "mrds-modelagem" (para a modelagem) e "rad-python" (para a implementação)
  na ordem certa, e mantém os critérios de avaliação do professor sempre
  visíveis.
---

# Entrega da disciplina — 4ADS (MRDS/RAD com Python)

## Por que esta skill existe

A apostila da disciplina define uma estrutura de avaliação fixa que se
repete em AV1 e AV2. Esta skill existe para que nenhuma parte do critério
seja esquecida e para guiar Davy (ou quem estiver com ele em dupla) pela
ordem correta de trabalho, delegando a parte técnica para as skills
especializadas.

## Critério de avaliação (memorize isto)

- **MD = (AV1 + AV2) / 2**
- Aprovado se **MD ≥ 6,0** *e* presença mínima de **75%**
- Cada avaliação (AV1, AV2, AVS/AVF) precisa de nota **≥ 3,0** para ser
  considerada validada — uma nota abaixo disso não conta, mesmo que a média
  geral dê 6,0.
- **AVS/AVF**: prova escrita, cobrindo o conteúdo de AV1 e AV2 juntos.

## O que cada AV exige (AV1 e AV2 têm exatamente a mesma estrutura)

Cada entrega — AV1 "Parte 1" e AV2 "Parte 2" do mesmo sistema, ou dois
sistemas diferentes, dependendo do que o professor definir no semestre —
precisa conter três blocos:

1. **Modelagem com MRDS** → acionar a skill `mrds-modelagem`
   - Modelo de Casos de Uso (lista, diagrama, descrição textual detalhada)
   - Matriz de Rastreabilidade de Requisitos
   - Modelo de Classes
   - Diagrama de Sequência
   - Diagrama de Estado
   - Diagrama de Atividades

2. **Sistema RAD** → acionar a skill `rad-python`
   - Linguagem Python
   - GUI Tkinter (ou framework correlato)
   - Banco de Dados SQLite3
   - CRUDs básicos: Inclusão, Consulta, Alteração, Remoção, Relatório de
     Informações

3. **Seminário de Sistemas** — apresentação em `.ppt`/`.pptx` (usar a skill
   `pptx` quando chegar a essa etapa) contendo no mínimo:
   - Diagrama de Casos de Uso
   - Diagrama de Classes
   - Link de acesso ao sistema (rodando/demonstrável)

## Ordem de trabalho recomendada

1. Confirmar a dupla de trabalho e o tema do sistema (complexidade média ou
   alta — evitar temas triviais).
2. Brainstorming/elicitação de requisitos (ver `mrds-modelagem`, seção 1).
3. Modelagem completa com `mrds-modelagem` (passos 2 a 7 daquela skill).
4. Implementação com `rad-python`, classe por classe, CRUD por CRUD, sempre
   voltando à Matriz de Rastreabilidade para confirmar que cada requisito
   foi de fato implementado.
5. Testar o sistema fim-a-fim contra os fluxos descritos nos Casos de Uso
   (inclusive os fluxos alternativos).
6. Montar os slides do seminário (skill `pptx`), reaproveitando os diagramas
   já produzidos no passo 3.
7. Revisar contra o checklist abaixo antes de considerar a entrega concluída.

## Checklist final de entrega

- [ ] Lista de Casos de Uso
- [ ] Diagrama de Casos de Uso
- [ ] Descrição textual detalhada de cada Caso de Uso
- [ ] Matriz de Rastreabilidade de Requisitos (preenchida, não só o template)
- [ ] Diagrama de Classes
- [ ] Diagrama de Sequência
- [ ] Diagrama de Estado
- [ ] Diagrama de Atividades
- [ ] Sistema Python rodando, com Tkinter + SQLite3
- [ ] CRUD de Inclusão funcionando
- [ ] CRUD de Consulta funcionando
- [ ] CRUD de Alteração funcionando
- [ ] CRUD de Remoção funcionando
- [ ] Relatório de Informações (não confundir com a Consulta simples)
- [ ] Slides do seminário com Casos de Uso + Classes + link do sistema

## Notas

- Se a tarefa em mãos for puramente sobre modelagem ou puramente sobre
  código, é mais direto acionar `mrds-modelagem` ou `rad-python` diretamente
  — esta skill é o "mapa" que aparece quando o pedido é sobre a entrega como
  um todo, sobre prazos/critérios, ou sobre montar o seminário.
- Se surgir um AVS/AVF, lembre que é prova escrita cobrindo todo o conteúdo
  teórico de AV1+AV2 (metodologia MRDS/RAD, fundamentos de Python, SQLite3,
  Tkinter) — não é entrega de sistema, é avaliação de conteúdo.