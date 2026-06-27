# Modelagem Relacional de Dados do Sistema (MRDS)
## Sakura Management System — Restaurante Sakura

---

## 1. DIAGRAMA ENTIDADE-RELACIONAMENTO (DER)

```
┌─────────────────────────┐
│        USUARIOS         │
├─────────────────────────┤
│ PK id                   │
│    nome                 │
│    cpf (UK)             │
│    login (UK)           │
│    senha                │
│    tipo                 │  ← 'garcom' | 'sushiman' | 'caixa' | 'gerente'
└───────────┬─────────────┘
            │
            ├──────────────────────────────┬─────────────────────────┐
            │ 1                            │ 1                       │ 1
            │                              │                         │
            │ N                            │ N                       │ N
            │                              │                         │
┌───────────┴─────────────┐  ┌─────────────┴──────────┐  ┌──────────┴──────────┐
│        PEDIDOS          │  │         CONTAS         │  │      ITEM_CARDAPIO  │
├─────────────────────────┤  ├────────────────────────┤  ├─────────────────────┤
│ PK id                   │  │ PK id                  │  │ PK id               │
│ FK mesa_id              │  │ FK pedido_id           │  │ FK categoria_id     │
│ FK garcom_id            │  │ FK caixa_id            │  │    nome             │
│    data_hora            │  │    valor_total         │  │    descricao        │
│    status               │  │    metodo_pagamento    │  │    preco            │
│    total                │  │    status              │  │    disponivel       │
└───────────┬─────────────┘  └────────────────────────┘  │    ingredientes     │
            │                                             │    valor_nutricional│
            │ 1                                           └──────────┬──────────┘
            │                                                       │ 1
            │ N                                                     │
            │                                                       │ N
┌───────────┴─────────────┐                                 ┌───────┴───────────┐
│      ITENS_PEDIDO       │                                 │     ITENS_INSUMO  │
├─────────────────────────┤                                 ├───────────────────┤
│ PK id                   │                                 │ PK id             │
│ FK pedido_id            │                                 │ FK item_id        │
│ FK item_id              │                                 │ FK insumo_id      │
│    quantidade           │                                 │    qtd_porcao     │
│    preco_no_momento     │                                 └───────┬───────────┘
│    observacao           │                                         │
└─────────────────────────┘                                         │
                                                                     │
                                                           ┌─────────┴──────────┐
                                                           │      INSUMOS       │
                                                           ├────────────────────┤
                                                           │ PK id              │
                                                           │    nome (UK)       │
                                                           │    qtd_atual       │
                                                           │    unidade         │
                                                           └────────────────────┘

┌─────────────────────────┐
│         MESAS           │
├─────────────────────────┤
│ PK id                   │
│    numero (UK)          │
│    capacidade           │
│    status               │  ← 'livre' | 'ocupada' | 'reservada'
└─────────────────────────┘

┌─────────────────────────┐
│       CATEGORIAS        │
├─────────────────────────┤
│ PK id                   │
│    nome (UK)            │
│    descricao            │
└─────────────────────────┘
```

---

## 2. DESCRIÇÃO DAS ENTIDADES

### 2.1 USUARIOS
Armazena todos os funcionários do restaurante (Garçom, Sushiman, Caixa, Gerente) com discriminação por tipo, aplicando o princípio de generalização (herança) da classe abstrata `Funcionario`.

**Atributos:**
- `id` (INTEGER) - Chave Primária, Auto Incremento
- `nome` (TEXT) - Nome completo, NOT NULL
- `cpf` (TEXT) - CPF do funcionário, UNIQUE, NOT NULL
- `login` (TEXT) - Login para acesso ao sistema, UNIQUE, NOT NULL
- `senha` (TEXT) - Senha de acesso, NOT NULL
- `tipo` (TEXT) - Cargo: 'garcom', 'sushiman', 'caixa' ou 'gerente', NOT NULL, CHECK

**Restrições:**
- CPF e login devem ser únicos
- Tipo deve ser um dos quatro valores definidos

