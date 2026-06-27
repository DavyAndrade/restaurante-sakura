---
name: rad-python
description: >
  Use esta skill sempre que Davy estiver implementando o SISTEMA RAD em
  Python para a disciplina "Tópicos em Análise e Desenvolvimento de
  Sistemas" (4ADS, FAETERJ, Prof. Alfredo Boente), ou qualquer app Python
  desktop no mesmo estilo: GUI Tkinter + banco SQLite3 + CRUD básico
  (Inclusão, Consulta, Alteração, Remoção, Relatório). Acione esta skill ao
  escrever, revisar ou estender código Python desse tipo de sistema —
  inclusive partes isoladas como só a camada de banco ou só a tela Tkinter.
  Pressupõe que a modelagem (Casos de Uso, Classes etc.) já existe — se ainda
  não existir, use primeiro a skill "mrds-modelagem".
---

# RAD com Python (Tkinter + SQLite3)

## O que é RAD e por que a arquitetura é assim

RAD (Rapid Application Development, James Martin, 1991) é um processo ágil
incremental: módulos pequenos, ciclos curtos, e o sistema cresce por
incrementos de funcionalidade. As fases — modelagem do negócio, modelagem dos
dados, modelagem do processo, geração da aplicação, teste e modificação —
são exatamente o que a skill `mrds-modelagem` resolve antes de chegar aqui.
Esta skill cuida da fase de **geração da aplicação** e do ciclo de
teste/modificação.

O entregável profissional de RAD Python, segundo o material da disciplina,
precisa contemplar:
- **Linguagem Python**
- **GUI**: Tkinter (ou framework correlato, mas Tkinter é o padrão do curso)
- **Banco de Dados**: SQLite3 (padrão universal SQL)
- **CRUDs básicos**: Inclusão, Consulta, Alteração, Remoção e **Relatório de
  Informações** (este último é fácil de esquecer — não é só listar, é uma
  visão agregada/formatada dos dados)

## Estrutura de pastas esperada

```
meu_sistema/
├── sistema.py          # programa principal (GUI + chamadas de CRUD)
├── pacotes/
│   └── uteis.py        # funções utilitárias e esquema do banco
└── meusistema.db        # criado automaticamente na primeira execução
```

Esse é o padrão usado em todos os exemplos do curso (`agenda_pratica.py` +
`pacotes/uteis.py` + `agenda.db`). Mantenha essa separação mesmo em projetos
maiores: **nunca misture a definição do esquema do banco com a lógica da
tela**.

## Convenções de código do professor (siga-as à risca)

O material é consistente em várias convenções de estilo. Seguir essas
convenções deixa o código alinhado ao que é ensinado e esperado na correção:

- **Prefixo `v` para variáveis de entrada/edição**: `vnome`, `vtelef`,
  `vsql`, `vcon`, `vid`. Em telas Tkinter, os próprios widgets `Entry`/`Text`
  recebem esse nome (`vnome = Entry(app)`), e `vnome.get()` lê o valor digitado.
- **Nomes de função em português, no infinitivo, descrevendo a ação**:
  `inserir()`, `apagar()`, `atualizar()`, `listar()`, `consultar()`.
- **Pacote `uteis.py`** concentra as funções de apoio reutilizadas em todo o
  programa principal:
  - `linha()`, `linha1()`, `linha2()` — separadores visuais (`'='*30` etc.)
  - `limpa()` — limpa a tela
  - `menu()` — imprime o menu de opções (na versão GUI, isso é substituído
    pelos próprios componentes Tkinter, mas o nome da função pode ser
    reaproveitado para montar a janela)
  - `esquema()` — cria a tabela do banco com `CREATE TABLE IF NOT EXISTS`
    dentro de um `try/except/finally`, fechando cursor e conexão no `finally`
- **Camada de banco com três funções fixas no script principal**:
  - `banco()` — abre e retorna uma conexão (`sqlite3.connect(caminho)`)
  - `query(conexao, sql)` — executa INSERT/UPDATE/DELETE e faz `commit()`
  - `verificar(conexao, sql)` — executa SELECT e retorna `cursor.fetchall()`
  - Cada função de CRUD (`inserir`, `apagar`, `atualizar`...) abre sua própria
    conexão via `banco()` no início e fecha com `vcon.close()` no final.

### Exemplo de camada de banco (estilo do curso)

```python
import sqlite3 as conector
from sqlite3 import Error

def banco():
    caminho = 'meusistema.db'
    try:
        conexao = conector.connect(caminho)
    except Error as ex:
        print(ex)
    return conexao

def query(conexao, sql, params=None):
    try:
        c = conexao.cursor()
        c.execute(sql, params or ())
        conexao.commit()
    except Error as ex:
        print(ex)
    finally:
        print('Operação concluída!')

def verificar(conexao, sql, params=None):
    c = conexao.cursor()
    c.execute(sql, params or ())
    return c.fetchall()
```

> **Atenção — desvio deliberado do material original:** o exemplo de CLI do
> curso (`agenda_pratica.py`) monta o SQL por concatenação de string
> (`"INSERT INTO agenda (nome, telef) VALUES ('"+vnome+"','"+vtelef+"')"`).
> Isso é didático, mas é SQL injection na cara. Para a entrega real, **use
> sempre query parametrizada** (`?` ou `:nome`), como o próprio material já
> faz no exemplo de GUI+BD (`guibd.py`, AULA 9) com placeholders nomeados.
> Ou seja: siga a arquitetura do curso, mas use o estilo de query seguro que
> o próprio curso usa na aula mais avançada.

