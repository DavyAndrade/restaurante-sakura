class ItemPedido:
    def __init__(self, pedido_id, item_id, quantidade, preco_no_momento,
                 observacao='', id=None):
        self.id = id
        self.pedido_id = pedido_id
        self.item_id = item_id
        self.quantidade = quantidade
        self.preco_no_momento = preco_no_momento
        self.observacao = observacao
        self.validar()

    def validar(self):
        if not self.pedido_id:
            raise ValueError("Pedido é obrigatório")
        if not self.item_id:
            raise ValueError("Item do cardápio é obrigatório")
        if self.quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero")
        if self.preco_no_momento <= 0:
            raise ValueError("Preço deve ser maior que zero")

    def to_dict(self):
        return {
            'id': self.id,
            'pedido_id': self.pedido_id,
            'item_id': self.item_id,
            'quantidade': self.quantidade,
            'preco_no_momento': self.preco_no_momento,
            'observacao': self.observacao,
        }