**Relacionamentos:**
- 1:N com PEDIDOS (um garçom valida vários pedidos)
- 1:N com CONTAS (um caixa processa várias contas)

---

### 2.2 MESAS
Representa as mesas físicas do restaurante, com controle de capacidade e status.

**Atributos:**
- `id` (INTEGER) - Chave Primária, Auto Incremento
- `numero` (INTEGER) - Número da mesa no mapa do restaurante, UNIQUE, NOT NULL
- `capacidade` (INTEGER) - Número máximo de lugares, NOT NULL
- `status` (TEXT) - Situação: 'livre', 'ocupada' ou 'reservada', NOT NULL, DEFAULT 'livre'

**Restrições:**
- Número da mesa deve ser único
- Capacidade deve ser maior que zero
- Status deve ser 'livre', 'ocupada' ou 'reservada'

**Relacionamentos:**
- 1:N com PEDIDOS (uma mesa pode ter vários pedidos ao longo do tempo)

---

### 2.3 CATEGORIAS
Classificação dos itens do cardápio (ex.: Sushi, Temaki, Bebidas, Sobremesas).

**Atributos:**
- `id` (INTEGER) - Chave Primária, Auto Incremento
- `nome` (TEXT) - Nome da categoria, UNIQUE, NOT NULL
- `descricao` (TEXT) - Descrição opcional da categoria

**Relacionamentos:**
- 1:N com ITENS_CARDAPIO (uma categoria pode ter vários itens)

---

### 2.4 ITENS_CARDAPIO
Pratos e bebidas do cardápio digital, com dados nutricionais, ingredientes e controle de disponibilidade.

**Atributos:**
- `id` (INTEGER) - Chave Primária, Auto Incremento
- `categoria_id` (INTEGER) - Chave Estrangeira para CATEGORIAS(id), NOT NULL
- `nome` (TEXT) - Nome do prato/bebida, NOT NULL
- `descricao` (TEXT) - Descrição detalhada do item
- `preco` (REAL) - Preço de venda, NOT NULL, CHECK(preco > 0)
- `disponivel` (INTEGER) - Flag: 1=disponível, 0=indisponível, DEFAULT 1
- `ingredientes` (TEXT) - Lista de ingredientes (texto livre)
- `valor_nutricional` (TEXT) - Informação nutricional (calorias, alérgenos)

**Restrições:**
- Preço deve ser maior que zero

**Relacionamentos:**
- N:1 com CATEGORIAS (um item pertence a uma categoria)
- 1:N com ITENS_PEDIDO (um item pode estar em vários pedidos)
- 1:N com ITENS_INSUMO (um item pode usar vários insumos, com quantidade por porção)

---

### 2.5 INSUMOS
Matéria-prima utilizada na produção dos pratos, com controle de estoque.

**Atributos:**
- `id` (INTEGER) - Chave Primária, Auto Incremento
- `nome` (TEXT) - Nome do insumo, UNIQUE, NOT NULL
- `qtd_atual` (REAL) - Quantidade atual em estoque, DEFAULT 0
- `unidade` (TEXT) - Unidade de medida (kg, g, un, l, ml), NOT NULL

**Restrições:**
- Nome do insumo deve ser único

**Relacionamentos:**
- 1:N com ITENS_INSUMO (um insumo pode estar em vários itens do cardápio)

---

### 2.6 ITENS_INSUMO
Tabela associativa (N:N) entre ITENS_CARDAPIO e INSUMOS, representando a ficha técnica: quais insumos cada prato consome e em qual quantidade por porção. Aplica a RN08 (Baixa Automática de Insumos).

**Atributos:**
- `id` (INTEGER) - Chave Primária, Auto Incremento
- `item_id` (INTEGER) - Chave Estrangeira para ITENS_CARDAPIO(id), NOT NULL
- `insumo_id` (INTEGER) - Chave Estrangeira para INSUMOS(id), NOT NULL
- `qtd_porcao` (REAL) - Quantidade do insumo necessária para uma porção do prato, NOT NULL, CHECK(qtd_porcao > 0)

