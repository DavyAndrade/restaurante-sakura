import tkinter as tk
from views.usuario_view import UsuarioView
from views.mesa_view import MesaView
from views.categoria_view import CategoriaView
from views.cardapio_view import CardapioView
from views.insumo_view import InsumoView
from views.pedido_view import PedidoView
from views.conta_view import ContaView

class MainView:
    def __init__(self, usuario):
        self.usuario = usuario
        self.janela = tk.Tk()
        self.janela.title(f'Sakura Management System - {usuario[1]} ({usuario[2]})')
        self.janela.geometry('600x500')
        self.janela.configure(background='#2c3e50')
        self.janela.protocol('WM_DELETE_WINDOW', self._sair)
        self._construir()

    def _construir(self):
        tk.Label(self.janela, text='Sakura Management System',
                 font=('Arial', 18, 'bold'), bg='#2c3e50', fg='white').pack(pady=20)
        tk.Label(self.janela,
                 text=f'Bem-vindo, {self.usuario[1]}  |  Cargo: {self.usuario[2]}',
                 font=('Arial', 10), bg='#2c3e50', fg='#bdc3c7').pack()

        frame = tk.Frame(self.janela, bg='#2c3e50')
        frame.pack(pady=20)

        botoes = [
            ('👤 Usuários', self._abrir_usuarios, '#3498db'),
            ('🪑 Mesas', self._abrir_mesas, '#2980b9'),
            ('📂 Categorias', self._abrir_categorias, '#1abc9c'),
            ('🍣 Cardápio', self._abrir_cardapio, '#16a085'),
            ('📦 Insumos', self._abrir_insumos, '#f39c12'),
            ('📋 Pedidos', self._abrir_pedidos, '#e67e22'),
            ('💰 Contas', self._abrir_contas, '#9b59b6'),
        ]

        for i, (texto, comando, cor) in enumerate(botoes):
            btn = tk.Button(frame, text=texto, command=comando,
                            bg=cor, fg='white', font=('Arial', 11, 'bold'),
                            width=25, height=2, relief='raised')
            btn.grid(row=i//2, column=i%2, padx=10, pady=10)

        tk.Button(self.janela, text='Sair', command=self._sair,
                  bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'),
                  width=15).pack(pady=20)

    def _abrir_usuarios(self):
        UsuarioView(self.janela)

    def _abrir_mesas(self):
        MesaView(self.janela)

    def _abrir_categorias(self):
        CategoriaView(self.janela)

    def _abrir_cardapio(self):
        CardapioView(self.janela)

    def _abrir_insumos(self):
        InsumoView(self.janela)

    def _abrir_pedidos(self):
        PedidoView(self.janela, self.usuario)

    def _abrir_contas(self):
        ContaView(self.janela, self.usuario)

    def _sair(self):
        self.janela.quit()
        self.janela.destroy()

    def iniciar(self):
        self.janela.mainloop()
