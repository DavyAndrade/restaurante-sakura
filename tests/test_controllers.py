import sys, os, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
from database.db_manager import DatabaseManager
from controllers.usuario_controller import UsuarioController
from controllers.mesa_controller import MesaController
from controllers.categoria_controller import CategoriaController
from controllers.item_cardapio_controller import ItemCardapioController
from controllers.insumo_controller import InsumoController
from controllers.pedido_controller import PedidoController
from controllers.conta_controller import ContaController


class BaseTest(unittest.TestCase):
    def setUp(self):
        if DatabaseManager._instancia and DatabaseManager._instancia._conexao:
            DatabaseManager._instancia.fechar()
        DatabaseManager._instancia = None
        self.db_path = tempfile.mktemp(suffix='.db')
        self.db = DatabaseManager(self.db_path)

    def tearDown(self):
        if hasattr(self, 'db'):
            self.db.fechar()
        for path in (self.db_path, self.db_path + '-wal', self.db_path + '-shm'):
            for _ in range(3):
                try:
                    if os.path.exists(path):
                        os.remove(path)
                    break
                except PermissionError:
                    import time
                    time.sleep(0.1)


class TestUsuarioController(BaseTest):
    def setUp(self):
        super().setUp()
        self.ctrl = UsuarioController()
        self.ctrl.db = self.db

    def test_criar_usuario(self):
        sucesso, msg = self.ctrl.criar('Carlos', '111.111.111-11', 'carlos', '123', 'garcom')
        self.assertTrue(sucesso)
        self.assertIn('sucesso', msg.lower())

    def test_criar_duplicado(self):
        self.ctrl.criar('A', '111.111.111-11', 'a', '1', 'garcom')
        sucesso, msg = self.ctrl.criar('B', '111.111.111-11', 'b', '2', 'garcom')
        self.assertFalse(sucesso)

    def test_listar_usuarios(self):
        self.ctrl.criar('Ana', '222.222.222-22', 'ana', '123', 'caixa')
        usuarios = self.ctrl.listar()
        self.assertGreater(len(usuarios), 0)

    def test_listar_por_tipo(self):
        self.ctrl.criar('Kenji', '333.333.333-33', 'kenji', '123', 'sushiman')
        sushimans = self.ctrl.listar(tipo='sushiman')
        self.assertTrue(all(u[4] == 'sushiman' for u in sushimans))

    def test_autenticar(self):
        self.ctrl.criar('Log', '444.444.444-44', 'log', 'senha', 'gerente')
        usuario = self.ctrl.autenticar('log', 'senha')
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario[2], 'gerente')

    def test_autenticar_invalido(self):
        usuario = self.ctrl.autenticar('naoexiste', 'x')
        self.assertIsNone(usuario)


class TestMesaController(BaseTest):
    def setUp(self):
        super().setUp()
        self.ctrl = MesaController()
        self.ctrl.db = self.db

    def test_criar_mesa(self):
        sucesso, msg = self.ctrl.criar(1, 4)
        self.assertTrue(sucesso)

    def test_listar_mesas(self):
        self.ctrl.criar(10, 2)
        mesas = self.ctrl.listar()
        self.assertGreater(len(mesas), 0)

    def test_abrir_mesa(self):
        self.ctrl.criar(5, 4)
        sucesso, msg = self.ctrl.abrir_mesa(1)
        self.assertTrue(sucesso)
        mesa = self.ctrl.buscar_por_id(1)
        self.assertEqual(mesa[3], 'ocupada')

    def test_abrir_mesa_ocupada(self):
        self.ctrl.criar(6, 4)
        self.ctrl.abrir_mesa(2)
        sucesso, msg = self.ctrl.abrir_mesa(2)
        self.assertFalse(sucesso)

    def test_liberar_mesa(self):
        self.ctrl.criar(7, 4)
        self.ctrl.abrir_mesa(1)
        self.ctrl.liberar_mesa(1)
        mesa = self.ctrl.buscar_por_id(1)
        self.assertEqual(mesa[3], 'livre')


class TestCategoriaController(BaseTest):
    def setUp(self):
        super().setUp()
        self.ctrl = CategoriaController()
        self.ctrl.db = self.db

    def test_criar_categoria(self):
        sucesso, msg = self.ctrl.criar('Teste')
        self.assertTrue(sucesso)

    def test_listar_categorias(self):
        cats = self.ctrl.listar()
        self.assertIsInstance(cats, list)


