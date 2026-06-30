import tkinter as tk
from tkinter import ttk, messagebox
from controllers.pedido_controller import PedidoController
from controllers.item_cardapio_controller import ItemCardapioController
from views.window_utils import ativar_modal

class PedidoView:
    def __init__(self, parent, usuario):
        self.parent = parent
        self.usuario = usuario
        self.ctrl = PedidoController()
        self.cardapio_ctrl = ItemCardapioController()
        self.pedido_atual = None
        self.janela = tk.Toplevel(parent)
        self.janela.title('Gerenciar Pedidos')
        self.janela.geometry('850x600')
        self.janela.configure(background='#34495e')
        ativar_modal(self.janela, parent)
        self._construir()
        self._atualizar_lista()

    def _construir(self):
        tk.Label(self.janela, text='Pedidos',
                 font=('Arial', 14, 'bold'), bg='#34495e', fg='white').pack(pady=10)

        notebook = ttk.Notebook(self.janela)
        notebook.pack(pady=10, padx=10, fill='both', expand=True)

        self._aba_pedidos(notebook)
        self._aba_itens(notebook)

    def _aba_pedidos(self, notebook):
        frame = tk.Frame(notebook, bg='#ecf0f1')
        notebook.add(frame, text='Pedidos')

        f_btn = tk.Frame(frame, bg='#ecf0f1')
        f_btn.pack(pady=5)

        tk.Label(f_btn, text='Mesa ID:', bg='#ecf0f1', font=('Arial', 9)).pack(side='left', padx=2)
        self.entry_mesa = tk.Entry(f_btn, width=5, font=('Arial', 9))
        self.entry_mesa.pack(side='left', padx=2)

        tk.Button(f_btn, text='Novo Pedido', command=self._novo_pedido,
                  bg='#27ae60', fg='white', font=('Arial', 9, 'bold')).pack(side='left', padx=5)
        tk.Button(f_btn, text='Validar', command=self._validar,
                  bg='#2980b9', fg='white', font=('Arial', 9, 'bold')).pack(side='left', padx=2)
        tk.Button(f_btn, text='Em Preparo', command=self._iniciar_preparo,
                  bg='#f39c12', fg='white', font=('Arial', 9, 'bold')).pack(side='left', padx=2)
        tk.Button(f_btn, text='Pronto', command=self._finalizar_preparo,
                  bg='#e67e22', fg='white', font=('Arial', 9, 'bold')).pack(side='left', padx=2)
        tk.Button(f_btn, text='Cancelar', command=self._cancelar,
                  bg='#e74c3c', fg='white', font=('Arial', 9, 'bold')).pack(side='left', padx=2)

        self.combo_filtro = ttk.Combobox(frame, values=['Todos', 'pendente', 'aguardando_validacao', 'em_preparo', 'pronto'],
                                          state='readonly', font=('Arial', 9))
        self.combo_filtro.set('Todos')
        self.combo_filtro.pack(pady=5)
        self.combo_filtro.bind('<<ComboboxSelected>>', lambda e: self._atualizar_lista())
        tk.Button(frame, text='Atualizar Lista', command=self._atualizar_lista,
                  bg='#95a5a6', fg='white', font=('Arial', 8)).pack()

        f_lista = tk.Frame(frame, bg='#ecf0f1')
        f_lista.pack(pady=5, padx=10, fill='both', expand=True)

        colunas = ('id', 'mesa', 'garcom', 'data', 'status', 'total')
        self.tree = ttk.Treeview(f_lista, columns=colunas, show='headings', height=8)
        headers = {'id': 'ID', 'mesa': 'Mesa', 'garcom': 'Garçom', 'data': 'Data', 'status': 'Status', 'total': 'Total'}
        widths = {'id': 40, 'mesa': 50, 'garcom': 120, 'data': 140, 'status': 120, 'total': 80}
        for c in colunas:
            self.tree.heading(c, text=headers[c])
            self.tree.column(c, width=widths[c])

        scroll = ttk.Scrollbar(f_lista, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')
        self.tree.bind('<<TreeviewSelect>>', self._on_select_pedido)

    def _aba_itens(self, notebook):
        frame = tk.Frame(notebook, bg='#ecf0f1')
        notebook.add(frame, text='Itens do Pedido')

        f_btn = tk.Frame(frame, bg='#ecf0f1')
        f_btn.pack(pady=5)

        tk.Label(f_btn, text='Pedido ID:', bg='#ecf0f1', font=('Arial', 9)).pack(side='left', padx=2)
        self.lbl_pedido_atual = tk.Label(f_btn, text='---', bg='#ecf0f1',
                                          font=('Arial', 9, 'bold'), fg='#e74c3c')
        self.lbl_pedido_atual.pack(side='left', padx=5)

        tk.Label(f_btn, text='Item ID:', bg='#ecf0f1', font=('Arial', 9)).pack(side='left', padx=2)
        self.entry_item = tk.Entry(f_btn, width=5, font=('Arial', 9))
        self.entry_item.pack(side='left', padx=2)

        tk.Label(f_btn, text='Qtd:', bg='#ecf0f1', font=('Arial', 9)).pack(side='left', padx=2)
        self.entry_qtd = tk.Entry(f_btn, width=4, font=('Arial', 9))
        self.entry_qtd.pack(side='left', padx=2)
        self.entry_qtd.insert(0, '1')

        tk.Label(f_btn, text='Preço:', bg='#ecf0f1', font=('Arial', 9)).pack(side='left', padx=2)
        self.entry_preco = tk.Entry(f_btn, width=6, font=('Arial', 9))
        self.entry_preco.pack(side='left', padx=2)

        tk.Label(f_btn, text='Obs:', bg='#ecf0f1', font=('Arial', 9)).pack(side='left', padx=2)
        self.entry_obs = tk.Entry(f_btn, width=15, font=('Arial', 9))
        self.entry_obs.pack(side='left', padx=2)

        tk.Button(f_btn, text='+', command=self._adicionar_item,
                  bg='#27ae60', fg='white', font=('Arial', 9, 'bold')).pack(side='left', padx=5)

        self.lista_itens = tk.Listbox(frame, font=('Arial', 9), height=12)
        self.lista_itens.pack(pady=5, padx=10, fill='both', expand=True)

    def _novo_pedido(self):
        try:
            mesa_id = int(self.entry_mesa.get())
            sucesso, msg, pedido_id = self.ctrl.criar(mesa_id, self.usuario[0])
            if sucesso:
                self.pedido_atual = pedido_id
                self.lbl_pedido_atual.config(text=str(pedido_id))
                messagebox.showinfo('Sucesso', msg)
                self._atualizar_lista()
            else:
                messagebox.showerror('Erro', msg)
        except ValueError:
            messagebox.showerror('Erro', 'ID da mesa deve ser número')

    def _adicionar_item(self):
        if not self.pedido_atual:
            messagebox.showwarning('Aviso', 'Crie um pedido primeiro')
            return
        try:
            item_id = int(self.entry_item.get())
            qtd = int(self.entry_qtd.get())
            preco = float(self.entry_preco.get())
            obs = self.entry_obs.get()
            sucesso, msg = self.ctrl.adicionar_item(self.pedido_atual, item_id, qtd, preco, obs)
            if sucesso:
                self._atualizar_itens()
                self._atualizar_lista()
            else:
                messagebox.showerror('Erro', msg)
        except ValueError:
            messagebox.showerror('Erro', 'Verifique os valores')

    def _on_select_pedido(self, event):
        sel = self.tree.selection()
        if sel:
            item = self.tree.item(sel[0])
            self.pedido_atual = item['values'][0]
            self.lbl_pedido_atual.config(text=str(self.pedido_atual))
            self._atualizar_itens()

    def _validar(self):
        self._acao_pedido(self.ctrl.validar_pedido, 'validar')
    def _iniciar_preparo(self):
        self._acao_pedido(self.ctrl.iniciar_preparo, 'iniciar preparo')
    def _finalizar_preparo(self):
        self._acao_pedido(self.ctrl.finalizar_preparo, 'finalizar')
    def _cancelar(self):
        self._acao_pedido(self.ctrl.cancelar, 'cancelar')

    def _acao_pedido(self, funcao, nome_acao):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning('Aviso', 'Selecione um pedido')
            return
        pid = self.tree.item(sel[0])['values'][0]
        if messagebox.askyesno('Confirmar', f'{nome_acao.capitalize()} pedido {pid}?'):
            sucesso, msg = funcao(pid)
            messagebox.showinfo('Info', msg)
            self._atualizar_lista()

    def _atualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        filtro = self.combo_filtro.get()
        pedidos = self.ctrl.listar() if filtro == 'Todos' else self.ctrl.listar(status=filtro)
        for p in pedidos:
            self.tree.insert('', 'end', values=p)

    def _atualizar_itens(self):
        self.lista_itens.delete(0, 'end')
        if not self.pedido_atual:
            return
        itens = self.ctrl.listar_itens(self.pedido_atual)
        for i in itens:
            subtotal = i[2] * i[3]
            texto = f'{i[1]} x{i[2]} = R$ {subtotal:.2f}'
            if i[4]:
                texto += f' ({i[4]})'
            self.lista_itens.insert('end', texto)