**Restrições:**
- Par (item_id, insumo_id) deve ser único (um insumo só aparece uma vez na ficha de cada prato)

---

### 2.7 PEDIDOS
Representa o pedido realizado em uma mesa, com controle de status para implementação do padrão State.

**Atributos:**
- `id` (INTEGER) - Chave Primária, Auto Incremento
- `mesa_id` (INTEGER) - Chave Estrangeira para MESAS(id), NOT NULL
- `garcom_id` (INTEGER) - Chave Estrangeira para USUARIOS(id), NOT NULL
- `data_hora` (TEXT) - Data e hora do pedido, DEFAULT CURRENT_TIMESTAMP
- `status` (TEXT) - Status do pedido: 'pendente', 'aguardando_validacao', 'em_preparo', 'pronto' ou 'cancelado', NOT NULL, DEFAULT 'pendente'
- `total` (REAL) - Valor total do pedido, DEFAULT 0

**Restrições:**
- Status deve ser um dos valores definidos (alinhado com RN05, RN06)

**Relacionamentos:**
- N:1 com MESAS (um pedido pertence a uma mesa)
- N:1 com USUARIOS (um pedido é validado por um garçom)
- 1:N com ITENS_PEDIDO (composição: um pedido contém vários itens)
- 1:1 com CONTAS (um pedido gera uma conta)

---

### 2.8 ITENS_PEDIDO
Itens individuais de um pedido (composição). Implementa o relacionamento todo-parte forte entre Pedido e ItemPedido.

**Atributos:**
- `id` (INTEGER) - Chave Primária, Auto Incremento
- `pedido_id` (INTEGER) - Chave Estrangeira para PEDIDOS(id), NOT NULL
- `item_id` (INTEGER) - Chave Estrangeira para ITENS_CARDAPIO(id), NOT NULL
- `quantidade` (INTEGER) - Quantidade do item, NOT NULL, CHECK(quantidade > 0)
- `preco_no_momento` (REAL) - Preço do item no momento da compra (para histórico), NOT NULL
- `observacao` (TEXT) - Observação opcional (ex.: "sem cebola", "ponto mal passado")

---

### 2.9 CONTAS
Registro financeiro da conta de um pedido, com método de pagamento para implementação do padrão Strategy.

**Atributos:**
- `id` (INTEGER) - Chave Primária, Auto Incremento
- `pedido_id` (INTEGER) - Chave Estrangeira para PEDIDOS(id), UNIQUE, NOT NULL
- `caixa_id` (INTEGER) - Chave Estrangeira para USUARIOS(id), NOT NULL
- `valor_total` (REAL) - Valor total da conta, NOT NULL
- `metodo_pagamento` (TEXT) - Método: 'pix', 'cartao' ou 'dinheiro', NULLABLE (permite pendente)
- `status` (INTEGER) - Flag: 0=aberta, 1=paga, DEFAULT 0

**Restrições:**
- Cada pedido gera no máximo uma conta (pedido_id é UNIQUE)

**Relacionamentos:**
- 1:1 com PEDIDOS (uma conta referencia um pedido)
- N:1 com USUARIOS (uma conta é processada por um caixa)

---

## 3. RELACIONAMENTOS

### 3.1 USUARIOS → PEDIDOS (1:N)
- Um garçom pode validar vários pedidos
- Cada pedido é validado por um único garçom
- Cardinalidade: (0,N) - (1,1)

### 3.2 USUARIOS → CONTAS (1:N)
- Um caixa pode processar várias contas
- Cada conta é processada por um único caixa
- Cardinalidade: (0,N) - (1,1)

### 3.3 MESAS → PEDIDOS (1:N)
- Uma mesa pode ter vários pedidos ao longo do tempo
- Cada pedido pertence a uma única mesa
- Cardinalidade: (0,N) - (1,1)

### 3.4 CATEGORIAS → ITENS_CARDAPIO (1:N)
- Uma categoria pode ter vários itens
- Cada item pertence a uma única categoria
- Cardinalidade: (1,N) - (1,1)

