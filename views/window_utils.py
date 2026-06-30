import tkinter as tk


def ativar_modal(janela, parent):
    janela.transient(parent)

    def aplicar_grab():
        try:
            if janela.winfo_exists():
                janela.lift(parent)
                janela.focus_force()
                janela.grab_set()
        except tk.TclError:
            janela.after(50, aplicar_grab)

    janela.after_idle(aplicar_grab)
