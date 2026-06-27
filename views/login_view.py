import tkinter as tk
from tkinter import messagebox
from controllers.usuario_controller import UsuarioController

USUARIO_LOGADO = None

class LoginView:
    def __init__(self, on_login_success):
        self.on_login_success = on_login_success
        self.ctrl = UsuarioController()
        self.janela = tk.Tk()
        self.janela.title('Sakura Management System - Login')
        self.janela.geometry('400x250')
        self.janela.configure(background='#2c3e50')
        self.janela.resizable(False, False)
        self._construir()

    def _construir(self):
        tk.Label(self.janela, text='Sakura Management System',
                 font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white').pack(pady=20)
        tk.Label(self.janela, text='Restaurante Sakura',
                 font=('Arial', 10), bg='#2c3e50', fg='#bdc3c7').pack()

        frame = tk.Frame(self.janela, bg='#2c3e50')
        frame.pack(pady=20)

        tk.Label(frame, text='Login', bg='#2c3e50', fg='white',
                 font=('Arial', 10)).grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_login = tk.Entry(frame, font=('Arial', 10))
        self.entry_login.grid(row=0, column=1, padx=5, pady=5)
        self.entry_login.focus()

        tk.Label(frame, text='Senha', bg='#2c3e50', fg='white',
                 font=('Arial', 10)).grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_senha = tk.Entry(frame, show='*', font=('Arial', 10))
        self.entry_senha.grid(row=1, column=1, padx=5, pady=5)
        self.entry_senha.bind('<Return>', lambda e: self._login())

        btn = tk.Button(self.janela, text='Entrar', command=self._login,
                        bg='#27ae60', fg='white', font=('Arial', 10, 'bold'),
                        width=20, height=1)
        btn.pack(pady=10)

    def _login(self):
        global USUARIO_LOGADO
        login = self.entry_login.get()
        senha = self.entry_senha.get()
        usuario = self.ctrl.autenticar(login, senha)
        if usuario:
            USUARIO_LOGADO = usuario
            self.janela.destroy()
            self.on_login_success(usuario)
        else:
            messagebox.showerror('Erro', 'Login ou senha inválidos!')

    def iniciar(self):
        self.janela.mainloop()
