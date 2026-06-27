from controllers.usuario_controller import UsuarioController
from controllers.mesa_controller import MesaController
from controllers.categoria_controller import CategoriaController
from controllers.item_cardapio_controller import ItemCardapioController
from controllers.insumo_controller import InsumoController
from controllers.pedido_controller import PedidoController
from controllers.conta_controller import ContaController
from views.cli import USUARIO_LOGADO, aguardar, cabecalho

def menu_usuarios():
    ctrl = UsuarioController()
    while True:
        cabecalho("USUARIOS (FUNCIONARIOS)")
        print("1. Cadastrar usuario")
        print("2. Listar todos")
        print("3. Listar garcons")
        print("4. Listar sushimans")
        print("5. Listar caixas")
        print("6. Listar gerentes")
        print("7. Excluir usuario")
        print("0. Voltar")
        op = input("\nOpcao: ")
        if op == '1':
            nome = input("Nome: ")
            cpf = input("CPF: ")
            login = input("Login: ")
            senha = input("Senha: ")
            print("Tipos: garcom, sushiman, caixa, gerente")
            tipo = input("Tipo: ")
            sucesso, msg = ctrl.criar(nome, cpf, login, senha, tipo)
            print(msg)
        elif op == '2':
            for u in ctrl.listar():
                print(f"ID: {u[0]} | {u[1]} | {u[2]} | {u[3]} | {u[4]}")
            if not ctrl.listar(): print("Nenhum usuario.")
        elif op in ('3','4','5','6'):
            m = {'3':'garcom','4':'sushiman','5':'caixa','6':'gerente'}
            for u in ctrl.listar(tipo=m[op]):
                print(f"ID: {u[0]} | {u[1]} | {u[3]}")
            if not ctrl.listar(tipo=m[op]): print("Nenhum encontrado.")
        elif op == '7':
            uid = int(input("ID do usuario: "))
            if input(f"Excluir ID {uid}? (s/N): ").lower() == 's':
                print(ctrl.excluir(uid)[1])
        elif op == '0': break
        aguardar()

def menu_mesas():
    ctrl = MesaController()
    while True:
        cabecalho("MESAS")
        print("1. Cadastrar mesa")
        print("2. Listar todas")
        print("3. Mesas livres")
        print("4. Abrir mesa")
        print("5. Liberar mesa")
        print("6. Excluir mesa")
        print("0. Voltar")
        op = input("\nOpcao: ")
        if op == '1':
            n = int(input("Numero: "))
            c = int(input("Capacidade: "))
            print(ctrl.criar(n, c)[1])
        elif op in ('2','3'):
            st = {'2':None,'3':'livre'}[op]
            for m in ctrl.listar(status=st):
                print(f"ID: {m[0]} | N{m[1]} | Cap:{m[2]} | {m[3]}")
            if not ctrl.listar(status=st): print("Nenhuma mesa.")
        elif op == '4':
            mid = int(input("ID da mesa: "))
            print(ctrl.abrir_mesa(mid)[1])
        elif op == '5':
            mid = int(input("ID da mesa: "))
            print(ctrl.liberar_mesa(mid)[1])
        elif op == '6':
            mid = int(input("ID da mesa: "))
            if input(f"Excluir mesa ID {mid}? (s/N): ").lower() == 's':
                print(ctrl.excluir(mid)[1])
        elif op == '0': break
        aguardar()

def menu_categorias():
    ctrl = CategoriaController()
    while True:
        cabecalho("CATEGORIAS")
        print("1. Cadastrar")
        print("2. Listar")
        print("3. Excluir")
        print("0. Voltar")
        op = input("\nOpcao: ")
        if op == '1':
            n = input("Nome: ")
            d = input("Descricao: ")
            print(ctrl.criar(n, d)[1])
        elif op == '2':
            for c in ctrl.listar():
                print(f"ID: {c[0]} | {c[1]} | {c[2]}")
            if not ctrl.listar(): print("Nenhuma categoria.")
        elif op == '3':
            cid = int(input("ID: "))
            if input(f"Excluir ID {cid}? (s/N): ").lower() == 's':
                print(ctrl.excluir(cid)[1])
        elif op == '0': break
        aguardar()

def menu_cardapio():
    ctrl = ItemCardapioController()
    while True:
        cabecalho("CARDAPIO")
        print("1. Cadastrar item")
        print("2. Listar tudo")
        print("3. Disponiveis")
        print("4. Alternar disponibilidade")
        print("5. Excluir")
        print("0. Voltar")
        op = input("\nOpcao: ")
        if op == '1':
            cat = int(input("ID categoria: "))
            nome = input("Nome: ")
            preco = float(input("Preco: "))
            print(ctrl.criar(cat, nome, preco, input("Desc: "), 1, input("Ingredientes: "), input("V.Nutri: "))[1])
        elif op == '2':
            for i in ctrl.listar():
                print(f"ID:{i[0]} | {i[1]} | R${i[3]:.2f} | {'OK' if i[4] else 'OFF'} | {i[7]}")
            if not ctrl.listar(): print("Nenhum item.")
        elif op == '3':
            for i in ctrl.listar(apenas_disponiveis=True):
                print(f"ID:{i[0]} | {i[1]} | R${i[3]:.2f} | {i[7]}")
            if not ctrl.listar(apenas_disponiveis=True): print("Nenhum item disponivel.")
        elif op == '4':
            iid = int(input("ID do item: "))
            print(ctrl.alternar_disponibilidade(iid)[1])
        elif op == '5':
            iid = int(input("ID do item: "))
            if input(f"Excluir ID {iid}? (s/N): ").lower() == 's':
                print(ctrl.excluir(iid)[1])
        elif op == '0': break
        aguardar()

