from models.item_cardapio import ItemCardapio
from database.db_manager import DatabaseManager

class ItemCardapioController:
    def __init__(self):
        self.db = DatabaseManager()

    def criar(self, categoria_id, nome, preco, descricao='',
              disponivel=1, ingredientes='', valor_nutricional=''):
        try:
            item = ItemCardapio(categoria_id, nome, preco, descricao,
                                disponivel, ingredientes, valor_nutricional)
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO itens_cardapio
                (categoria_id, nome, descricao, preco, disponivel, ingredientes, valor_nutricional)
                VALUES (?, ?, ?, ?, ?, ?, ?)''',
                           (item.categoria_id, item.nome, item.descricao,
                            item.preco, item.disponivel, item.ingredientes, item.valor_nutricional))
            conn.commit()
            item_id = cursor.lastrowid
            return True, f"Item '{nome}' cadastrado com sucesso! ID: {item_id}"
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro ao criar item: {str(e)}"

    def listar(self, apenas_disponiveis=False, categoria_id=None):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            query = '''SELECT ic.id, ic.nome, ic.descricao, ic.preco,
                              ic.disponivel, ic.ingredientes, ic.valor_nutricional,
                              c.nome AS categoria
                       FROM itens_cardapio ic
                       JOIN categorias c ON ic.categoria_id = c.id
                       WHERE 1=1'''
            params = []
            if apenas_disponiveis:
                query += " AND ic.disponivel = 1"
            if categoria_id:
                query += " AND ic.categoria_id = ?"
                params.append(categoria_id)
            query += " ORDER BY c.nome, ic.nome"
            cursor.execute(query, params)
            itens = cursor.fetchall()
            return itens
        except Exception as e:
            print(f"Erro ao listar itens: {str(e)}")
            return []

    def buscar_por_id(self, item_id):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute('''SELECT ic.id, ic.nome, ic.descricao, ic.preco,
                                     ic.disponivel, ic.ingredientes, ic.valor_nutricional,
                                     ic.categoria_id
                              FROM itens_cardapio ic WHERE ic.id = ?''', (item_id,))
            item = cursor.fetchone()
            return item
        except Exception as e:
            print(f"Erro ao buscar item: {str(e)}")
            return None

    def atualizar(self, item_id, **kwargs):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            campos = []
            params = []
            for campo in ('nome', 'descricao', 'preco', 'disponivel',
                          'ingredientes', 'valor_nutricional', 'categoria_id'):
                if campo in kwargs and kwargs[campo] is not None:
                    campos.append(f"{campo} = ?")
                    params.append(kwargs[campo])
            if not campos:
                return False, "Nenhum campo para atualizar"
            params.append(item_id)
            cursor.execute(f"UPDATE itens_cardapio SET {', '.join(campos)} WHERE id = ?", params)
            conn.commit()
            return True, "Item atualizado com sucesso!"
        except Exception as e:
            return False, f"Erro ao atualizar item: {str(e)}"

    def alternar_disponibilidade(self, item_id):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT disponivel FROM itens_cardapio WHERE id = ?", (item_id,))
            resultado = cursor.fetchone()
            if not resultado:
                return False, "Item não encontrado"
            novo = 0 if resultado[0] else 1
            cursor.execute("UPDATE itens_cardapio SET disponivel = ? WHERE id = ?", (novo, item_id))
            conn.commit()
            status = "disponível" if novo else "indisponível"
            return True, f"Item agora está {status}"
        except Exception as e:
            return False, f"Erro ao alternar disponibilidade: {str(e)}"

    def excluir(self, item_id):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM itens_cardapio WHERE id = ?", (item_id,))
            conn.commit()
            return True, "Item excluído com sucesso!"
        except Exception as e:
            return False, f"Erro ao excluir item: {str(e)}"
