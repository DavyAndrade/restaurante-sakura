class Mesa:
    def __init__(self, numero, capacidade, status='livre', id=None):
        self.id = id
        self.numero = numero
        self.capacidade = capacidade
        self.status = status
        self.validar()

    def validar(self):
        if not self.numero or self.numero <= 0:
            raise ValueError("Número da mesa deve ser positivo")
        if self.capacidade <= 0:
            raise ValueError("Capacidade deve ser maior que zero")
        if self.status not in ('livre', 'ocupada', 'reservada'):
            raise ValueError("Status deve ser livre, ocupada ou reservada")

    def to_dict(self):
        return {
            'id': self.id,
            'numero': self.numero,
            'capacidade': self.capacidade,
            'status': self.status,
        }