### 3.5 ITENS_CARDAPIO → ITENS_PEDIDO (1:N)
- Um item pode aparecer em vários pedidos
- Cada item_pedido referencia um único item do cardápio
- Cardinalidade: (0,N) - (1,1)

### 3.6 PEDIDOS → ITENS_PEDIDO (1:N) — COMPOSIÇÃO
- Um pedido contém um ou mais itens (composição forte)
- Itens de pedido não existem sem o pedido
- Cardinalidade: (1,1) - (1,N) na parte todo

### 3.7 PEDIDOS → CONTAS (1:1)
- Um pedido gera no máximo uma conta
- Cada conta referencia exatamente um pedido
- Cardinalidade: (0,1) - (1,1)

### 3.8 ITENS_CARDAPIO → ITENS_INSUMO → INSUMOS (N:N)
- Um item do cardápio pode usar vários insumos (através de ITENS_INSUMO)
- Um insumo pode estar em vários itens do cardápio
- Cardinalidade: (0,N) - (0,N)

---

## 4. REGRAS DE NEGÓCIO

### 4.1 Regras para Usuários
1. Cada funcionário deve ter CPF e login únicos no sistema
2. O tipo do usuário define suas permissões: apenas Gerente pode ajustar estoque, apenas Caixa pode processar pagamento

### 4.2 Regras para Mesas
1. RN02 — Uma mesa só pode ser aberta se seu status for 'livre'
2. RN02 — Ao abrir, status altera para 'ocupada'
3. RN13 — Status só volta para 'livre' após confirmação de pagamento integral

### 4.3 Regras para Cardápio e Itens
1. RN04 — Cardápio deve exibir preço, ingredientes e valor nutricional
2. RN09 — Sushiman pode ativar/desativar itens em tempo real
3. Todo item pertence a uma categoria

### 4.4 Regras para Pedidos
1. RN05 — Pedido inicia como 'pendente' e precisa de validação do garçom
2. RN05 — Após validação, status muda para 'aguardando_validacao' e segue para produção
3. RN06 — Sushiman altera status para 'em_preparo' e depois 'pronto'
4. RN08 — Ao marcar como 'pronto', baixa automática de insumos via itens_insumo

### 4.5 Regras para Contas
1. RN11 — Processamento financeiro é exclusivo do Caixa
2. RN12 — Suporta Pix, Cartão e Dinheiro
3. RN12 — Permite fechamento parcial ou dividido

### 4.6 Regras para Estoque
1. RN08 — Baixa automática por porção unitária ao finalizar preparo
2. RN09 — Se insumo crítico atinge nível zero, sistema bloqueia novos pedidos do prato relacionado
3. RN10 — Ajustes manuais são exclusivos do Gerente

---

## 5. ÍNDICES E OTIMIZAÇÕES

```sql
-- Índices para chaves estrangeiras (JOINs)
CREATE INDEX idx_pedidos_mesa ON pedidos(mesa_id);
CREATE INDEX idx_pedidos_garcom ON pedidos(garcom_id);
CREATE INDEX idx_itens_pedido_pedido ON itens_pedido(pedido_id);
CREATE INDEX idx_itens_pedido_item ON itens_pedido(item_id);
CREATE INDEX idx_contas_pedido ON contas(pedido_id);
CREATE INDEX idx_contas_caixa ON contas(caixa_id);
CREATE INDEX idx_itens_cardapio_categoria ON itens_cardapio(categoria_id);
CREATE INDEX idx_itens_insumo_item ON itens_insumo(item_id);
CREATE INDEX idx_itens_insumo_insumo ON itens_insumo(insumo_id);

-- Índices para buscas frequentes
CREATE INDEX idx_pedidos_status ON pedidos(status);
CREATE INDEX idx_pedidos_data ON pedidos(data_hora);
CREATE INDEX idx_usuarios_tipo ON usuarios(tipo);
CREATE INDEX idx_mesas_status ON mesas(status);
CREATE INDEX idx_contas_status ON contas(status);
CREATE UNIQUE INDEX idx_usuarios_login ON usuarios(login);
CREATE UNIQUE INDEX idx_usuarios_cpf ON usuarios(cpf);
```

