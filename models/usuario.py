class Usuario:
    def __init__(self, nome, cpf, login, senha, tipo, id=None):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.login = login
        self.senha = senha
        self.tipo = tipo
        self.validar()

    def validar(self):
        if not self.nome:
            raise ValueError("Nome é obrigatório")
        if not self.cpf:
            raise ValueError("CPF é obrigatório")
        if not self.login:
            raise ValueError("Login é obrigatório")
        if not self.senha:
            raise ValueError("Senha é obrigatória")
        if self.tipo not in ('garcom', 'sushiman', 'caixa', 'gerente'):
            raise ValueError("Tipo deve ser garcom, sushiman, caixa ou gerente")

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'login': self.login,
            'tipo': self.tipo,
        }
