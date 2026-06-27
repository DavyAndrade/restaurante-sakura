---
name: mvc-python-sqlite
description: >
  Use esta skill ao construir, estender ou revisar qualquer sistema
  desktop em Python que siga o padrao MVC (Model-View-Controller) com
  banco SQLite3. Ela consolida o padrao arquitetural observado no sistema
  "controle_gastos/" e serve como receita para novos projetos como
  "SakuraRestaurant" — ou qualquer outro sistema no mesmo estilo.
  Pressupoe que a modelagem de dados ja existe (use a skill
  "modelagem-dados-sqlite" se ainda nao existir).
---

# MVC com Python + SQLite3

## Por que esta skill existe

O sistema `controle_gastos/` estabeleceu um padrao concreto para
construir aplicacoes desktop Python com SQLite seguindo MVC. Esta skill
captura esse padrao para que qualquer projeto novo — como o SakuraRestaurant
— possa reaproveitar a arquitetura sem reinventar a estrutura de pastas,
a camada de banco, o estilo dos models, ou o fluxo dos controllers.

## Estrutura de pastas esperada

```
meu_sistema/
  main.py                     # entry point: cria controllers e inicia a interface
  database/
    __init__.py
    db_manager.py             # gerenciamento de conexao e criacao de tabelas
  models/
    __init__.py
    entidade1.py              # uma classe por entidade
    entidade2.py
  controllers/
    __init__.py
    entidade1_controller.py   # um controller por entidade
    entidade2_controller.py
  views/
    __init__.py               # telas Tkinter (ou CLI no estilo do controle_gastos)
```

Todos os `__init__.py` podem ficar vazios — existem apenas para tornar os
diretorios em pacotes Python.

## Camada de dados — DatabaseManager

Crie um gerenciador unico que centraliza a conexao e a criacao do esquema:

```python
# database/db_manager.py
import sqlite3

class DatabaseManager:
    def __init__(self, db_name='meu_sistema.db'):
        self.db_name = db_name
        self.criar_tabelas()

    def conectar(self):
        return sqlite3.connect(self.db_name)

    def criar_tabelas(self):
        conn = self.conectar()
        cursor = conn.cursor()
        # Executar CREATE TABLE IF NOT EXISTS para cada entidade
        cursor.execute('''CREATE TABLE IF NOT EXISTS entidade1 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            ...
        )''')
        # Seed de dados padrao (se houver)
        conn.commit()
        conn.close()
```

### Convencoes de nomenclatura do banco

| Convencao | Exemplo |
|---|---|
| Nome da tabela: plural minusculo | `usuarios`, `contas`, `transacoes` |
| Chave primaria: sempre `id` | `id INTEGER PRIMARY KEY AUTOINCREMENT` |
| Chave estrangeira: `{tabela}_id` | `usuario_id`, `conta_id` |
| Flag booleana: `INTEGER DEFAULT 0` | `padrao INTEGER DEFAULT 0` |
| Moeda: `REAL` | `saldo_inicial REAL DEFAULT 0` |
| String: `TEXT` ou `VARCHAR(n)` | `nome TEXT NOT NULL` |
| Unico: `UNIQUE` direto na coluna | `email TEXT UNIQUE NOT NULL` |

### Uso de chaves estrangeiras

```sql
FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
```

### Query parametrizada (sempre — nunca concatenacao de strings)

```python
cursor.execute("INSERT INTO entidade (campo) VALUES (?)", (valor,))
cursor.execute("SELECT * FROM entidade WHERE id = ?", (id_alvo,))
cursor.execute("UPDATE entidade SET campo = ? WHERE id = ?", (novo_valor, id_alvo))
cursor.execute("DELETE FROM entidade WHERE id = ?", (id_alvo,))
```

## Camada de Model

Cada entidade vira uma classe com `__init__` (validacao inclusa) e `to_dict()`:

```python
# models/entidade1.py
class Entidade1:
    def __init__(self, campo1, campo2, ..., id=None):
        self.id = id
        self.campo1 = campo1
        self.campo2 = campo2
        self.validar()

    def validar(self):
        if not self.campo1:
            raise ValueError("campo1 e obrigatorio")
        # outras validacoes

    def to_dict(self):
        return {
            'id': self.id,
            'campo1': self.campo1,
            'campo2': self.campo2,
        }
```

