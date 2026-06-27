import sqlite3
import os

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, '..', 'sakura.db')

class DatabaseManager:
    _instancia = None

    def __new__(cls, *args, **kwargs):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._conexao = None
        return cls._instancia

    def __init__(self, db_name=None):
        if not hasattr(self, '_inicializado'):
            self.db_name = db_name or DB_PATH
            self._inicializado = True
            self.criar_tabelas()

    def conectar(self):
        if self._conexao is None:
            self._conexao = sqlite3.connect(self.db_name, timeout=30)
            self._conexao.execute("PRAGMA journal_mode=WAL")
            self._conexao.execute("PRAGMA busy_timeout=10000")
            self._conexao.execute("PRAGMA foreign_keys=ON")
        return self._conexao

    def fechar(self):
        if self._conexao:
            self._conexao.close()
            self._conexao = None
        DatabaseManager._instancia = None

    def criar_tabelas(self):
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT UNIQUE NOT NULL,
            login TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            tipo TEXT NOT NULL CHECK(tipo IN ('garcom','sushiman','caixa','gerente'))
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS mesas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero INTEGER UNIQUE NOT NULL,
            capacidade INTEGER NOT NULL CHECK(capacidade > 0),
            status TEXT NOT NULL DEFAULT 'livre'
                CHECK(status IN ('livre','ocupada','reservada'))
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            descricao TEXT
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS itens_cardapio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria_id INTEGER NOT NULL,
            nome TEXT NOT NULL,
            descricao TEXT,
            preco REAL NOT NULL CHECK(preco > 0),
            disponivel INTEGER DEFAULT 1,
            ingredientes TEXT,
            valor_nutricional TEXT,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS insumos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            qtd_atual REAL DEFAULT 0,
            unidade TEXT NOT NULL
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS itens_insumo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            insumo_id INTEGER NOT NULL,
            qtd_porcao REAL NOT NULL CHECK(qtd_porcao > 0),
            FOREIGN KEY (item_id) REFERENCES itens_cardapio(id) ON DELETE CASCADE,
            FOREIGN KEY (insumo_id) REFERENCES insumos(id),
            UNIQUE(item_id, insumo_id)
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mesa_id INTEGER NOT NULL,
            garcom_id INTEGER NOT NULL,
            data_hora TEXT DEFAULT (datetime('now','localtime')),
            status TEXT NOT NULL DEFAULT 'pendente'
                CHECK(status IN ('pendente','aguardando_validacao','em_preparo','pronto','cancelado')),
            total REAL DEFAULT 0,
            FOREIGN KEY (mesa_id) REFERENCES mesas(id),
            FOREIGN KEY (garcom_id) REFERENCES usuarios(id)
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS itens_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            quantidade INTEGER NOT NULL CHECK(quantidade > 0),
            preco_no_momento REAL NOT NULL,
            observacao TEXT,
            FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE,
            FOREIGN KEY (item_id) REFERENCES itens_cardapio(id)
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS contas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER UNIQUE NOT NULL,
            caixa_id INTEGER NOT NULL,
            valor_total REAL NOT NULL,
            metodo_pagamento TEXT CHECK(metodo_pagamento IN ('pix','cartao','dinheiro')),
            status INTEGER DEFAULT 0,
            FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
            FOREIGN KEY (caixa_id) REFERENCES usuarios(id)
        )''')

        cursor.execute("SELECT COUNT(*) FROM categorias")
        if cursor.fetchone()[0] == 0:
            categorias = [
                ('Sushi', 'Pratos de sushi variados'),
                ('Sashimi', 'Fatias de peixe cru'),
                ('Temaki', 'Cone de alga com recheio'),
                ('Bebidas', 'Refrigerantes, sucos e água'),
                ('Sobremesas', 'Doces e sobremesas orientais'),
                ('Pratos Quentes', 'Opções quentes do cardápio'),
            ]
            cursor.executemany(
                "INSERT INTO categorias (nome, descricao) VALUES (?, ?)",
                categorias
            )

        cursor.execute("SELECT COUNT(*) FROM usuarios")
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO usuarios (nome, cpf, login, senha, tipo) VALUES (?, ?, ?, ?, ?)",
                ('Administrador', '000.000.000-00', 'admin', '123', 'gerente')
            )

        conn.commit()
