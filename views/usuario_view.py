import tkinter as tk
from tkinter import ttk, messagebox
from controllers.usuario_controller import UsuarioController

class UsuarioView:
    def __init__(self, parent):
        self.parent = parent
        self.ctrl = UsuarioController()
        self.janela = tk.Toplevel(parent)
        self.janela.title('Gerenciar Usuários')
        self.janela.geometry('700x500')
        self.janela.configure(background='#34495e')
        self.janela.transient(parent)
        self.janela.grab_set()
        self._construir()
        self._atualizar_lista()

    def _construir(self):
        tk.Label(self.janela, text='Usuários (Funcionários)',
                 font=('Arial', 14, 'bold'), bg='#34495e', fg='white').pack(pady=10)

        frame_form = tk.Frame(self.janela, bg='#34495e')
        frame_form.pack(pady=5, padx=10, fill='x')

        campos = [('Nome:', 0), ('CPF:', 1), ('Login:', 2), ('Senha:', 3)]
        self.entries = {}
        for texto, row in campos:
            tk.Label(frame_form, text=texto, bg='#34495e', fg='white',
                     font=('Arial', 9)).grid(row=row, column=0, padx=5, pady=2, sticky='e')
            e = tk.Entry(frame_form, font=('Arial', 9))
            e.grid(row=row, column=1, padx=5, pady=2, sticky='ew')
            self.entries[texto.replace(':', '').lower()] = e
            frame_form.columnconfigure(1, weight=1)

        tk.Label(frame_form, text='Tipo:', bg='#34495e', fg='white',
                 font=('Arial', 9)).grid(row=4, column=0, padx=5, pady=2, sticky='e')
        self.combo_tipo = ttk.Combobox(frame_form, values=['garcom', 'sushiman', 'caixa', 'gerente'],
                                       state='readonly', font=('Arial', 9))
        self.combo_tipo.grid(row=4, column=1, padx=5, pady=2, sticky='ew')
        self.combo_tipo.set('garcom')

        frame_btn = tk.Frame(self.janela, bg='#34495e')
        frame_btn.pack(pady=5)
        tk.Button(frame_btn, text='Cadastrar', command=self._cadastrar,
                  bg='#27ae60', fg='white', font=('Arial', 9, 'bold')).pack(side='left', padx=5)
        tk.Button(frame_btn, text='Excluir', command=self._excluir,
                  bg='#e74c3c', fg='white', font=('Arial', 9, 'bold')).pack(side='left', padx=5)

        frame_lista = tk.Frame(self.janela, bg='#34495e')
        frame_lista.pack(pady=10, padx=10, fill='both', expand=True)

        self.tree = ttk.Treeview(frame_lista, columns=('id', 'nome', 'cpf', 'login', 'tipo'),
                                  show='headings', height=12)
        self.tree.heading('id', text='ID')
        self.tree.heading('nome', text='Nome')
        self.tree.heading('cpf', text='CPF')
        self.tree.heading('login', text='Login')
        self.tree.heading('tipo', text='Tipo')
        self.tree.column('id', width=40)
        self.tree.column('nome', width=180)
        self.tree.column('cpf', width=120)
        self.tree.column('login', width=100)
        self.tree.column('tipo', width=80)

        scroll = ttk.Scrollbar(frame_lista, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')

    def _cadastrar(self):
        nome = self.entries['nome'].get()
        cpf = self.entries['cpf'].get()
        login = self.entries['login'].get()
        senha = self.entries['senha'].get()
        tipo = self.combo_tipo.get()
        sucesso, msg = self.ctrl.criar(nome, cpf, login, senha, tipo)
        if sucesso:
            messagebox.showinfo('Sucesso', msg)
            for e in self.entries.values():
                e.delete(0, 'end')
            self._atualizar_lista()
        else:
            messagebox.showerror('Erro', msg)

    def _excluir(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning('Aviso', 'Selecione um usuário na lista')
            return
        item = self.tree.item(sel[0])
        uid = item['values'][0]
        nome = item['values'][1]
        if messagebox.askyesno('Confirmar', f'Excluir {nome}?'):
            sucesso, msg = self.ctrl.excluir(uid)
            if sucesso:
                messagebox.showinfo('Sucesso', msg)
                self._atualizar_lista()
            else:
                messagebox.showerror('Erro', msg)

    def _atualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for u in self.ctrl.listar():
            self.tree.insert('', 'end', values=u)
