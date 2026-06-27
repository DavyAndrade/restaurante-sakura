class ItemCardapio:
    def __init__(self, categoria_id, nome, preco, descricao='',
                 disponivel=1, ingredientes='', valor_nutricional='', id=None):
        self.id = id
        self.categoria_id = categoria_id
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.disponivel = disponivel
        self.ingredientes = ingredientes
        self.valor_nutricional = valor_nutricional
        self.validar()

    def validar(self):
        if not self.categoria_id:
            raise ValueError("Categoria é obrigatória")
        if not self.nome:
            raise ValueError("Nome do item é obrigatório")
        if self.preco <= 0:
            raise ValueError("Preço deve ser maior que zero")

    def to_dict(self):
        return {
            'id': self.id,
            'categoria_id': self.categoria_id,
            'nome': self.nome,
            'descricao': self.descricao,
            'preco': self.preco,
            'disponivel': self.disponivel,
            'ingredientes': self.ingredientes,
            'valor_nutricional': self.valor_nutricional,
        }
