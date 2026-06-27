import sys, os
sys.path.insert(0, os.path.dirname(__file__))

def executar_fallback_cli():
    print("Tkinter nao esta disponivel para abrir a interface grafica.")
    print("Instale/configure o Tkinter ou use o modo terminal. Exemplos:")
    print("  sudo apt install python3-tk")
    print("  sudo pacman -S tk")
    print("\nUsando modo terminal como fallback...\n")
    from views.cli import executar_cli
    executar_cli()

def main():
    from database.db_manager import DatabaseManager
    DatabaseManager()

    try:
        from views.login_view import LoginView
        from views.main_view import MainView

        def iniciar_sistema(usuario):
            app = MainView(usuario)
            app.iniciar()

        login = LoginView(on_login_success=iniciar_sistema)
        login.iniciar()

    except ImportError as e:
        msg = str(e)
        if 'tkinter' in msg.lower() or 'libtk' in msg:
            executar_fallback_cli()
        else:
            raise
    except Exception as e:
        if e.__class__.__name__ == 'TclError':
            executar_fallback_cli()
        else:
            raise

if __name__ == "__main__":
    main()
