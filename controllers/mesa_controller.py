from models.mesa import Mesa
from database.db_manager import DatabaseManager

class MesaController:
    def __init__(self):
        self.db = DatabaseManager()

    def criar(self, numero, capacidade):
        try:
            mesa = Mesa(numero, capacidade)
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO mesas (numero, capacidade) VALUES (?, ?)",
                           (mesa.numero, mesa.capacidade))
            conn.commit()
            mesa_id = cursor.lastrowid
            return True, f"Mesa {numero} cadastrada com sucesso! ID: {mesa_id}"
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro ao criar mesa: {str(e)}"

    def listar(self, status=None):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            if status:
                cursor.execute("SELECT id, numero, capacidade, status FROM mesas WHERE status = ? ORDER BY numero", (status,))
            else:
                cursor.execute("SELECT id, numero, capacidade, status FROM mesas ORDER BY numero")
            mesas = cursor.fetchall()
            return mesas
        except Exception as e:
            print(f"Erro ao listar mesas: {str(e)}")
            return []

    def buscar_por_id(self, mesa_id):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, numero, capacidade, status FROM mesas WHERE id = ?", (mesa_id,))
            mesa = cursor.fetchone()
            return mesa
        except Exception as e:
            print(f"Erro ao buscar mesa: {str(e)}")
            return None

    def abrir_mesa(self, mesa_id):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT status FROM mesas WHERE id = ?", (mesa_id,))
            resultado = cursor.fetchone()
            if not resultado:
                return False, "Mesa não encontrada"
            if resultado[0] != 'livre':
                return False, f"Mesa não está livre (status: {resultado[0]})"
            cursor.execute("UPDATE mesas SET status = 'ocupada' WHERE id = ?", (mesa_id,))
            conn.commit()
            return True, "Mesa aberta com sucesso!"
        except Exception as e:
            return False, f"Erro ao abrir mesa: {str(e)}"

    def liberar_mesa(self, mesa_id):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("UPDATE mesas SET status = 'livre' WHERE id = ?", (mesa_id,))
            conn.commit()
            return True, "Mesa liberada com sucesso!"
        except Exception as e:
            return False, f"Erro ao liberar mesa: {str(e)}"

    def atualizar(self, mesa_id, numero=None, capacidade=None):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            campos = []
            params = []
            if numero:
                campos.append("numero = ?")
                params.append(numero)
            if capacidade:
                campos.append("capacidade = ?")
                params.append(capacidade)
            if not campos:
                return False, "Nenhum campo para atualizar"
            params.append(mesa_id)
            cursor.execute(f"UPDATE mesas SET {', '.join(campos)} WHERE id = ?", params)
            conn.commit()
            return True, "Mesa atualizada com sucesso!"
        except Exception as e:
            return False, f"Erro ao atualizar mesa: {str(e)}"

    def excluir(self, mesa_id):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM mesas WHERE id = ?", (mesa_id,))
            conn.commit()
            return True, "Mesa excluída com sucesso!"
        except Exception as e:
            return False, f"Erro ao excluir mesa: {str(e)}"
