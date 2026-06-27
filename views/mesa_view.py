import tkinter as tk
from tkinter import ttk, messagebox
from controllers.mesa_controller import MesaController

class MesaView:
    def __init__(self, parent):
        self.parent = parent
        self.ctrl = MesaController()
        self.janela = tk.Toplevel(parent)
        self.janela.title('Gerenciar Mesas')
        self.janela.geometry('650x480')
        self.janela.configure(background='#34495e')
        self.janela.transient(parent)
        self.janela.grab_set()
        self._construir()
        self._atualizar_lista()

    def _construir(self):
        tk.Label(self.janela, text='Gerenciamento de Mesas',
                 font=('Arial', 14, 'bold'), bg='#34495e', fg='white').pack(pady=10)

        frame_form = tk.Frame(self.janela, bg='#34495e')
        frame_form.pack(pady=5, padx=10, fill='x')

        tk.Label(frame_form, text='Número:', bg='#34495e', fg='white',
                 font=('Arial', 9)).grid(row=0, column=0, padx=5, pady=2, sticky='e')
        self.entry_numero = tk.Entry(frame_form, font=('Arial', 9))
        self.entry_numero.grid(row=0, column=1, padx=5, pady=2, sticky='ew')
        self.entry_numero.insert(0, '1')

        tk.Label(frame_form, text='Capacidade:', bg='#34495e', fg='white',
                 font=('Arial', 9)).grid(row=1, column=0, padx=5, pady=2, sticky='e')
        self.entry_capacidade = tk.Entry(frame_form, font=('Arial', 9))
        self.entry_capacidade.grid(row=1, column=1, padx=5, pady=2, sticky='ew')
        self.entry_capacidade.insert(0, '4')
        frame_form.columnconfigure(1, weight=1)

        frame_btn = tk.Frame(self.janela, bg='#34495e')
        frame_btn.pack(pady=5)
        for texto, comando, cor in [
            ('Cadastrar', self._cadastrar, '#27ae60'),
            ('Abrir Mesa', self._abrir, '#2980b9'),
            ('Liberar Mesa', self._liberar, '#f39c12'),
            ('Excluir', self._excluir, '#e74c3c'),
        ]:
            tk.Button(frame_btn, text=texto, command=comando,
                      bg=cor, fg='white', font=('Arial', 9, 'bold')).pack(side='left', padx=3)

        frame_lista = tk.Frame(self.janela, bg='#34495e')
        frame_lista.pack(pady=10, padx=10, fill='both', expand=True)

        self.tree = ttk.Treeview(frame_lista, columns=('id', 'numero', 'capacidade', 'status'),
                                  show='headings', height=12)
        self.tree.heading('id', text='ID')
        self.tree.heading('numero', text='Nº')
        self.tree.heading('capacidade', text='Capacidade')
        self.tree.heading('status', text='Status')
        self.tree.column('id', width=40)
        self.tree.column('numero', width=60)
        self.tree.column('capacidade', width=90)
        self.tree.column('status', width=100)

        scroll = ttk.Scrollbar(frame_lista, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')

    def _cadastrar(self):
        try:
            numero = int(self.entry_numero.get())
            capacidade = int(self.entry_capacidade.get())
            sucesso, msg = self.ctrl.criar(numero, capacidade)
            if sucesso:
                messagebox.showinfo('Sucesso', msg)
                self._atualizar_lista()
            else:
                messagebox.showerror('Erro', msg)
        except ValueError:
            messagebox.showerror('Erro', 'Número e capacidade devem ser inteiros')

    def _abrir(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning('Aviso', 'Selecione uma mesa')
            return
        mid = self.tree.item(sel[0])['values'][0]
        sucesso, msg = self.ctrl.abrir_mesa(mid)
        if sucesso:
            messagebox.showinfo('Sucesso', msg)
        else:
            messagebox.showerror('Erro', msg)
        self._atualizar_lista()

    def _liberar(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning('Aviso', 'Selecione uma mesa')
            return
        mid = self.tree.item(sel[0])['values'][0]
        if messagebox.askyesno('Confirmar', 'Liberar esta mesa?'):
            sucesso, msg = self.ctrl.liberar_mesa(mid)
            if sucesso:
                messagebox.showinfo('Sucesso', msg)
            else:
                messagebox.showerror('Erro', msg)
            self._atualizar_lista()

    def _excluir(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning('Aviso', 'Selecione uma mesa')
            return
        item = self.tree.item(sel[0])
        mid = item['values'][0]
        if messagebox.askyesno('Confirmar', f'Excluir mesa {item["values"][1]}?'):
            sucesso, msg = self.ctrl.excluir(mid)
            if sucesso:
                messagebox.showinfo('Sucesso', msg)
            else:
                messagebox.showerror('Erro', msg)
            self._atualizar_lista()

    def _atualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for m in self.ctrl.listar():
            self.tree.insert('', 'end', values=m)
