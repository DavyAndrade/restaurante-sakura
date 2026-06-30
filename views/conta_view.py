import tkinter as tk
from tkinter import ttk, messagebox
from controllers.conta_controller import ContaController
from views.window_utils import ativar_modal

class ContaView:
    def __init__(self, parent, usuario):
        self.parent = parent
        self.usuario = usuario
        self.ctrl = ContaController()
        self.janela = tk.Toplevel(parent)
        self.janela.title('Contas e Pagamentos')
        self.janela.geometry('800x550')
        self.janela.configure(background='#34495e')
        ativar_modal(self.janela, parent)
        self._construir()
        self._atualizar_lista()

    def _construir(self):
        tk.Label(self.janela, text='Contas e Pagamentos',
                 font=('Arial', 14, 'bold'), bg='#34495e', fg='white').pack(pady=10)

        notebook = ttk.Notebook(self.janela)
        notebook.pack(pady=10, padx=10, fill='both', expand=True)

        self._aba_contas(notebook)
        self._aba_relatorio(notebook)

    def _aba_contas(self, notebook):
        frame = tk.Frame(notebook, bg='#ecf0f1')
        notebook.add(frame, text='Contas')

        f_btn = tk.Frame(frame, bg='#ecf0f1')
        f_btn.pack(pady=5)

        tk.Label(f_btn, text='Pedido ID:', bg='#ecf0f1', font=('Arial', 9)).pack(side='left', padx=2)
        self.entry_pedido = tk.Entry(f_btn, width=6, font=('Arial', 9))
        self.entry_pedido.pack(side='left', padx=2)

        tk.Button(f_btn, text='Abrir Conta', command=self._abrir_conta,
                  bg='#27ae60', fg='white', font=('Arial', 9, 'bold')).pack(side='left', padx=5)

        self.combo_metodo = ttk.Combobox(f_btn, values=['pix', 'cartao', 'dinheiro'],
                                          state='readonly', font=('Arial', 9), width=10)
        self.combo_metodo.pack(side='left', padx=2)
        self.combo_metodo.set('pix')

        tk.Button(f_btn, text='Pagar', command=self._pagar,
                  bg='#2980b9', fg='white', font=('Arial', 9, 'bold')).pack(side='left', padx=5)

        self.combo_filtro = ttk.Combobox(frame, values=['Todas', 'Abertas', 'Pagas'],
                                          state='readonly', font=('Arial', 9))
        self.combo_filtro.set('Todas')
        self.combo_filtro.pack(pady=5)
        self.combo_filtro.bind('<<ComboboxSelected>>', lambda e: self._atualizar_lista())

        f_lista = tk.Frame(frame, bg='#ecf0f1')
        f_lista.pack(pady=5, padx=10, fill='both', expand=True)

        colunas = ('id', 'valor', 'metodo', 'status', 'pedido_id', 'mesa', 'caixa')
        self.tree = ttk.Treeview(f_lista, columns=colunas, show='headings', height=10)
        headers = {'id': 'ID', 'valor': 'Valor', 'metodo': 'Método', 'status': 'Status',
                    'pedido_id': 'Pedido', 'mesa': 'Mesa', 'caixa': 'Caixa'}
        widths = {'id': 40, 'valor': 80, 'metodo': 80, 'status': 60, 'pedido_id': 60, 'mesa': 50, 'caixa': 120}
        for c in colunas:
            self.tree.heading(c, text=headers[c])
            self.tree.column(c, width=widths[c])

        scroll = ttk.Scrollbar(f_lista, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')

    def _aba_relatorio(self, notebook):
        frame = tk.Frame(notebook, bg='#ecf0f1')
        notebook.add(frame, text='Relatório')

        f_filtro = tk.Frame(frame, bg='#ecf0f1')
        f_filtro.pack(pady=10, padx=10, fill='x')

        tk.Label(f_filtro, text='Início (YYYY-MM-DD):', bg='#ecf0f1', font=('Arial', 9)).pack(side='left', padx=2)
        self.entry_ini = tk.Entry(f_filtro, width=12, font=('Arial', 9))
        self.entry_ini.pack(side='left', padx=2)

        tk.Label(f_filtro, text='Fim:', bg='#ecf0f1', font=('Arial', 9)).pack(side='left', padx=2)
        self.entry_fim = tk.Entry(f_filtro, width=12, font=('Arial', 9))
        self.entry_fim.pack(side='left', padx=2)

        tk.Button(f_filtro, text='Gerar', command=self._gerar_relatorio,
                  bg='#27ae60', fg='white', font=('Arial', 9, 'bold')).pack(side='left', padx=5)

        self.lista_rel = tk.Listbox(frame, font=('Arial', 9), height=15)
        self.lista_rel.pack(pady=5, padx=10, fill='both', expand=True)

    def _abrir_conta(self):
        if self.usuario[2] != 'caixa':
            messagebox.showerror('Erro', 'Apenas o Caixa pode abrir contas')
            return
        try:
            pedido_id = int(self.entry_pedido.get())
            sucesso, msg = self.ctrl.abrir_conta(pedido_id, self.usuario[0])
            if sucesso:
                messagebox.showinfo('Sucesso', msg)
                self._atualizar_lista()
            else:
                messagebox.showerror('Erro', msg)
        except ValueError:
            messagebox.showerror('Erro', 'ID do pedido deve ser número')

    def _pagar(self):
        if self.usuario[2] != 'caixa':
            messagebox.showerror('Erro', 'Apenas o Caixa pode processar pagamentos')
            return
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning('Aviso', 'Selecione uma conta')
            return
        conta_id = self.tree.item(sel[0])['values'][0]
        metodo = self.combo_metodo.get()
        if messagebox.askyesno('Confirmar', f'Processar pagamento via {metodo}?'):
            sucesso, msg = self.ctrl.processar_pagamento(conta_id, metodo)
            messagebox.showinfo('Info', msg)
            self._atualizar_lista()

    def _gerar_relatorio(self):
        self.lista_rel.delete(0, 'end')
        inicio = self.entry_ini.get() or None
        fim = self.entry_fim.get() or None
        dados = self.ctrl.relatorio_vendas(inicio, fim)
        total_geral = 0
        for d in dados:
            linha = f'{d[0]} | {d[3] or "N/A"} | {d[1]} conta(s) | R$ {d[2]:.2f}'
            self.lista_rel.insert('end', linha)
            total_geral += d[2]
        self.lista_rel.insert('end', '')
        self.lista_rel.insert('end', f'Total geral: R$ {total_geral:.2f}')
        if not dados:
            self.lista_rel.insert('end', 'Nenhum dado para o período.')

    def _atualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        filtro = self.combo_filtro.get()
        if filtro == 'Abertas':
            contas = self.ctrl.listar(status=0)
        elif filtro == 'Pagas':
            contas = self.ctrl.listar(status=1)
        else:
            contas = self.ctrl.listar()
        for c in contas:
            v = list(c)
            v[3] = '✅ Paga' if v[3] else '⏳ Aberta'
            v[1] = f'R$ {v[1]:.2f}'
            self.tree.insert('', 'end', values=v)
