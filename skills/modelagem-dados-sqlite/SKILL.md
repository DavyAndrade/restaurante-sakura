---
name: modelagem-dados-sqlite
description: >
  Use esta skill sempre que precisar MODELAR OS DADOS de um novo sistema
  com banco SQLite, seguindo o formato MRDS (Modelagem Relacional de Dados
  de Sistema). Ela captura o padrao de documentacao observado no sistema
  "controle_gastos/" (arquivo MRDS.md) e serve para projetar e documentar
  a estrutura do banco antes de implementar. Ideal para usar antes da skill
  "mvc-python-sqlite", que implementa o que foi modelado aqui.
---

# Modelagem Relacional de Dados para SQLite

## O que e e por que existe

Antes de escrever uma linha de codigo, e preciso ter um projeto de dados
claro: quais entidades existem, quais atributos cada uma tem, como se
relacionam, e quais regras de negocio incidem sobre elas. O arquivo
`MRDS.md` do sistema `controle_gastos/` estabeleceu um formato de
documentacao que cobre tudo isso. Esta skill generaliza aquele formato
para que qualquer novo sistema — como o SakuraRestaurant — possa ter
sua modelagem documentada de forma consistente.

## Formato do documento MRDS.md

Produza um unico arquivo `MRDS.md` na raiz do projeto com estas secoes:

### 1. Diagrama Entidade-Relacionamento (DER)

Use um diagrama em ASCII art mostrando todas as entidades, seus atributos
(com PK/FK marcados) e os relacionamentos com cardinalidade:

```
┌──────────────────┐
│    ENTIDADES     │
├──────────────────┤
│ PK id            │
│    atributo1     │
│ FK outra_id      │
│    atributo2     │
└────────┬─────────┘
         │
         │ 1
         │
         │ N
         │
┌────────┴─────────┐
│   OUTRA_TABELA   │
├──────────────────┤
│ PK id            │
│    ...
```

### 2. Descricao detalhada de cada entidade

Para cada entidade, documente:

```
### NOME_DA_TABELA
Descricao do que a entidade representa.

**Atributos:**
- `id` (INTEGER) - Chave Primaria, Auto Incremento
- `campo` (TIPO) - Descricao, restricoes (NOT NULL, UNIQUE, DEFAULT, etc.)

**Restricoes:**
- Lista de constraints que a tabela deve respeitar

**Relacionamentos:**
- N:1 com OUTRA_TABELA (descricao da cardinalidade)
- 1:N com OUTRA_TABELA (descricao da cardinalidade)
```

### 3. Mapa de Relacionamentos

Para cada par de entidades ligadas por FK, documente:

```
### ENTIDADE_A → ENTIDADE_B (1:N)
- Uma entidade A pode ter varias entidades B
- Cada entidade B pertence a uma unica entidade A
- Cardinalidade: (1,N) - (1,1)  [min,max de cada lado]
```

### 4. Regras de Negocio

Liste todas as regras que o sistema deve respeitar, agrupadas por entidade:

```
### Regras para ENTIDADE_X
1. Regra 1
2. Regra 2
```

Inclua regras de: unicidade, obrigatoriedade, integridade referencial,
restricoes de dominio (valores permitidos), cascata de exclusao.

### 5. Indices e Otimizacoes

Liste indices recomendados para as queries mais frequentes:

```sql
CREATE INDEX idx_tabela_campo ON tabela(campo);
```

Priorize indices para:
- Chaves estrangeiras (campos usados em JOIN)
- Campos usados em WHERE com frequencia
- Campos usados em ORDER BY

### 6. Integridade Referencial

Documente todas as FKs e a politica de cascata:

```
- TABELA_A.campo_fk → TABELA_B.id (ON DELETE CASCADE / ON UPDATE CASCADE)
```

### 7. Dicionario de Dados

Documente as convencoes de tipos e nomenclatura:

```
- INTEGER: numeros inteiros (IDs, flags booleanos 0/1)
- TEXT: strings de tamanho variavel
- REAL: numeros decimais (valores monetarios)
- Nomes de tabelas em plural e minusculas
- Chaves primarias sempre chamadas 'id'
- Chaves estrangeiras no formato 'tabela_id'
- Formato de data: ISO 8601 (YYYY-MM-DD)
- Valores booleanos: 0 (falso) e 1 (verdadeiro)
```

### 8. Queries Uteis (opcional, mas recomendado)

Inclua exemplos de consultas SQL que o sistema vai usar com frequencia,
como calculos de total, extratos por periodo, resumos agrupados.

## Tipos de dados SQLite usados no padrao

| Tipo SQLite | Uso |
|---|---|
| `INTEGER` | IDs, flags, contadores |
| `TEXT` | Nomes, descricoes, emails, datas (ISO) |
| `REAL` | Valores monetarios, percentuais |

## Checklist de modelagem

- [ ] DER em ASCII documentado
- [ ] Descricao textual de cada entidade (atributos + tipos + restricoes)
- [ ] Relacionamentos mapeados com cardinalidade
- [ ] Regras de negocio documentadas
- [ ] Convencao de nomenclatura definida e aplicada
- [ ] Indices recomendados (minimo: FKs)
- [ ] Integridade referencial (FKs com `ON DELETE` / `ON UPDATE`)
- [ ] Queries uteis exemplificadas

## Quando usar outras skills

- **mvc-python-sqlite** — depois de concluir a modelagem, para implementar
  o sistema seguindo o padrao MVC + SQLite.
- **mrds-modelagem** (skills/mrds-modelagem/) — se o projeto for da
  disciplina 4ADS e precisar tambem de diagramas UML (casos de uso,
  sequencia, estado, atividades).
