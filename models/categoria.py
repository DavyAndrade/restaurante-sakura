class Categoria:
    def __init__(self, nome, descricao='', id=None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.validar()

    def validar(self):
        if not self.nome:
            raise ValueError("Nome da categoria é obrigatório")

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
        }
