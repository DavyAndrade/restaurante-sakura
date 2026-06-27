from datetime import datetime

STATUS_VALIDOS = ('pendente', 'aguardando_validacao', 'em_preparo', 'pronto', 'cancelado')

class Pedido:
    def __init__(self, mesa_id, garcom_id, status='pendente', total=0.0,
                 data_hora=None, id=None):
        self.id = id
        self.mesa_id = mesa_id
        self.garcom_id = garcom_id
        self.status = status
        self.total = total
        self.data_hora = data_hora or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.validar()

    def validar(self):
        if not self.mesa_id:
            raise ValueError("Mesa é obrigatória")
        if not self.garcom_id:
            raise ValueError("Garçom é obrigatório")
        if self.status not in STATUS_VALIDOS:
            raise ValueError(f"Status deve ser um de: {', '.join(STATUS_VALIDOS)}")
        if self.total < 0:
            raise ValueError("Total não pode ser negativo")

    def to_dict(self):
        return {
            'id': self.id,
            'mesa_id': self.mesa_id,
            'garcom_id': self.garcom_id,
            'data_hora': self.data_hora,
            'status': self.status,
            'total': self.total,
        }
