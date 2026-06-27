from models.pedido import Pedido
from models.item_pedido import ItemPedido
from database.db_manager import DatabaseManager

class PedidoController:
    def __init__(self):
        self.db = DatabaseManager()

    def criar(self, mesa_id, garcom_id):
        try:
            pedido = Pedido(mesa_id, garcom_id)
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO pedidos (mesa_id, garcom_id, status)
                VALUES (?, ?, ?)''', (pedido.mesa_id, pedido.garcom_id, pedido.status))
            conn.commit()
            pedido_id = cursor.lastrowid
            return True, f"Pedido {pedido_id} criado com sucesso!", pedido_id
        except ValueError as e:
            return False, str(e), None
        except Exception as e:
            return False, f"Erro ao criar pedido: {str(e)}", None

    def adicionar_item(self, pedido_id, item_id, quantidade, preco_no_momento, observacao=''):
        try:
            item_pedido = ItemPedido(pedido_id, item_id, quantidade, preco_no_momento, observacao)
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO itens_pedido
                (pedido_id, item_id, quantidade, preco_no_momento, observacao)
                VALUES (?, ?, ?, ?, ?)''',
                           (item_pedido.pedido_id, item_pedido.item_id,
                            item_pedido.quantidade, item_pedido.preco_no_momento,
                            item_pedido.observacao))
            conn.commit()
            cursor.execute('''UPDATE pedidos SET total = (
                SELECT COALESCE(SUM(ip.quantidade * ip.preco_no_momento), 0)
                FROM itens_pedido ip WHERE ip.pedido_id = ?) WHERE id = ?''',
                           (pedido_id, pedido_id))
            conn.commit()
            return True, "Item adicionado ao pedido!"
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro ao adicionar item: {str(e)}"

    def listar(self, status=None, mesa_id=None):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            query = '''SELECT p.id, p.data_hora, p.status, p.total,
                              m.numero AS mesa,
                              u.nome AS garcom
                       FROM pedidos p
                       JOIN mesas m ON p.mesa_id = m.id
                       JOIN usuarios u ON p.garcom_id = u.id
                       WHERE 1=1'''
            params = []
            if status:
                query += " AND p.status = ?"
                params.append(status)
            if mesa_id:
                query += " AND p.mesa_id = ?"
                params.append(mesa_id)
            query += " ORDER BY p.data_hora DESC"
            cursor.execute(query, params)
            pedidos = cursor.fetchall()
            return pedidos
        except Exception as e:
            print(f"Erro ao listar pedidos: {str(e)}")
            return []

    def listar_itens(self, pedido_id):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute('''SELECT ip.id, ic.nome, ip.quantidade,
                                     ip.preco_no_momento, ip.observacao
                FROM itens_pedido ip
                JOIN itens_cardapio ic ON ip.item_id = ic.id
                WHERE ip.pedido_id = ?''', (pedido_id,))
            itens = cursor.fetchall()
            return itens
        except Exception as e:
            print(f"Erro ao listar itens do pedido: {str(e)}")
            return []

    def buscar_por_id(self, pedido_id):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute('''SELECT p.id, p.mesa_id, p.garcom_id, p.data_hora,
                                     p.status, p.total
                FROM pedidos p WHERE p.id = ?''', (pedido_id,))
            pedido = cursor.fetchone()
            return pedido
        except Exception as e:
            print(f"Erro ao buscar pedido: {str(e)}")
            return None

    def atualizar_status(self, pedido_id, novo_status):
        if novo_status not in ('pendente', 'aguardando_validacao', 'em_preparo', 'pronto', 'cancelado'):
            return False, f"Status inválido: {novo_status}"
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("UPDATE pedidos SET status = ? WHERE id = ?", (novo_status, pedido_id))
            conn.commit()
            return True, f"Pedido {pedido_id} agora está '{novo_status}'"
        except Exception as e:
            return False, f"Erro ao atualizar status: {str(e)}"

    def validar_pedido(self, pedido_id):
        return self.atualizar_status(pedido_id, 'aguardando_validacao')

    def iniciar_preparo(self, pedido_id):
        return self.atualizar_status(pedido_id, 'em_preparo')

    def finalizar_preparo(self, pedido_id):
        return self.atualizar_status(pedido_id, 'pronto')

    def cancelar(self, pedido_id):
        return self.atualizar_status(pedido_id, 'cancelado')

    def excluir(self, pedido_id):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pedidos WHERE id = ?", (pedido_id,))
            conn.commit()
            return True, "Pedido excluído com sucesso!"
        except Exception as e:
            return False, f"Erro ao excluir pedido: {str(e)}"
