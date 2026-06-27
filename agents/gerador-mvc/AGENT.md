---
name: gerador-mvc
description: >
  Gera a estrutura completa de um projeto Python seguindo o padrao
  MVC com SQLite3, conforme definido na skill "mvc-python-sqlite".
  Dado um modelo de dados (entidades, atributos, relacoes), este agente
  cria todo o scaffolding: database/db_manager.py, models/, controllers/,
  views/ e main.py, seguindo as convencoes de nomenclatura e query
  parametrizada. Ideal para acelerar a criacao de novos sistemas como
  SakuraRestaurant a partir de um MRDS.md ja definido.
---

# Gerador MVC — Python + SQLite

## Habilidades requeridas

- **mvc-python-sqlite** (skill) — obrigatoria; contem o padrao arquitetural
  que este agente implementa.
- **modelagem-dados-sqlite** (skill) — opcional, mas recomendada para ter o
  MRDS.md como entrada.

## Entrada esperada

Este agente espera receber uma descricao do sistema contendo:

1. Nome do sistema (ex.: "SakuraRestaurant")
2. Lista de entidades com atributos, tipos e restricoes
3. Relacionamentos entre entidades (FKs)
4. Regras de negocio (validacoes especificas)
5. Dados padrao para seed (se houver)

### Formato de entrada recomendado

Pode ser um arquivo MRDS.md existente ou uma descricao textual como:

```
Sistema: SakuraRestaurant
Entidades:
  - usuario: id, nome, email (UNIQUE), senha, tipo (admin/garcom/cozinha)
  - mesa: id, numero (UNIQUE), capacidade, status (livre/ocupada/reservada)
  - categoria: id, nome
  - item_cardapio: id, categoria_id (FK), nome, descricao, preco (REAL), disponivel (bool)
  - pedido: id, mesa_id (FK), garcom_id (FK), status (aberto/andamento/fechado/cancelado), data_hora, total (REAL)
  - item_pedido: id, pedido_id (FK), item_id (FK), quantidade (INTEGER), preco_unit (REAL), observacao
  - pagamento: id, pedido_id (FK), metodo (dinheiro/cartao/pix), valor (REAL), data_hora
```

## Saida gerada

```
sistema/
  main.py                        # entry point com menu CLI inicial
  database/
    __init__.py
    db_manager.py                # DatabaseManager + criacao de todas as tabelas + seed
  models/
    __init__.py
    entidade1.py                 # classe com validacao + to_dict()
    entidade2.py
    ...
  controllers/
    __init__.py
    entidade1_controller.py      # CRUD completo
    entidade2_controller.py
    ...
  views/
    __init__.py
```

## Fluxo de trabalho do agente

1. **Ler a skill mvc-python-sqlite** para garantir que o padrao sera seguido.
2. **Analisar a entrada** (MRDS.md ou descricao textual) para extrair
   entidades, atributos, tipos, FKs e regras.
3. **Gerar database/db_manager.py**:
   - Classe `DatabaseManager` com `__init__(db_name)`, `conectar()`, `criar_tabelas()`
   - `CREATE TABLE IF NOT EXISTS` para cada entidade
   - FKs com `REFERENCES`
   - Seed de dados padrao (se houver)
4. **Gerar models/entidade.py** para cada entidade:
   - Classe com `__init__` (construtor), `validar()`, `to_dict()`
   - Validacoes: NOT NULL, CHECK de dominio, formato de data, valor > 0
5. **Gerar controllers/entidade_controller.py** para cada entidade:
   - `criar()` — INSERT com query parametrizada
   - `listar()` — SELECT com filtros opcionais
   - `atualizar()` — UPDATE por id
   - `excluir()` — DELETE por id
   - Retorno padrao: `(True, msg)` ou `(False, msg)` para escritas; lista para leituras
6. **Gerar main.py**:
   - Import dos controllers
   - Menu CLI basico: cada entidade com opcoes de criar/listar/atualizar/excluir
7. **Criar __init__.py** vazios em database/, models/, controllers/, views/

## Regras de codigo que este agente segue

- Nomes de variavel em portugues
- Query parametrizada com `?` (nunca concatenacao)
- `try/except` em todos os metodos de controller
- Model valida no construtor e levanta `ValueError`
- Controller captura `ValueError` do model e `Exception` do banco separadamente
- `conn.close()` apos cada operacao
- `cursor.lastrowid` para obter o ID inserido

## Exemplo de uso prompt

> "Gere o projeto SakuraRestaurant com as entidades: usuario (nome, email,
> senha, tipo), mesa (numero, capacidade, status), categoria (nome),
> item_cardapio (categoria_id FK, nome, descricao, preco, disponivel),
> pedido (mesa_id FK, garcom_id FK, status, total),
> item_pedido (pedido_id FK, item_id FK, quantidade, preco_unit, observacao),
> pagamento (pedido_id FK, metodo, valor). Use a skill mvc-python-sqlite."
