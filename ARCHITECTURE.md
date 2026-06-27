# Arquitetura do Sakura Management System

## Padrão Arquitetural: MVC (Model-View-Controller)

O sistema segue o padrão MVC com três camadas isoladas, mais uma camada de banco.

```
┌──────────┐     ┌──────────────┐     ┌──────────┐
│  Views   │────▶│  Controllers │────▶│  Models  │
│ (Tkinter)│     │  (CRUD + RN) │     │ (Dados)  │
└──────────┘     └──────┬───────┘     └──────────┘
                        │
                        ▼
                  ┌──────────────┐
                  │  Database    │
                  │  Manager     │
                  │  (Singleton) │
                  └──────────────┘
```

### Camadas

**Models** (`models/`)
- Classes de domínio com construtor, validação e `to_dict()`
- Usam exceções `ValueError` para validar dados na criação
- 9 entidades: Usuario, Mesa, Categoria, ItemCardapio, Insumo, ItemInsumo, Pedido, ItemPedido, Conta

**Controllers** (`controllers/`)
- Um controller por entidade
- Métodos retornam `(bool, str)` para escritas, listas para leituras
- Cada método abre a conexão com o banco via `DatabaseManager`, executa query parametrizada e faz commit
- Regras de negócio implementadas nos controllers (ex.: `MesaController.abrir_mesa()` verifica RN02)

**Views** (`views/`)
- Interface Tkinter com uma classe por módulo
- Cada view cria seu controller e popula uma `Treeview` com os dados
- As views de `Pedido` e `Conta` usam `ttk.Notebook` com abas
- Fallback CLI automático se Tkinter não estiver disponível

### Database

**DatabaseManager** (`database/db_manager.py`)
- **Singleton**: todas as instâncias compartilham a mesma conexão SQLite
- Conexão única mantida aberta durante toda a execução (sem `conn.close()`)
- WAL mode (`PRAGMA journal_mode=WAL`) para leitura concorrente
- `busy_timeout=10000` para esperar até 10s em caso de contenção
- `foreign_keys=ON` para integridade referencial
- Seed automático: 6 categorias padrão + usuário admin na primeira execução

## Convenções de Código

- Nomes em português (entidades, controllers, views)
- Queries parametrizadas com `?` (sem concatenação SQL)
- `try/except ValueError` para validação de modelo; `try/except Exception` para erros de banco
- Retorno padronizado de controllers: `(sucesso: bool, mensagem: str)` para escritas

## Fluxo de Dados — Pedido

```
Cliente (touchscreen) ──▶ Garçom valida ──▶ Sushiman produz ──▶ Pronto
                              │                    │
                              ▼                    ▼
                         Pendente ──▶ Aguardando ──▶ Em Preparo ──▶ Pronto
                                                                     │
                                                                     ▼
                                                              Baixa Estoque
                                                                     │
                                                                     ▼
Cliente solicita conta ──▶ Caixa processa ──▶ Pagamento ──▶ Mesa liberada
```

## Estados do Pedido (State Pattern — camada controller)

```
pendente ──▶ aguardando_validacao ──▶ em_preparo ──▶ pronto
     │                                                   │
     └── cancelado ◀─────────────────────────────────────┘
```

## Estratégias de Pagamento (Strategy — camada controller)

```
Conta.processar_pagamento(metodo)
  ├── pix
  ├── cartao
  └── dinheiro
```

Ao confirmar o pagamento, a mesa vinculada ao pedido é automaticamente liberada para `'livre'`.

## Tratamento de Erros

- Views exibem `messagebox.showerror()` com a mensagem retornada pelo controller
- Controllers capturam `ValueError` (validação) e `Exception` (banco) separadamente
- CLI fallback usa `print()` no terminal quando Tkinter não está disponível