class TestItemCardapioController(BaseTest):
    def setUp(self):
        super().setUp()
        self.cat_ctrl = CategoriaController()
        self.cat_ctrl.db = self.db
        self.cat_ctrl.criar('Pizzas')
        self.ctrl = ItemCardapioController()
        self.ctrl.db = self.db

    def test_criar_item(self):
        sucesso, msg = self.ctrl.criar(1, 'Pizza Margherita', 35.0)
        self.assertTrue(sucesso)

    def test_listar_itens(self):
        self.ctrl.criar(1, 'Pizza Calabresa', 38.0)
        itens = self.ctrl.listar()
        self.assertGreater(len(itens), 0)

    def test_alternar_disponibilidade(self):
        self.ctrl.criar(1, 'Item Teste', 10.0)
        sucesso, msg = self.ctrl.alternar_disponibilidade(1)
        self.assertTrue(sucesso)


class TestPedidoController(BaseTest):
    def setUp(self):
        super().setUp()
        self.uc = UsuarioController()
        self.uc.db = self.db
        self.uc.criar('Garçom', '555.555.555-55', 'g1', '123', 'garcom')
        self.mc = MesaController()
        self.mc.db = self.db
        self.mc.criar(1, 4)
        self.ctrl = PedidoController()
        self.ctrl.db = self.db

    def test_criar_pedido(self):
        self.mc.abrir_mesa(1)
        sucesso, msg, pid = self.ctrl.criar(1, 1)
        self.assertTrue(sucesso)
        self.assertIsNotNone(pid)

    def test_adicionar_item_ao_pedido(self):
        cc = CategoriaController()
        cc.db = self.db
        cc.criar('Bebidas')
        ic = ItemCardapioController()
        ic.db = self.db
        ic.criar(1, 'Suco', 8.0)
        self.mc.abrir_mesa(1)
        s, _, pid = self.ctrl.criar(1, 1)
        sucesso, msg = self.ctrl.adicionar_item(pid, 1, 2, 8.0)
        self.assertTrue(sucesso)
        itens = self.ctrl.listar_itens(pid)
        self.assertEqual(len(itens), 1)

    def test_transicoes_status(self):
        self.mc.abrir_mesa(1)
        _, _, pid = self.ctrl.criar(1, 1)
        self.assertTrue(self.ctrl.validar_pedido(pid)[0])
        self.assertTrue(self.ctrl.iniciar_preparo(pid)[0])
        self.assertTrue(self.ctrl.finalizar_preparo(pid)[0])

    def test_cancelar_pedido(self):
        self.mc.abrir_mesa(1)
        _, _, pid = self.ctrl.criar(1, 1)
        sucesso, msg = self.ctrl.cancelar(pid)
        self.assertTrue(sucesso)
        pedido = self.ctrl.buscar_por_id(pid)
        self.assertEqual(pedido[4], 'cancelado')


class TestContaController(BaseTest):
    def setUp(self):
        super().setUp()
        self.uc = UsuarioController()
        self.uc.db = self.db
        self.uc.criar('Garçom', '666.666.666-66', 'g2', '123', 'garcom')
        self.uc.criar('Caixa', '777.777.777-77', 'cx', '123', 'caixa')
        self.mc = MesaController()
        self.mc.db = self.db
        self.mc.criar(1, 4)
        self.mc.abrir_mesa(1)
        self.pc = PedidoController()
        self.pc.db = self.db
        _, _, self.pid = self.pc.criar(1, 1)
        self.ic = ItemCardapioController()
        self.ic.db = self.db
        self.ic.criar(1, 'Suco', 8.0)
        self.pc.adicionar_item(self.pid, 1, 2, 8.0)
        self.ctrl = ContaController()
        self.ctrl.db = self.db

    def test_abrir_conta(self):
        sucesso, msg = self.ctrl.abrir_conta(self.pid, 2)
        self.assertTrue(sucesso)
        self.assertIn('conta', msg.lower())

    def test_processar_pagamento(self):
        self.ctrl.abrir_conta(self.pid, 2)
        sucesso, msg = self.ctrl.processar_pagamento(1, 'pix')
        self.assertTrue(sucesso)

    def test_metodo_invalido(self):
        self.ctrl.abrir_conta(self.pid, 2)
        sucesso, msg = self.ctrl.processar_pagamento(1, 'invalido')
        self.assertFalse(sucesso)

    def test_relatorio_vendas(self):
        self.ctrl.abrir_conta(self.pid, 2)
        self.ctrl.processar_pagamento(1, 'dinheiro')
        dados = self.ctrl.relatorio_vendas()
        self.assertGreater(len(dados), 0)


if __name__ == '__main__':
    unittest.main()
