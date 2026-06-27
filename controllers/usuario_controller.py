from models.usuario import Usuario
from database.db_manager import DatabaseManager

class UsuarioController:
    def __init__(self):
        self.db = DatabaseManager()

    def criar(self, nome, cpf, login, senha, tipo):
        try:
            usuario = Usuario(nome, cpf, login, senha, tipo)
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO usuarios (nome, cpf, login, senha, tipo)
                VALUES (?, ?, ?, ?, ?)''',
                (usuario.nome, usuario.cpf, usuario.login, usuario.senha, usuario.tipo))
            conn.commit()
            usuario_id = cursor.lastrowid
            return True, f"Usuário cadastrado com sucesso! ID: {usuario_id}"
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro ao criar usuário: {str(e)}"

    def listar(self, tipo=None):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            if tipo:
                cursor.execute("SELECT id, nome, cpf, login, tipo FROM usuarios WHERE tipo = ? ORDER BY nome", (tipo,))
            else:
                cursor.execute("SELECT id, nome, cpf, login, tipo FROM usuarios ORDER BY nome")
            usuarios = cursor.fetchall()
            return usuarios
        except Exception as e:
            print(f"Erro ao listar usuários: {str(e)}")
            return []

    def buscar_por_id(self, usuario_id):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, cpf, login, tipo FROM usuarios WHERE id = ?", (usuario_id,))
            usuario = cursor.fetchone()
            return usuario
        except Exception as e:
            print(f"Erro ao buscar usuário: {str(e)}")
            return None

    def autenticar(self, login, senha):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, tipo FROM usuarios WHERE login = ? AND senha = ?", (login, senha))
            usuario = cursor.fetchone()
            return usuario
        except Exception as e:
            print(f"Erro ao autenticar: {str(e)}")
            return None

    def atualizar(self, usuario_id, nome=None, cpf=None, login=None, senha=None, tipo=None):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            campos = []
            params = []
            if nome:
                campos.append("nome = ?")
                params.append(nome)
            if cpf:
                campos.append("cpf = ?")
                params.append(cpf)
            if login:
                campos.append("login = ?")
                params.append(login)
            if senha:
                campos.append("senha = ?")
                params.append(senha)
            if tipo:
                campos.append("tipo = ?")
                params.append(tipo)
            if not campos:
                return False, "Nenhum campo para atualizar"
            params.append(usuario_id)
            cursor.execute(f"UPDATE usuarios SET {', '.join(campos)} WHERE id = ?", params)
            conn.commit()
            return True, "Usuário atualizado com sucesso!"
        except Exception as e:
            return False, f"Erro ao atualizar usuário: {str(e)}"

    def excluir(self, usuario_id):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
            conn.commit()
            return True, "Usuário excluído com sucesso!"
        except Exception as e:
            return False, f"Erro ao excluir usuário: {str(e)}"
