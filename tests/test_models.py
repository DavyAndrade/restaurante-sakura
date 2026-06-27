import sys, os, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
from models.usuario import Usuario
from models.mesa import Mesa
from models.categoria import Categoria
from models.item_cardapio import ItemCardapio
from models.insumo import Insumo
from models.pedido import Pedido
from models.item_pedido import ItemPedido
from models.conta import Conta
from models.item_insumo import ItemInsumo


class TestUsuario(unittest.TestCase):
    def test_criar_valido(self):
        u = Usuario('João', '111.111.111-11', 'joao', '123', 'garcom')
        self.assertEqual(u.nome, 'João')
        self.assertEqual(u.tipo, 'garcom')

    def test_tipo_invalido(self):
        with self.assertRaises(ValueError):
            Usuario('João', '111.111.111-11', 'joao', '123', 'piloto')

    def test_campo_obrigatorio(self):
        with self.assertRaises(ValueError):
            Usuario('', '111.111.111-11', 'joao', '123', 'garcom')


class TestMesa(unittest.TestCase):
    def test_criar_valido(self):
        m = Mesa(1, 4)
        self.assertEqual(m.status, 'livre')

    def test_capacidade_invalida(self):
        with self.assertRaises(ValueError):
            Mesa(1, 0)

    def test_status_invalido(self):
        with self.assertRaises(ValueError):
            Mesa(1, 4, status='inexistente')

    def test_to_dict(self):
        m = Mesa(5, 2, status='ocupada', id=3)
        d = m.to_dict()
        self.assertEqual(d['numero'], 5)
        self.assertEqual(d['status'], 'ocupada')


class TestCategoria(unittest.TestCase):
    def test_criar(self):
        c = Categoria('Bebidas')
        self.assertEqual(c.nome, 'Bebidas')

    def test_nome_obrigatorio(self):
        with self.assertRaises(ValueError):
            Categoria('')


class TestItemCardapio(unittest.TestCase):
    def test_criar_valido(self):
        item = ItemCardapio(1, 'Sushi de Salmão', 25.0)
        self.assertEqual(item.preco, 25.0)
        self.assertEqual(item.disponivel, 1)

    def test_preco_invalido(self):
        with self.assertRaises(ValueError):
            ItemCardapio(1, 'Sushi', 0)

    def test_sem_categoria(self):
        with self.assertRaises(ValueError):
            ItemCardapio(None, 'Sushi', 10)


class TestInsumo(unittest.TestCase):
    def test_criar(self):
        i = Insumo('Salmão', 10.0, 'kg')
        self.assertEqual(i.nome, 'Salmão')

    def test_nome_obrigatorio(self):
        with self.assertRaises(ValueError):
            Insumo('')


class TestPedido(unittest.TestCase):
    def test_criar_valido(self):
        p = Pedido(1, 1)
        self.assertEqual(p.status, 'pendente')

    def test_status_invalido(self):
        with self.assertRaises(ValueError):
            Pedido(1, 1, status='invalido')

    def test_mesa_obrigatoria(self):
        with self.assertRaises(ValueError):
            Pedido(None, 1)


class TestItemPedido(unittest.TestCase):
    def test_criar_valido(self):
        ip = ItemPedido(1, 1, 2, 25.0)
        self.assertEqual(ip.quantidade, 2)

    def test_quantidade_invalida(self):
        with self.assertRaises(ValueError):
            ItemPedido(1, 1, 0, 25.0)


class TestConta(unittest.TestCase):
    def test_criar_valido(self):
        c = Conta(1, 3, 100.0)
        self.assertEqual(c.status, 0)

    def test_valor_invalido(self):
        with self.assertRaises(ValueError):
            Conta(1, 3, -10)

    def test_metodo_invalido(self):
        with self.assertRaises(ValueError):
            Conta(1, 3, 100, metodo_pagamento='bitcoin')


class TestItemInsumo(unittest.TestCase):
    def test_criar_valido(self):
        ii = ItemInsumo(1, 1, 0.150)
        self.assertEqual(ii.qtd_porcao, 0.150)

    def test_qtd_invalida(self):
        with self.assertRaises(ValueError):
            ItemInsumo(1, 1, 0)


if __name__ == '__main__':
    unittest.main()
