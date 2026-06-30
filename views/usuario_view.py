import tkinter as tk
from tkinter import messagebox, ttk

from controllers.usuario_controller import UsuarioController
from views.window_utils import ativar_modal


class UsuarioView:
    COR_FUNDO = "#141e2e"
    COR_HEADER = "#1a2535"
    COR_CARD = "#1e2d42"
    COR_CARD_BORDA = "#2a3f5f"
    COR_TITULO = "#ffffff"
    COR_SUBTITULO = "#e8a0bf"
    COR_LABEL = "#94a3b8"
    COR_ENTRY_BG = "#162030"
    COR_ENTRY_FG = "#f1f5f9"
    COR_ENTRY_BORDA = "#2e4a6b"
    COR_ENTRY_FOCUS = "#e8a0bf"
    COR_BTN_OK = "#1a6ea8"
    COR_BTN_OK_H = "#2185c5"
    COR_BTN_DEL = "#7b1a28"
    COR_BTN_DEL_H = "#c0392b"
    COR_TREE_BG = "#162030"
    COR_TREE_FG = "#cbd5e1"
    COR_TREE_SEL = "#1a6ea8"
    COR_TREE_HEAD = "#1a2535"
    COR_DIVISOR = "#1e2d42"

    def __init__(self, parent):
        self.parent = parent
        self.ctrl = UsuarioController()

        self.janela = tk.Toplevel(parent)
        self.janela.title("Gerenciar Usuários")
        self.janela.configure(background=self.COR_FUNDO)
        self.janela.resizable(False, False)
        ativar_modal(self.janela, parent)

        w, h = 860, 640
        sw = self.janela.winfo_screenwidth()
        sh = self.janela.winfo_screenheight()
        self.janela.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

        self._estilo_tree()
        self._construir()
        self._atualizar_lista()

    def _estilo_tree(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Sakura.Treeview",
            background=self.COR_TREE_BG,
            foreground=self.COR_TREE_FG,
            fieldbackground=self.COR_TREE_BG,
            rowheight=28,
            font=("Arial", 9),
        )
        style.configure(
            "Sakura.Treeview.Heading",
            background=self.COR_TREE_HEAD,
            foreground=self.COR_SUBTITULO,
            font=("Arial", 9, "bold"),
            relief="flat",
        )
        style.map(
            "Sakura.Treeview",
            background=[("selected", self.COR_TREE_SEL)],
            foreground=[("selected", "#ffffff")],
        )
        style.configure(
            "Sakura.TCombobox",
            fieldbackground=self.COR_ENTRY_BG,
            background=self.COR_ENTRY_BG,
            foreground=self.COR_ENTRY_FG,
            arrowcolor=self.COR_SUBTITULO,
            selectbackground=self.COR_ENTRY_BG,
            selectforeground=self.COR_ENTRY_FG,
        )

    def _construir(self):

        # HEADER
        header = tk.Frame(
            self.janela,
            bg=self.COR_HEADER,
            highlightbackground=self.COR_DIVISOR,
            highlightthickness=1,
        )
        header.pack(fill="x")

        tk.Label(
            header,
            text="👤  Usuários / Funcionários",
            font=("Arial", 14, "bold"),
            bg=self.COR_HEADER,
            fg=self.COR_TITULO,
        ).pack(side="left", padx=24, pady=16)

        # CORPO
        corpo = tk.Frame(self.janela, bg=self.COR_FUNDO)
        corpo.pack(fill="both", expand=True, padx=16, pady=14)

        # ── Painel esquerdo: formulário
        painel_form = tk.Frame(
            corpo,
            bg=self.COR_CARD,
            highlightbackground=self.COR_CARD_BORDA,
            highlightthickness=1,
        )
        painel_form.pack(side="left", fill="y", padx=(0, 10), ipadx=4)

        tk.Label(
            painel_form,
            text="Novo funcionário",
            font=("Arial", 10, "bold"),
            bg=self.COR_CARD,
            fg=self.COR_TITULO,
        ).pack(anchor="w", padx=20, pady=(18, 12))

        tk.Frame(painel_form, height=1, bg=self.COR_DIVISOR).pack(
            fill="x", padx=14, pady=(0, 14)
        )

        campos = [
            ("nome", "Nome completo", False),
            ("cpf", "CPF", False),
            ("login", "Login", False),
            ("senha", "Senha", True),
        ]
        self.entries = {}
        for chave, placeholder, is_senha in campos:
            self._campo(painel_form, chave, placeholder, is_senha)

        tk.Label(
            painel_form,
            text="Cargo",
            font=("Arial", 9),
            bg=self.COR_CARD,
            fg=self.COR_LABEL,
        ).pack(anchor="w", padx=20, pady=(6, 3))

        self.combo_tipo = ttk.Combobox(
            painel_form,
            values=["garcom", "sushiman", "caixa", "gerente"],
            state="readonly",
            font=("Arial", 10),
            style="Sakura.TCombobox",
        )
        self.combo_tipo.pack(fill="x", padx=20, ipady=5, pady=(0, 16))
        self.combo_tipo.set("garcom")

        btn_cad = tk.Button(
            painel_form,
            text="＋  Cadastrar",
            command=self._cadastrar,
            bg=self.COR_BTN_OK,
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            activebackground=self.COR_BTN_OK_H,
            activeforeground="white",
        )
        btn_cad.pack(fill="x", padx=20, ipady=9, pady=(0, 8))
        btn_cad.bind("<Enter>", lambda e: btn_cad.config(bg=self.COR_BTN_OK_H))
        btn_cad.bind("<Leave>", lambda e: btn_cad.config(bg=self.COR_BTN_OK))

        btn_del = tk.Button(
            painel_form,
            text="✕  Excluir selecionado",
            command=self._excluir,
            bg=self.COR_BTN_DEL,
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            activebackground=self.COR_BTN_DEL_H,
            activeforeground="white",
        )
        btn_del.pack(fill="x", padx=20, ipady=9, pady=(0, 20))
        btn_del.bind("<Enter>", lambda e: btn_del.config(bg=self.COR_BTN_DEL_H))
        btn_del.bind("<Leave>", lambda e: btn_del.config(bg=self.COR_BTN_DEL))

        # ── Painel direito: lista
        painel_lista = tk.Frame(corpo, bg=self.COR_FUNDO)
        painel_lista.pack(side="left", fill="both", expand=True)

        tk.Label(
            painel_lista,
            text="Funcionários cadastrados",
            font=("Arial", 10, "bold"),
            bg=self.COR_FUNDO,
            fg=self.COR_LABEL,
        ).pack(anchor="w", pady=(4, 8))

        frame_tree = tk.Frame(
            painel_lista,
            bg=self.COR_CARD,
            highlightbackground=self.COR_CARD_BORDA,
            highlightthickness=1,
        )
        frame_tree.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            frame_tree,
            columns=("id", "nome", "cpf", "login", "tipo"),
            show="headings",
            style="Sakura.Treeview",
        )
        for col, txt, w in [
            ("id", "ID", 45),
            ("nome", "Nome", 200),
            ("cpf", "CPF", 130),
            ("login", "Login", 120),
            ("tipo", "Cargo", 100),
        ]:
            self.tree.heading(col, text=txt, anchor="w" if col != "id" else "center")
            self.tree.column(col, width=w, anchor="center" if col == "id" else "w")

        scroll = ttk.Scrollbar(frame_tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def _campo(self, parent, chave, placeholder, senha=False):
        tk.Label(
            parent,
            text=placeholder,
            font=("Arial", 9),
            bg=self.COR_CARD,
            fg=self.COR_LABEL,
        ).pack(anchor="w", padx=20, pady=(6, 3))

        entry = tk.Entry(
            parent,
            font=("Arial", 10),
            bg=self.COR_ENTRY_BG,
            fg=self.COR_ENTRY_FG,
            insertbackground=self.COR_SUBTITULO,
            relief="flat",
            highlightbackground=self.COR_ENTRY_BORDA,
            highlightcolor=self.COR_ENTRY_FOCUS,
            highlightthickness=1,
            show="●" if senha else "",
        )
        entry.pack(fill="x", padx=20, ipady=6, pady=(0, 2))
        entry.bind(
            "<FocusIn>",
            lambda e: entry.config(highlightbackground=self.COR_ENTRY_FOCUS),
        )
        entry.bind(
            "<FocusOut>",
            lambda e: entry.config(highlightbackground=self.COR_ENTRY_BORDA),
        )
        self.entries[chave] = entry

    def _cadastrar(self):
        nome = self.entries["nome"].get().strip()
        cpf = self.entries["cpf"].get().strip()
        login = self.entries["login"].get().strip()
        senha = self.entries["senha"].get().strip()
        tipo = self.combo_tipo.get()

        if not all([nome, cpf, login, senha]):
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return

        sucesso, msg = self.ctrl.criar(nome, cpf, login, senha, tipo)
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            for e in self.entries.values():
                e.delete(0, "end")
            self._atualizar_lista()
        else:
            messagebox.showerror("Erro", msg)

    def _excluir(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um funcionário na lista.")
            return
        item = self.tree.item(sel[0])
        uid = item["values"][0]
        nome = item["values"][1]
        if messagebox.askyesno("Confirmar", f'Excluir "{nome}"?'):
            sucesso, msg = self.ctrl.excluir(uid)
            if sucesso:
                messagebox.showinfo("Sucesso", msg)
                self._atualizar_lista()
            else:
                messagebox.showerror("Erro", msg)

    def _atualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for u in self.ctrl.listar():
            self.tree.insert("", "end", values=u)