---

## 6. INTEGRIDADE REFERENCIAL

| FK | Referencia | Cascade |
|---|---|---|
| pedidos.mesa_id | mesas.id | ON DELETE RESTRICT |
| pedidos.garcom_id | usuarios.id | ON DELETE RESTRICT |
| itens_pedido.pedido_id | pedidos.id | ON DELETE CASCADE |
| itens_pedido.item_id | itens_cardapio.id | ON DELETE RESTRICT |
| itens_cardapio.categoria_id | categorias.id | ON DELETE RESTRICT |
| contas.pedido_id | pedidos.id | ON DELETE RESTRICT |
| contas.caixa_id | usuarios.id | ON DELETE RESTRICT |
| itens_insumo.item_id | itens_cardapio.id | ON DELETE CASCADE |
| itens_insumo.insumo_id | insumos.id | ON DELETE RESTRICT |

---

## 7. DICIONÁRIO DE DADOS

| Tipo SQLite | Uso |
|---|---|
| INTEGER | IDs, flags booleanas (0/1), quantidades, números de mesa |
| TEXT | Nomes, descrições, logins, senhas, status, datas ISO, ingredientes |
| REAL | Preços, valores monetários, quantidades de insumo |

**Convenções:**
- Nomes de tabelas em plural e minúsculas
- Chaves primárias sempre chamadas `id`
- Chaves estrangeiras no formato `{tabela}_id`
- Datas em ISO 8601 (`YYYY-MM-DD HH:MM:SS`)
- Booleanos: 0 (falso/inativo/livre) e 1 (verdadeiro/ativo/ocupado)
- Enumerações em texto com CHECK: `'livre','ocupada','reservada'`; `'pendente','aguardando_validacao','em_preparo','pronto','cancelado'`; `'pix','cartao','dinheiro'`

---

## 8. QUERIES ÚTEIS

### 8.1 Cardápio disponível com categoria
```sql
SELECT ic.id, ic.nome, ic.preco, c.nome AS categoria
FROM itens_cardapio ic
JOIN categorias c ON ic.categoria_id = c.id
WHERE ic.disponivel = 1
ORDER BY c.nome, ic.nome;
```

### 8.2 Pedidos pendentes para a cozinha (KDS)
```sql
SELECT p.id, m.numero AS mesa, p.data_hora,
       GROUP_CONCAT(ic.nome || ' x' || ip.quantidade, ', ') AS itens
FROM pedidos p
JOIN mesas m ON p.mesa_id = m.id
JOIN itens_pedido ip ON ip.pedido_id = p.id
JOIN itens_cardapio ic ON ip.item_id = ic.id
WHERE p.status IN ('aguardando_validacao', 'em_preparo')
GROUP BY p.id
ORDER BY p.data_hora;
```

### 8.3 Faturamento do dia
```sql
SELECT SUM(valor_total) AS faturamento, COUNT(*) AS total_contas
FROM contas
WHERE status = 1 AND DATE(data_hora) = DATE('now');
```

### 8.4 Baixar estoque ao finalizar preparo (gatilho)
```sql
SELECT ii.insumo_id, ii.qtd_porcao * ip.quantidade AS total_baixa
FROM itens_pedido ip
JOIN itens_insumo ii ON ip.item_id = ii.item_id
WHERE ip.pedido_id = ?;
```

### 8.5 Verificar disponibilidade de insumo para um item
```sql
SELECT i.nome AS insumo,
       ii.qtd_porcao AS necessario,
       ins.qtd_atual AS disponivel,
       CASE WHEN ins.qtd_atual >= ii.qtd_porcao THEN 'OK' ELSE 'INSUFICIENTE' END AS status
FROM itens_insumo ii
JOIN insumos ins ON ii.insumo_id = ins.id
JOIN itens_cardapio ic ON ii.item_id = ic.id
JOIN insumos i ON ii.insumo_id = i.id
WHERE ic.id = ?;
```
