import tkinter as tk
from tkinter import ttk, messagebox
from controllers.item_cardapio_controller import ItemCardapioController
from controllers.categoria_controller import CategoriaController
from views.window_utils import ativar_modal

class CardapioView:
    def __init__(self, parent):
        self.parent = parent
        self.ctrl = ItemCardapioController()
        self.cat_ctrl = CategoriaController()
        self.janela = tk.Toplevel(parent)
        self.janela.title('Gerenciar Cardápio')
        self.janela.geometry('800x550')
        self.janela.configure(background='#34495e')
        ativar_modal(self.janela, parent)
        self._construir()
        self._atualizar_lista()

    def _construir(self):
        tk.Label(self.janela, text='Cardápio Digital',
                 font=('Arial', 14, 'bold'), bg='#34495e', fg='white').pack(pady=10)

        frame_form = tk.Frame(self.janela, bg='#34495e')
        frame_form.pack(pady=5, padx=10, fill='x')

        tk.Label(frame_form, text='Categoria:', bg='#34495e', fg='white',
                 font=('Arial', 9)).grid(row=0, column=0, padx=5, pady=2, sticky='e')
        self.combo_cat = ttk.Combobox(frame_form, state='readonly', font=('Arial', 9))
        self.combo_cat.grid(row=0, column=1, padx=5, pady=2, sticky='ew')
        self._carregar_categorias()

        tk.Label(frame_form, text='Nome:', bg='#34495e', fg='white',
                 font=('Arial', 9)).grid(row=1, column=0, padx=5, pady=2, sticky='e')
        self.entry_nome = tk.Entry(frame_form, font=('Arial', 9))
        self.entry_nome.grid(row=1, column=1, padx=5, pady=2, sticky='ew')

        tk.Label(frame_form, text='Preço:', bg='#34495e', fg='white',
                 font=('Arial', 9)).grid(row=2, column=0, padx=5, pady=2, sticky='e')
        self.entry_preco = tk.Entry(frame_form, font=('Arial', 9))
        self.entry_preco.grid(row=2, column=1, padx=5, pady=2, sticky='ew')

        tk.Label(frame_form, text='Descrição:', bg='#34495e', fg='white',
                 font=('Arial', 9)).grid(row=3, column=0, padx=5, pady=2, sticky='e')
        self.entry_desc = tk.Entry(frame_form, font=('Arial', 9))
        self.entry_desc.grid(row=3, column=1, padx=5, pady=2, sticky='ew')

        tk.Label(frame_form, text='Ingredientes:', bg='#34495e', fg='white',
                 font=('Arial', 9)).grid(row=4, column=0, padx=5, pady=2, sticky='e')
        self.entry_ing = tk.Entry(frame_form, font=('Arial', 9))
        self.entry_ing.grid(row=4, column=1, padx=5, pady=2, sticky='ew')

        tk.Label(frame_form, text='V. Nutricional:', bg='#34495e', fg='white',
                 font=('Arial', 9)).grid(row=5, column=0, padx=5, pady=2, sticky='e')
        self.entry_nutri = tk.Entry(frame_form, font=('Arial', 9))
        self.entry_nutri.grid(row=5, column=1, padx=5, pady=2, sticky='ew')
        frame_form.columnconfigure(1, weight=1)

        frame_btn = tk.Frame(self.janela, bg='#34495e')
        frame_btn.pack(pady=5)
        for texto, comando, cor in [
            ('Cadastrar', self._cadastrar, '#27ae60'),
            ('Alternar Disp.', self._alternar_disp, '#f39c12'),
            ('Excluir', self._excluir, '#e74c3c'),
        ]:
            tk.Button(frame_btn, text=texto, command=comando,
                      bg=cor, fg='white', font=('Arial', 9, 'bold')).pack(side='left', padx=3)

        frame_lista = tk.Frame(self.janela, bg='#34495e')
        frame_lista.pack(pady=10, padx=10, fill='both', expand=True)

        colunas = ('id', 'nome', 'preco', 'disponivel', 'categoria', 'ingredientes')
        self.tree = ttk.Treeview(frame_lista, columns=colunas, show='headings', height=12)
        self.tree.heading('id', text='ID')
        self.tree.heading('nome', text='Nome')
        self.tree.heading('preco', text='Preço')
        self.tree.heading('disponivel', text='Disp.')
        self.tree.heading('categoria', text='Categoria')
        self.tree.heading('ingredientes', text='Ingredientes')
        for c, w in zip(colunas, [40, 180, 70, 50, 120, 200]):
            self.tree.column(c, width=w)

        scroll = ttk.Scrollbar(frame_lista, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')

    def _carregar_categorias(self):
        cats = self.cat_ctrl.listar()
        self.cat_map = {f'{c[1]} (ID {c[0]})': c[0] for c in cats}
        self.combo_cat['values'] = list(self.cat_map.keys())
        if self.cat_map:
            self.combo_cat.set(list(self.cat_map.keys())[0])

    def _cadastrar(self):
        try:
            cat_key = self.combo_cat.get()
            if not cat_key or cat_key not in self.cat_map:
                messagebox.showerror('Erro', 'Selecione uma categoria')
                return
            cat_id = self.cat_map[cat_key]
            nome = self.entry_nome.get()
            preco = float(self.entry_preco.get())
            sucesso, msg = self.ctrl.criar(cat_id, nome, preco,
                                           self.entry_desc.get(), 1,
                                           self.entry_ing.get(), self.entry_nutri.get())
            if sucesso:
                messagebox.showinfo('Sucesso', msg)
                for e in [self.entry_nome, self.entry_preco, self.entry_desc,
                          self.entry_ing, self.entry_nutri]:
                    e.delete(0, 'end')
                self._atualizar_lista()
            else:
                messagebox.showerror('Erro', msg)
        except ValueError:
            messagebox.showerror('Erro', 'Preço deve ser um número')

    def _alternar_disp(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning('Aviso', 'Selecione um item')
            return
        iid = self.tree.item(sel[0])['values'][0]
        sucesso, msg = self.ctrl.alternar_disponibilidade(iid)
        messagebox.showinfo('Info', msg)
        self._atualizar_lista()

    def _excluir(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning('Aviso', 'Selecione um item')
            return
        item = self.tree.item(sel[0])
        iid = item['values'][0]
        if messagebox.askyesno('Confirmar', f'Excluir "{item["values"][1]}"?'):
            sucesso, msg = self.ctrl.excluir(iid)
            if sucesso:
                messagebox.showinfo('Sucesso', msg)
                self._atualizar_lista()
            else:
                messagebox.showerror('Erro', msg)

    def _atualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for i in self.ctrl.listar():
            values = (i[0], i[1], f'R$ {i[3]:.2f}', '✅' if i[4] else '❌', i[7], i[5])
            self.tree.insert('', 'end', values=values)
