class ItemInsumo:
    def __init__(self, item_id, insumo_id, qtd_porcao, id=None):
        self.id = id
        self.item_id = item_id
        self.insumo_id = insumo_id
        self.qtd_porcao = qtd_porcao
        self.validar()

    def validar(self):
        if not self.item_id:
            raise ValueError("Item do cardápio é obrigatório")
        if not self.insumo_id:
            raise ValueError("Insumo é obrigatório")
        if self.qtd_porcao <= 0:
            raise ValueError("Quantidade por porção deve ser maior que zero")

    def to_dict(self):
        return {
            'id': self.id,
            'item_id': self.item_id,
            'insumo_id': self.insumo_id,
            'qtd_porcao': self.qtd_porcao,
        }
