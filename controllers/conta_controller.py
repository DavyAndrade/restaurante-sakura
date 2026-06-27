from models.conta import Conta
from database.db_manager import DatabaseManager

class ContaController:
    def __init__(self):
        self.db = DatabaseManager()

    def abrir_conta(self, pedido_id, caixa_id):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT total FROM pedidos WHERE id = ?", (pedido_id,))
            resultado = cursor.fetchone()
            if not resultado:
                return False, "Pedido não encontrado"
            valor_total = resultado[0]
            conta = Conta(pedido_id, caixa_id, valor_total)
            cursor.execute('''INSERT INTO contas (pedido_id, caixa_id, valor_total)
                VALUES (?, ?, ?)''', (conta.pedido_id, conta.caixa_id, conta.valor_total))
            conn.commit()
            conta_id = cursor.lastrowid
            return True, f"Conta {conta_id} aberta! Valor: R$ {valor_total:.2f}"
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro ao abrir conta: {str(e)}"

    def processar_pagamento(self, conta_id, metodo):
        try:
            if metodo not in ('pix', 'cartao', 'dinheiro'):
                return False, "Método deve ser pix, cartao ou dinheiro"
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute('''UPDATE contas SET metodo_pagamento = ?, status = 1
                WHERE id = ?''', (metodo, conta_id))
            cursor.execute('''SELECT pedido_id, caixa_id FROM contas WHERE id = ?''', (conta_id,))
            resultado = cursor.fetchone()
            if resultado:
                cursor.execute('''UPDATE mesas SET status = 'livre'
                    WHERE id = (SELECT mesa_id FROM pedidos WHERE id = ?)''', (resultado[0],))
            conn.commit()
            if not resultado:
                return False, "Conta não encontrada"
            return True, f"Pagamento processado via {metodo}!"
        except Exception as e:
            return False, f"Erro ao processar pagamento: {str(e)}"

    def listar(self, status=None):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            query = '''SELECT c.id, c.valor_total, c.metodo_pagamento, c.status,
                              p.id AS pedido_id, m.numero AS mesa,
                              u.nome AS caixa
                       FROM contas c
                       JOIN pedidos p ON c.pedido_id = p.id
                       JOIN mesas m ON p.mesa_id = m.id
                       JOIN usuarios u ON c.caixa_id = u.id
                       WHERE 1=1'''
            params = []
            if status is not None:
                query += " AND c.status = ?"
                params.append(status)
            query += " ORDER BY c.id DESC"
            cursor.execute(query, params)
            contas = cursor.fetchall()
            return contas
        except Exception as e:
            print(f"Erro ao listar contas: {str(e)}")
            return []

    def buscar_por_id(self, conta_id):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute('''SELECT c.id, c.pedido_id, c.caixa_id, c.valor_total,
                                     c.metodo_pagamento, c.status
                FROM contas c WHERE c.id = ?''', (conta_id,))
            conta = cursor.fetchone()
            return conta
        except Exception as e:
            print(f"Erro ao buscar conta: {str(e)}")
            return None

    def buscar_por_pedido(self, pedido_id):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute('''SELECT id, pedido_id, caixa_id, valor_total,
                                     metodo_pagamento, status
                FROM contas WHERE pedido_id = ?''', (pedido_id,))
            conta = cursor.fetchone()
            return conta
        except Exception as e:
            print(f"Erro ao buscar conta por pedido: {str(e)}")
            return None

    def relatorio_vendas(self, periodo_inicio=None, periodo_fim=None):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            query = '''SELECT DATE(p.data_hora) AS dia,
                              COUNT(c.id) AS total_contas,
                              SUM(c.valor_total) AS faturamento,
                              c.metodo_pagamento
                       FROM contas c
                       JOIN pedidos p ON c.pedido_id = p.id
                       WHERE c.status = 1'''
            params = []
            if periodo_inicio:
                query += " AND p.data_hora >= ?"
                params.append(periodo_inicio)
            if periodo_fim:
                query += " AND p.data_hora <= ?"
                params.append(periodo_fim)
            query += " GROUP BY dia, c.metodo_pagamento ORDER BY dia DESC"
            cursor.execute(query, params)
            dados = cursor.fetchall()
            return dados
        except Exception as e:
            print(f"Erro ao gerar relatório: {str(e)}")
            return []
