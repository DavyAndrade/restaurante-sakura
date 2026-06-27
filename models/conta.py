METODOS_PAGAMENTO = ('pix', 'cartao', 'dinheiro')

class Conta:
    def __init__(self, pedido_id, caixa_id, valor_total,
                 metodo_pagamento=None, status=0, id=None):
        self.id = id
        self.pedido_id = pedido_id
        self.caixa_id = caixa_id
        self.valor_total = valor_total
        self.metodo_pagamento = metodo_pagamento
        self.status = status
        self.validar()

    def validar(self):
        if not self.pedido_id:
            raise ValueError("Pedido é obrigatório")
        if not self.caixa_id:
            raise ValueError("Caixa é obrigatório")
        if self.valor_total <= 0:
            raise ValueError("Valor total deve ser maior que zero")
        if self.metodo_pagamento and self.metodo_pagamento not in METODOS_PAGAMENTO:
            raise ValueError(f"Método deve ser um de: {', '.join(METODOS_PAGAMENTO)}")

    def to_dict(self):
        return {
            'id': self.id,
            'pedido_id': self.pedido_id,
            'caixa_id': self.caixa_id,
            'valor_total': self.valor_total,
            'metodo_pagamento': self.metodo_pagamento,
            'status': self.status,
        }
