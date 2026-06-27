from models.insumo import Insumo
from models.item_insumo import ItemInsumo
from database.db_manager import DatabaseManager

class InsumoController:
    def __init__(self):
        self.db = DatabaseManager()

    def criar(self, nome, qtd_atual=0.0, unidade='un'):
        try:
            insumo = Insumo(nome, qtd_atual, unidade)
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO insumos (nome, qtd_atual, unidade) VALUES (?, ?, ?)",
                           (insumo.nome, insumo.qtd_atual, insumo.unidade))
            conn.commit()
            insumo_id = cursor.lastrowid
            return True, f"Insumo '{nome}' cadastrado! ID: {insumo_id}"
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro ao criar insumo: {str(e)}"

    def listar(self):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, qtd_atual, unidade FROM insumos ORDER BY nome")
            insumos = cursor.fetchall()
            return insumos
        except Exception as e:
            print(f"Erro ao listar insumos: {str(e)}")
            return []

    def buscar_por_id(self, insumo_id):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, qtd_atual, unidade FROM insumos WHERE id = ?", (insumo_id,))
            insumo = cursor.fetchone()
            return insumo
        except Exception as e:
            print(f"Erro ao buscar insumo: {str(e)}")
            return None

    def ajustar_estoque(self, insumo_id, quantidade):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("UPDATE insumos SET qtd_atual = qtd_atual + ? WHERE id = ?",
                           (quantidade, insumo_id))
            conn.commit()
            return True, "Estoque ajustado com sucesso!"
        except Exception as e:
            return False, f"Erro ao ajustar estoque: {str(e)}"

    def baixar_estoque_por_pedido(self, pedido_id):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute('''SELECT ii.insumo_id, ii.qtd_porcao * ip.quantidade AS total_baixa
                FROM itens_pedido ip
                JOIN itens_insumo ii ON ip.item_id = ii.item_id
                WHERE ip.pedido_id = ?''', (pedido_id,))
            baixas = cursor.fetchall()
            for insumo_id, qtd in baixas:
                cursor.execute("UPDATE insumos SET qtd_atual = qtd_atual - ? WHERE id = ?",
                               (qtd, insumo_id))
            conn.commit()
            return True, f"Estoque baixado para {len(baixas)} insumo(s)"
        except Exception as e:
            return False, f"Erro ao baixar estoque: {str(e)}"

    def vincular_item(self, item_id, insumo_id, qtd_porcao):
        try:
            item_insumo = ItemInsumo(item_id, insumo_id, qtd_porcao)
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO itens_insumo (item_id, insumo_id, qtd_porcao) VALUES (?, ?, ?)",
                           (item_insumo.item_id, item_insumo.insumo_id, item_insumo.qtd_porcao))
            conn.commit()
            return True, "Insumo vinculado ao item com sucesso!"
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro ao vincular insumo: {str(e)}"

    def listar_insumos_do_item(self, item_id):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute('''SELECT ii.id, i.nome, i.unidade, ii.qtd_porcao
                FROM itens_insumo ii
                JOIN insumos i ON ii.insumo_id = i.id
                WHERE ii.item_id = ?''', (item_id,))
            itens = cursor.fetchall()
            return itens
        except Exception as e:
            print(f"Erro ao listar insumos do item: {str(e)}")
            return []

    def excluir(self, insumo_id):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM insumos WHERE id = ?", (insumo_id,))
            conn.commit()
            return True, "Insumo excluído com sucesso!"
        except Exception as e:
            return False, f"Erro ao excluir insumo: {str(e)}"