### Esquema do banco

```python
comando = '''CREATE TABLE IF NOT EXISTS minha_tabela (
        id INTEGER NOT NULL,
        nome VARCHAR(32) NOT NULL,
        telef VARCHAR(15) NOT NULL,
        PRIMARY KEY(id)
        );'''
```

Use sempre `INTEGER ... PRIMARY KEY` para chave autoincremento (estilo
SQLite) e tipos `VARCHAR(n)`/`TEXT`/`INTEGER`/`REAL` compatíveis com SQL
padrão — não use tipagem específica de outro SGBD.

## Camada de interface — Tkinter

### Janela básica

```python
from tkinter import *

app = Tk()
app.title('Nome do Sistema')
app.geometry('500x350')
app.configure(background='light grey')
app.mainloop()
```

### Padrão Label + Entry (campo simples)

```python
Label(app, text='Nome', background='light grey',
      foreground='midnight blue', anchor=W).place(x=10, y=10, width=100, height=20)
vnome = Entry(app)
vnome.place(x=10, y=30, width=200, height=20)
```

Use `Text(app)` (não `Entry`) para campos de múltiplas linhas (ex.:
observações) — e lembre que a leitura de um `Text` é `vobs.get(1.0, END)`,
diferente de `Entry.get()`.

### Botão + limpeza de campos após salvar

```python
def gravar():
    conn = sqlite3.connect('meusistema.db')
    c = conn.cursor()
    c.execute("INSERT INTO minha_tabela (nome, telef) VALUES (:nome, :telef)",
              {'nome': vnome.get(), 'telef': vtelef.get()})
    conn.commit()
    conn.close()
    messagebox.showinfo("MENSAGEM IMPORTANTE", "Informações gravadas com sucesso!")
    vnome.delete(0, END)
    vtelef.delete(0, END)
    Entry.focus(vnome)

Button(app, text='Gravar', command=gravar).place(x=10, y=270, width=100, height=30)
```

Esse trio — `messagebox.showinfo` de confirmação, limpeza dos campos
(`delete`) e refoco no primeiro campo (`Entry.focus`) — é o padrão esperado
após qualquer operação de escrita (incluir/alterar/remover).

### Layouts mais ricos (sistemas de "complexidade média/alta")

Para telas com várias seções, use `Frame` com `pack(side=LEFT/RIGHT/TOP/BOTTOM)`
para dividir a janela em blocos, e dentro de cada bloco prefira `grid()` para
alinhar pares Label/Entry em linhas e colunas (mais previsível que `place()`
quando há muitos campos). Para imagens (ícone do app, logo, foto de produto):

```python
from PIL import Image, ImageTk   # pip install pillow
tkimage = ImageTk.PhotoImage(Image.open(caminho_da_imagem))
Label(frame, image=tkimage).grid(row=0, column=0)
```

## Checklist de CRUD completo

Todo sistema entregue precisa cobrir, com tela própria ou seção de tela para
cada um:

- [ ] **Inclusão** — formulário + botão "Incluir"/"Gravar"
- [ ] **Consulta** — busca por algum campo (ex.: `LIKE '%texto%'` para nome)
- [ ] **Alteração** — carregar registro existente, editar, salvar
- [ ] **Remoção** — apagar por id, idealmente com confirmação
  (`messagebox.askyesno`)
- [ ] **Relatório de Informações** — listagem formatada/agrupada de todos os
  registros (pode ser uma `Treeview`/`Listbox` na GUI, ou uma tela dedicada
  de relatório — não é apenas reaproveitar a consulta)

## Tratamento de erro e exceção

Padrão do curso: `try / except / else` para fluxo geral, e
`try / except Error / finally` para conexões de banco (sempre fechando
cursor e conexão no `finally`, mesmo se a operação falhar):

```python
try:
    a = int(entrada_a.get())
    b = int(entrada_b.get())
    r = a / b
except Exception:
    messagebox.showerror('Erro', 'Operação inválida!')
else:
    messagebox.showinfo('Resultado', f'O resultado é {r}')
```

Capture exceções específicas quando fizer sentido (`sqlite3.OperationalError`,
`sqlite3.DatabaseError`) em vez de `except:` genérico, especialmente na
criação do esquema do banco.

## Fundamentos de Python cobrados na disciplina (referência rápida)

Use como lembrete de sintaxe ao escrever o código — não é o foco principal
desta skill, mas é pré-requisito direto do RAD:

- **Tipos primitivos**: `int()`, `float()`, `bool()`, `str()`; tipagem
  dinâmica (`type(var)`); `isnumeric()`, `isalpha()`, `isalnum()`.
- **Strings**: aspas simples como padrão da comunidade; fatiamento
  `frase[13:24]`; formatação preferencial com f-string: `f'{nome} tem
  {idade} anos'`.
- **Coleções**: tuplas, listas e dicionários — escolha dicionário quando o
  registro tiver campos nomeados (mapeia bem para uma linha de tabela).
- **Funções/módulos/pacotes**: `def nome(parametros=default):`; separar
  utilitários reaproveitáveis em `pacotes/uteis.py`, importados com
  `from pacotes.uteis import esquema, linha, limpa, menu`.

## Quando voltar para a outra skill

Se durante a implementação surgir a necessidade de uma classe, atributo ou
fluxo que não estava no Diagrama de Classes / Casos de Uso, volte para a
skill **mrds-modelagem** e atualize o modelo (e a Matriz de Rastreabilidade)
antes de seguir codificando — a entrega é avaliada pela coerência entre o
modelo e o sistema, não só pelo sistema funcionando.