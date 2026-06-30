import tkinter as tk
from tkinter import ttk, messagebox
from controllers.categoria_controller import CategoriaController
from views.window_utils import ativar_modal

class CategoriaView:
    def __init__(self, parent):
        self.parent = parent
        self.ctrl = CategoriaController()
        self.janela = tk.Toplevel(parent)
        self.janela.title('Gerenciar Categorias')
        self.janela.geometry('550x400')
        self.janela.configure(background='#34495e')
        ativar_modal(self.janela, parent)
        self._construir()
        self._atualizar_lista()

    def _construir(self):
        tk.Label(self.janela, text='Categorias do Cardápio',
                 font=('Arial', 14, 'bold'), bg='#34495e', fg='white').pack(pady=10)

        frame_form = tk.Frame(self.janela, bg='#34495e')
        frame_form.pack(pady=5, padx=10, fill='x')

        tk.Label(frame_form, text='Nome:', bg='#34495e', fg='white',
                 font=('Arial', 9)).grid(row=0, column=0, padx=5, pady=2, sticky='e')
        self.entry_nome = tk.Entry(frame_form, font=('Arial', 9))
        self.entry_nome.grid(row=0, column=1, padx=5, pady=2, sticky='ew')

        tk.Label(frame_form, text='Descrição:', bg='#34495e', fg='white',
                 font=('Arial', 9)).grid(row=1, column=0, padx=5, pady=2, sticky='e')
        self.entry_desc = tk.Entry(frame_form, font=('Arial', 9))
        self.entry_desc.grid(row=1, column=1, padx=5, pady=2, sticky='ew')
        frame_form.columnconfigure(1, weight=1)

        frame_btn = tk.Frame(self.janela, bg='#34495e')
        frame_btn.pack(pady=5)
        tk.Button(frame_btn, text='Cadastrar', command=self._cadastrar,
                  bg='#27ae60', fg='white', font=('Arial', 9, 'bold')).pack(side='left', padx=5)
        tk.Button(frame_btn, text='Excluir', command=self._excluir,
                  bg='#e74c3c', fg='white', font=('Arial', 9, 'bold')).pack(side='left', padx=5)

        frame_lista = tk.Frame(self.janela, bg='#34495e')
        frame_lista.pack(pady=10, padx=10, fill='both', expand=True)

        self.tree = ttk.Treeview(frame_lista, columns=('id', 'nome', 'descricao'),
                                  show='headings', height=10)
        self.tree.heading('id', text='ID')
        self.tree.heading('nome', text='Nome')
        self.tree.heading('descricao', text='Descrição')
        self.tree.column('id', width=40)
        self.tree.column('nome', width=150)
        self.tree.column('descricao', width=250)

        scroll = ttk.Scrollbar(frame_lista, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')

    def _cadastrar(self):
        nome = self.entry_nome.get()
        desc = self.entry_desc.get()
        sucesso, msg = self.ctrl.criar(nome, desc)
        if sucesso:
            messagebox.showinfo('Sucesso', msg)
            self.entry_nome.delete(0, 'end')
            self.entry_desc.delete(0, 'end')
            self._atualizar_lista()
        else:
            messagebox.showerror('Erro', msg)

    def _excluir(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning('Aviso', 'Selecione uma categoria')
            return
        item = self.tree.item(sel[0])
        cid = item['values'][0]
        if messagebox.askyesno('Confirmar', f'Excluir "{item["values"][1]}"?'):
            sucesso, msg = self.ctrl.excluir(cid)
            if sucesso:
                messagebox.showinfo('Sucesso', msg)
                self._atualizar_lista()
            else:
                messagebox.showerror('Erro', msg)

    def _atualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for c in self.ctrl.listar():
            self.tree.insert('', 'end', values=c)