### Padroes de validacao observados no controle_gastos

- Valor monetario: `if self.valor <= 0: raise ValueError("...")`
- Campo com valores fixos: `if self.tipo not in ['opcao1', 'opcao2']: raise ValueError("...")`
- Formato de data: `datetime.strptime(self.data, '%Y-%m-%d')` com `except ValueError`

## Camada de Controller

Cada controller recebe um `DatabaseManager` (instancia propria) e expoe
metodos que retornam `(sucesso: bool, mensagem: str)` para operacoes de
escrita e listas para operacoes de leitura:

```python
# controllers/entidade1_controller.py
from models.entidade1 import Entidade1
from database.db_manager import DatabaseManager

class Entidade1Controller:
    def __init__(self):
        self.db = DatabaseManager()

    def criar(self, ...):
        try:
            obj = Entidade1(...)
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("INSERT ... VALUES (?)", (...))
            conn.commit()
            obj_id = cursor.lastrowid
            conn.close()
            return True, "Cadastrado com sucesso! ID: {obj_id}"
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro: {str(e)}"

    def listar(self, usuario_id=None, filtros=None):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            query = "SELECT ... FROM ... WHERE 1=1"
            params = []
            if filtros:
                ...
            cursor.execute(query, params)
            resultados = cursor.fetchall()
            conn.close()
            return resultados
        except Exception as e:
            print(f"Erro ao listar: {str(e)}")
            return []

    def atualizar(self, id, ...):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("UPDATE entidade SET campo = ? WHERE id = ?", (valor, id))
            conn.commit()
            conn.close()
            return True, "Atualizado com sucesso!"
        except Exception as e:
            return False, f"Erro ao atualizar: {str(e)}"

    def excluir(self, id):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM entidade WHERE id = ?", (id,))
            conn.commit()
            conn.close()
            return True, "Excluido com sucesso!"
        except Exception as e:
            return False, f"Erro ao excluir: {str(e)}"
```

### Fluxo de controller com validacao do model

```
Metodo do controller
  -> instancia o Model (validacao acontece aqui)
    -> se ValueError: retorna (False, msg de erro)
  -> persiste no banco com query parametrizada
    -> se Exception: retorna (False, msg de erro)
  -> retorna (True, mensagem de sucesso)
```

## Camada de Interface

- **CLI (terminal):** menu `while True` com `input()` e `if/elif` para cada
  opcao, reaproveitando os controllers.
- **GUI (Tkinter):** use `Tk()` + `Label`/`Entry`/`Button` com `.place()`
  ou `.grid()`; mensagens com `messagebox.showinfo/askyesno`; limpeza de
  campos apos salvar com `.delete(0, END)`.

O `main.py` do `controle_gastos` mostra o padrao CLI:
```python
from database.db_manager import DatabaseManager
from controllers.entidade1_controller import Entidade1Controller
from controllers.entidade2_controller import Entidade2Controller

db = DatabaseManager()
ctrl1 = Entidade1Controller()
ctrl2 = Entidade2Controller()
usuario_id = 1  # simplificado

while True:
    # exibe menu, le opcao, chama controller, mostra resultado
```

## Checklist de implantacao para novo projeto

- [ ] Estrutura de pastas criada (database/, models/, controllers/, views/)
- [ ] `database/db_manager.py` com `DatabaseManager` e `criar_tabelas()`
- [ ] Models com `__init__` (validacao), `validar()`, `to_dict()`
- [ ] Controllers com os 5 CRUDs: criar, listar, atualizar, excluir + relatorio
- [ ] Queries parametrizadas (sem concatenacao de string SQL)
- [ ] `try/except` em cada metodo de controller
- [ ] Interface (CLI ou Tkinter) consumindo os controllers
- [ ] Seed de dados padrao no `criar_tabelas()` (se aplicavel)

## Quando usar outras skills

- **modelagem-dados-sqlite** — antes de comecar a codificar, para definir
  as entidades, atributos, relacoes e documentar no formato MRDS.
- **rad-python** (skills/rad-python/) — se o projeto for uma entrega da
  disciplina 4ADS e precisar seguir as convencoes de codigo do professor
  (prefixo `v`, `uteis.py`, funcoes `banco()`/`query()`/`verificar()`).
