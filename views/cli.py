import sys

def limpar():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def aguardar():
    input("\nPressione Enter para continuar...")

def cabecalho(titulo):
    print(f"\n{'='*50}")
    print(f"  {titulo}")
    print(f"{'='*50}")

USUARIO_LOGADO = None

def executar_cli():
    from database.db_manager import DatabaseManager
    from controllers.usuario_controller import UsuarioController

    db = DatabaseManager()
    uc = UsuarioController()

    global USUARIO_LOGADO

    print(f"\n{'='*50}")
    print(f"  SAKURA MANAGEMENT SYSTEM (CLI)")
    print(f"  Restaurante Sakura")
    print(f"{'='*50}")
    print("  Login: admin / 123\n")

    while True:
        login = input("Login: ")
        senha = input("Senha: ")
        USUARIO_LOGADO = uc.autenticar(login, senha)
        if USUARIO_LOGADO:
            print(f"Bem-vindo, {USUARIO_LOGADO[1]}!")
            break
        print("Login ou senha invalidos!")

    from views.main_menu import menu_usuarios, menu_mesas, menu_categorias, menu_cardapio, menu_insumos, menu_pedidos, menu_contas

    while True:
        print(f"\n{'='*50}")
        print(f"  SAKURA MANAGEMENT SYSTEM  |  {USUARIO_LOGADO[1]} ({USUARIO_LOGADO[2]})")
        print(f"{'='*50}")
        print("  1. Usuarios (Funcionarios)")
        print("  2. Mesas")
        print("  3. Categorias")
        print("  4. Cardapio (Itens)")
        print("  5. Insumos e Estoque")
        print("  6. Pedidos")
        print("  7. Contas e Pagamentos")
        print("  0. Sair")
        print(f"{'='*50}")

        op = input("\nOpcao: ")

        if op == '1': menu_usuarios()
        elif op == '2': menu_mesas()
        elif op == '3': menu_categorias()
        elif op == '4': menu_cardapio()
        elif op == '5': menu_insumos()
        elif op == '6': menu_pedidos()
        elif op == '7': menu_contas()
        elif op == '0':
            print("\nEncerrando...")
            break
        else:
            print("Opcao invalida!")
            aguardar()
