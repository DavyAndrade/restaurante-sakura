from models.categoria import Categoria
from database.db_manager import DatabaseManager

class CategoriaController:
    def __init__(self):
        self.db = DatabaseManager()

    def criar(self, nome, descricao=''):
        try:
            categoria = Categoria(nome, descricao)
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO categorias (nome, descricao) VALUES (?, ?)",
                           (categoria.nome, categoria.descricao))
            conn.commit()
            cat_id = cursor.lastrowid
            return True, f"Categoria '{nome}' cadastrada com sucesso! ID: {cat_id}"
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro ao criar categoria: {str(e)}"

    def listar(self):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, descricao FROM categorias ORDER BY nome")
            categorias = cursor.fetchall()
            return categorias
        except Exception as e:
            print(f"Erro ao listar categorias: {str(e)}")
            return []

    def buscar_por_id(self, cat_id):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, descricao FROM categorias WHERE id = ?", (cat_id,))
            categoria = cursor.fetchone()
            return categoria
        except Exception as e:
            print(f"Erro ao buscar categoria: {str(e)}")
            return None

    def atualizar(self, cat_id, nome=None, descricao=None):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            campos = []
            params = []
            if nome:
                campos.append("nome = ?")
                params.append(nome)
            if descricao is not None:
                campos.append("descricao = ?")
                params.append(descricao)
            if not campos:
                return False, "Nenhum campo para atualizar"
            params.append(cat_id)
            cursor.execute(f"UPDATE categorias SET {', '.join(campos)} WHERE id = ?", params)
            conn.commit()
            return True, "Categoria atualizada com sucesso!"
        except Exception as e:
            return False, f"Erro ao atualizar categoria: {str(e)}"

    def excluir(self, cat_id):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM categorias WHERE id = ?", (cat_id,))
            conn.commit()
            return True, "Categoria excluída com sucesso!"
        except Exception as e:
            return False, f"Erro ao excluir categoria: {str(e)}"
