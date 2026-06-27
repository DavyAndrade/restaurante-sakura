class Insumo:
    def __init__(self, nome, qtd_atual=0.0, unidade='un', id=None):
        self.id = id
        self.nome = nome
        self.qtd_atual = qtd_atual
        self.unidade = unidade
        self.validar()

    def validar(self):
        if not self.nome:
            raise ValueError("Nome do insumo é obrigatório")
        if not self.unidade:
            raise ValueError("Unidade é obrigatória")

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'qtd_atual': self.qtd_atual,
            'unidade': self.unidade,
        }
