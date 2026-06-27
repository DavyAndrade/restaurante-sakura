# Sakura Management System

Sistema de gestão operacional para o Restaurante Sakura — controle de mesas, cardápio digital, pedidos, produção, estoque e fluxo financeiro.

## Tecnologias

- **Python 3.7+**
- **Tkinter** — interface gráfica desktop
- **SQLite3** — banco de dados embutido com WAL mode
- **MVC** — arquitetura Model-View-Controller

## Instalação

```bash
# Ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate

# Dependências (apenas stdlib, nada a instalar via pip)
pip install -r requirements.txt

# Tkinter (Debian/Ubuntu)
sudo apt install python3-tk

# Tkinter (Arch/CachyOS)
sudo pacman -S tk
```

## Execução

```bash
python main.py
```

**Login padrão:** `admin` / `123` (gerente)

## Funcionalidades

| Módulo | Operações |
|---|---|
| **Usuários** | Cadastro de garçons, sushimans, caixas e gerentes |
| **Mesas** | Controle de status (livre/ocupada/reservada), abertura e liberação |
| **Categorias** | Classificação de itens do cardápio (Sushi, Bebidas, etc.) |
| **Cardápio** | Itens com preço, ingredientes, valor nutricional, disponibilidade |
| **Insumos** | Estoque por insumo, ajustes, vínculo com ficha técnica dos pratos |
| **Pedidos** | Ciclo completo: pendente → validação → preparo → pronto |
| **Contas** | Abertura, pagamento (Pix/Cartão/Dinheiro), relatório de vendas |

## Estrutura do Projeto

```
main.py                  # entry point (Tkinter ou CLI fallback)
database/
  db_manager.py          # DatabaseManager singleton + schema SQLite
models/                  # Classes de domínio com validação
  usuario.py | mesa.py | categoria.py | item_cardapio.py
  insumo.py | item_insumo.py | pedido.py | item_pedido.py | conta.py
controllers/             # CRUD + regras de negócio
  usuario_controller.py  | mesa_controller.py
  categoria_controller.py | item_cardapio_controller.py
  insumo_controller.py  | pedido_controller.py
  conta_controller.py
views/                   # Interface Tkinter
  login_view.py          | main_view.py
  usuario_view.py        | mesa_view.py
  categoria_view.py      | cardapio_view.py
  insumo_view.py         | pedido_view.py
  conta_view.py          | cli.py (fallback terminal)
docs/
  MRDS.md                # Modelagem UML (casos de uso, classes, sequência)
  MRDS-BANCO.md           # Modelagem relacional SQLite
```

## Modelo de Dados

9 tabelas: `usuarios`, `mesas`, `categorias`, `itens_cardapio`, `insumos`, `itens_insumo`, `pedidos`, `itens_pedido`, `contas`. Detalhes completos em `docs/MRDS-BANCO.md`.
