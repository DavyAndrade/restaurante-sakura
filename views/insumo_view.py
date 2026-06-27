import tkinter as tk
from tkinter import ttk, messagebox
from controllers.insumo_controller import InsumoController

class InsumoView:
    def __init__(self, parent):
        self.parent = parent
        self.ctrl = InsumoController()
        self.janela = tk.Toplevel(parent)
        self.janela.title('Gerenciar Insumos')
        self.janela.geometry('700x500')
        self.janela.configure(background='#34495e')
        self.janela.transient(parent)
        self.janela.grab_set()
        self._construir()
        self._atualizar_lista()

    def _construir(self):
        tk.Label(self.janela, text='Insumos e Estoque',
                 font=('Arial', 14, 'bold'), bg='#34495e', fg='white').pack(pady=10)

        notebook = ttk.Notebook(self.janela)
        notebook.pack(pady=10, padx=10, fill='both', expand=True)

        self._aba_insumos(notebook)
        self._aba_vinculo(notebook)

    def _aba_insumos(self, notebook):
        frame = tk.Frame(notebook, bg='#ecf0f1')
        notebook.add(frame, text='Insumos')

        f_form = tk.Frame(frame, bg='#ecf0f1')
        f_form.pack(pady=10, padx=10, fill='x')

        tk.Label(f_form, text='Nome:', bg='#ecf0f1', font=('Arial', 9)).grid(row=0, column=0, padx=5, pady=2, sticky='e')
        self.entry_nome = tk.Entry(f_form, font=('Arial', 9))
        self.entry_nome.grid(row=0, column=1, padx=5, pady=2, sticky='ew')

        tk.Label(f_form, text='Qtd atual:', bg='#ecf0f1', font=('Arial', 9)).grid(row=1, column=0, padx=5, pady=2, sticky='e')
        self.entry_qtd = tk.Entry(f_form, font=('Arial', 9))
        self.entry_qtd.grid(row=1, column=1, padx=5, pady=2, sticky='ew')
        self.entry_qtd.insert(0, '0')

        tk.Label(f_form, text='Unidade:', bg='#ecf0f1', font=('Arial', 9)).grid(row=2, column=0, padx=5, pady=2, sticky='e')
        self.combo_un = ttk.Combobox(f_form, values=['kg', 'g', 'un', 'l', 'ml'], state='readonly', font=('Arial', 9))
        self.combo_un.grid(row=2, column=1, padx=5, pady=2, sticky='ew')
        self.combo_un.set('un')
        f_form.columnconfigure(1, weight=1)

        f_btn = tk.Frame(frame, bg='#ecf0f1')
        f_btn.pack(pady=5)
        tk.Button(f_btn, text='Cadastrar', command=self._cadastrar,
                  bg='#27ae60', fg='white', font=('Arial', 9, 'bold')).pack(side='left', padx=5)
        tk.Button(f_btn, text='Ajustar Estoque', command=self._ajustar,
                  bg='#f39c12', fg='white', font=('Arial', 9, 'bold')).pack(side='left', padx=5)

        f_lista = tk.Frame(frame, bg='#ecf0f1')
        f_lista.pack(pady=10, padx=10, fill='both', expand=True)

        self.tree = ttk.Treeview(f_lista, columns=('id', 'nome', 'qtd', 'un'), show='headings', height=10)
        self.tree.heading('id', text='ID')
        self.tree.heading('nome', text='Nome')
        self.tree.heading('qtd', text='Estoque')
        self.tree.heading('un', text='Un')
        self.tree.column('id', width=40)
        self.tree.column('nome', width=200)
        self.tree.column('qtd', width=80)
        self.tree.column('un', width=50)
        scroll = ttk.Scrollbar(f_lista, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')

        self.entry_ajuste_qtd = tk.Entry(frame, font=('Arial', 9))
        self.entry_ajuste_qtd.pack(pady=5)
        self.entry_ajuste_qtd.insert(0, 'Qtd para adicionar (negativo p/ retirar)')

    def _aba_vinculo(self, notebook):
        frame = tk.Frame(notebook, bg='#ecf0f1')
        notebook.add(frame, text='Vincular a Item')

        f_form = tk.Frame(frame, bg='#ecf0f1')
        f_form.pack(pady=10, padx=10, fill='x')

        tk.Label(f_form, text='ID do Item:', bg='#ecf0f1', font=('Arial', 9)).grid(row=0, column=0, padx=5, pady=2, sticky='e')
        self.entry_vi_item = tk.Entry(f_form, font=('Arial', 9))
        self.entry_vi_item.grid(row=0, column=1, padx=5, pady=2, sticky='ew')

        tk.Label(f_form, text='ID do Insumo:', bg='#ecf0f1', font=('Arial', 9)).grid(row=1, column=0, padx=5, pady=2, sticky='e')
        self.entry_vi_insumo = tk.Entry(f_form, font=('Arial', 9))
        self.entry_vi_insumo.grid(row=1, column=1, padx=5, pady=2, sticky='ew')

        tk.Label(f_form, text='Qtd por porção:', bg='#ecf0f1', font=('Arial', 9)).grid(row=2, column=0, padx=5, pady=2, sticky='e')
        self.entry_vi_qtd = tk.Entry(f_form, font=('Arial', 9))
        self.entry_vi_qtd.grid(row=2, column=1, padx=5, pady=2, sticky='ew')
        f_form.columnconfigure(1, weight=1)

        tk.Button(frame, text='Vincular', command=self._vincular,
                  bg='#27ae60', fg='white', font=('Arial', 9, 'bold')).pack(pady=5)

        f_consulta = tk.Frame(frame, bg='#ecf0f1')
        f_consulta.pack(pady=10, padx=10, fill='both', expand=True)
        tk.Label(f_consulta, text='Consultar insumos de um item (ID):',
                 bg='#ecf0f1', font=('Arial', 9)).pack(anchor='w')
        f_row = tk.Frame(f_consulta, bg='#ecf0f1')
        f_row.pack(fill='x')
        self.entry_vi_consulta = tk.Entry(f_row, font=('Arial', 9))
        self.entry_vi_consulta.pack(side='left', padx=5, fill='x', expand=True)
        tk.Button(f_row, text='Consultar', command=self._consultar_vinculos,
                  bg='#2980b9', fg='white', font=('Arial', 9)).pack(side='right')

        self.lista_vinculos = tk.Listbox(f_consulta, font=('Arial', 9), height=6)
        self.lista_vinculos.pack(pady=5, fill='both', expand=True)

    def _cadastrar(self):
        nome = self.entry_nome.get()
        try:
            qtd = float(self.entry_qtd.get())
        except ValueError:
            qtd = 0
        un = self.combo_un.get()
        sucesso, msg = self.ctrl.criar(nome, qtd, un)
        if sucesso:
            messagebox.showinfo('Sucesso', msg)
            self.entry_nome.delete(0, 'end')
            self._atualizar_lista()
        else:
            messagebox.showerror('Erro', msg)

    def _ajustar(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning('Aviso', 'Selecione um insumo')
            return
        iid = self.tree.item(sel[0])['values'][0]
        try:
            qtd = float(self.entry_ajuste_qtd.get())
        except ValueError:
            messagebox.showerror('Erro', 'Quantidade inválida')
            return
        sucesso, msg = self.ctrl.ajustar_estoque(iid, qtd)
        messagebox.showinfo('Info', msg)
        self._atualizar_lista()

    def _vincular(self):
        try:
            item_id = int(self.entry_vi_item.get())
            insumo_id = int(self.entry_vi_insumo.get())
            qtd = float(self.entry_vi_qtd.get())
            sucesso, msg = self.ctrl.vincular_item(item_id, insumo_id, qtd)
            if sucesso:
                messagebox.showinfo('Sucesso', msg)
                for e in [self.entry_vi_item, self.entry_vi_insumo, self.entry_vi_qtd]:
                    e.delete(0, 'end')
            else:
                messagebox.showerror('Erro', msg)
        except ValueError:
            messagebox.showerror('Erro', 'IDs e quantidade devem ser números')

    def _consultar_vinculos(self):
        try:
            item_id = int(self.entry_vi_consulta.get())
            self.lista_vinculos.delete(0, 'end')
            itens = self.ctrl.listar_insumos_do_item(item_id)
            if itens:
                for i in itens:
                    self.lista_vinculos.insert('end', f'{i[1]} - {i[2]} ({i[3]:.2f} por porção)')
            else:
                self.lista_vinculos.insert('end', 'Nenhum vínculo encontrado')
        except ValueError:
            messagebox.showerror('Erro', 'ID inválido')

    def _atualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for i in self.ctrl.listar():
            self.tree.insert('', 'end', values=(i[0], i[1], i[2], i[3]))