def menu_insumos():
    ctrl = InsumoController()
    while True:
        cabecalho("INSUMOS")
        print("1. Cadastrar")
        print("2. Listar")
        print("3. Ajustar estoque")
        print("4. Vincular a item")
        print("5. Ver insumos de item")
        print("0. Voltar")
        op = input("\nOpcao: ")
        if op == '1':
            n = input("Nome: ")
            q = float(input("Qtd atual: ") or '0')
            u = input("Unidade (kg,g,un,l,ml): ")
            print(ctrl.criar(n, q, u)[1])
        elif op == '2':
            for i in ctrl.listar():
                print(f"ID:{i[0]} | {i[1]} | {i[2]} {i[3]}")
            if not ctrl.listar(): print("Nenhum insumo.")
        elif op == '3':
            iid = int(input("ID insumo: "))
            q = float(input("Qtd (+/-): "))
            print(ctrl.ajustar_estoque(iid, q)[1])
        elif op == '4':
            it = int(input("ID item cardapio: "))
            ins = int(input("ID insumo: "))
            q = float(input("Qtd por porcao: "))
            print(ctrl.vincular_item(it, ins, q)[1])
        elif op == '5':
            it = int(input("ID item cardapio: "))
            for i in ctrl.listar_insumos_do_item(it):
                print(f"{i[1]} - {i[2]} ({i[3]:.2f} por porcao)")
            if not ctrl.listar_insumos_do_item(it): print("Nenhum vinculo.")
        elif op == '0': break
        aguardar()

def menu_pedidos():
    ctrl = PedidoController()
    while True:
        cabecalho("PEDIDOS")
        print("1. Novo pedido")
        print("2. Adicionar item")
        print("3. Listar pendentes")
        print("4. Listar em producao")
        print("5. Validar pedido")
        print("6. Iniciar preparo")
        print("7. Finalizar preparo")
        print("8. Cancelar")
        print("0. Voltar")
        op = input("\nOpcao: ")
        if op == '1':
            m = int(input("ID mesa: "))
            s, msg, pid = ctrl.criar(m, USUARIO_LOGADO[0])
            print(msg)
        elif op == '2':
            pid = int(input("ID pedido: "))
            item = int(input("ID item cardapio: "))
            q = int(input("Quantidade: "))
            p = float(input("Preco unit: "))
            o = input("Observacao: ")
            print(ctrl.adicionar_item(pid, item, q, p, o)[1])
        elif op == '3':
            for p in ctrl.listar(status='pendente'):
                print(f"ID:{p[0]} | Mesa:{p[4]} | {p[2]} | R${p[3]:.2f}")
            if not ctrl.listar(status='pendente'): print("Nenhum pedido pendente.")
        elif op == '4':
            for p in ctrl.listar(status='aguardando_validacao') + ctrl.listar(status='em_preparo'):
                print(f"ID:{p[0]} | Mesa:{p[4]} | {p[2]}")
            if not ctrl.listar(status='aguardando_validacao') and not ctrl.listar(status='em_preparo'):
                print("Nenhum pedido em producao.")
        elif op in ('5','6','7','8'):
            pid = int(input("ID pedido: "))
            fn = {'5':ctrl.validar_pedido,'6':ctrl.iniciar_preparo,'7':ctrl.finalizar_preparo,'8':ctrl.cancelar}
            print(fn[op](pid)[1])
        elif op == '0': break
        aguardar()

def menu_contas():
    ctrl = ContaController()
    while True:
        cabecalho("CONTAS")
        print("1. Abrir conta")
        print("2. Processar pagamento")
        print("3. Contas abertas")
        print("4. Contas pagas")
        print("5. Relatorio de vendas")
        print("0. Voltar")
        op = input("\nOpcao: ")
        if op == '1':
            pid = int(input("ID pedido: "))
            print(ctrl.abrir_conta(pid, USUARIO_LOGADO[0])[1])
        elif op == '2':
            cid = int(input("ID conta: "))
            print("Métodos: pix, cartao, dinheiro")
            m = input("Metodo: ")
            print(ctrl.processar_pagamento(cid, m)[1])
        elif op == '3':
            for c in ctrl.listar(status=0):
                print(f"ID:{c[0]} | Mesa:{c[5]} | R${c[1]:.2f}")
            if not ctrl.listar(status=0): print("Nenhuma conta aberta.")
        elif op == '4':
            for c in ctrl.listar(status=1):
                print(f"ID:{c[0]} | Mesa:{c[5]} | R${c[1]:.2f} | {c[2]}")
            if not ctrl.listar(status=1): print("Nenhuma conta paga.")
        elif op == '5':
            ini = input("Data inicio (YYYY-MM-DD, vazio=td): ") or None
            fim = input("Data fim (YYYY-MM-DD, vazio=td): ") or None
            total = 0
            for d in ctrl.relatorio_vendas(ini, fim):
                print(f"{d[0]} | {d[3] or '-'} | {d[1]} conta(s) | R$ {d[2]:.2f}")
                total += d[2]
            print(f"\nTotal: R$ {total:.2f}")
            if not ctrl.relatorio_vendas(ini, fim): print("Nenhum dado.")
        elif op == '0': break
        aguardar()
