import tkinter as tk
from tkinter import messagebox

from controllers.usuario_controller import UsuarioController

USUARIO_LOGADO = None


class LoginView:
    # ── Paleta ────────────────────────────────────────────────────────
    COR_FUNDO = "#141e2e"
    COR_CARD = "#1e2d42"
    COR_CARD_BORDA = "#2a3f5f"
    COR_TITULO = "#ffffff"
    COR_SUBTITULO = "#e8a0bf"
    COR_LABEL = "#94a3b8"
    COR_LABEL_FOCUS = "#cbd5e1"
    COR_ENTRY_BG = "#162030"
    COR_ENTRY_FG = "#f1f5f9"
    COR_ENTRY_BORDA = "#2e4a6b"
    COR_ENTRY_FOCUS = "#e8a0bf"
    COR_BTN = "#9b2335"
    COR_BTN_HOVER = "#c0392b"
    COR_BTN_PRESS = "#7b1a28"
    COR_DIVISOR = "#1e2d42"
    COR_VERSAO = "#3d5275"
    COR_ICONE_CAMPO = "#3d5275"

    def __init__(self, on_login_success):
        self.on_login_success = on_login_success
        self.ctrl = UsuarioController()

        self.janela = tk.Tk()
        self.janela.title("Sakura Management System")
        self.janela.configure(background=self.COR_FUNDO)
        self.janela.resizable(False, False)

        w, h = 480, 520
        sw = self.janela.winfo_screenwidth()
        sh = self.janela.winfo_screenheight()
        self.janela.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

        self._construir()

    def _construir(self):

        frame_header = tk.Frame(self.janela, bg=self.COR_FUNDO)
        frame_header.pack(fill="x", pady=(38, 0))

        tk.Label(
            frame_header,
            text="🌸",
            font=("Arial", 30),
            bg=self.COR_FUNDO,
            fg=self.COR_SUBTITULO,
        ).pack()

        tk.Label(
            frame_header,
            text="Restaurante Sakura",
            font=("Arial", 22, "bold"),
            bg=self.COR_FUNDO,
            fg=self.COR_TITULO,
        ).pack(pady=(4, 0))

        tk.Label(
            frame_header,
            text="Sistema de Gestão Interno",
            font=("Arial", 9),
            bg=self.COR_FUNDO,
            fg=self.COR_SUBTITULO,
        ).pack(pady=(3, 0))

        tk.Frame(self.janela, height=1, bg=self.COR_DIVISOR).pack(
            fill="x", padx=44, pady=(22, 0)
        )

        card = tk.Frame(
            self.janela,
            bg=self.COR_CARD,
            highlightbackground=self.COR_CARD_BORDA,
            highlightthickness=1,
        )
        card.pack(padx=44, pady=18, fill="both")

        inner = tk.Frame(card, bg=self.COR_CARD)
        inner.pack(padx=28, pady=24, fill="both")

        tk.Label(
            inner,
            text="Acesso ao sistema",
            font=("Arial", 10, "bold"),
            bg=self.COR_CARD,
            fg=self.COR_LABEL_FOCUS,
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 16))

        tk.Label(
            inner,
            text="👤  Usuário",
            font=("Arial", 9),
            anchor="w",
            bg=self.COR_CARD,
            fg=self.COR_LABEL,
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 4))

        self.entry_login = tk.Entry(
            inner,
            font=("Arial", 11),
            width=30,
            bg=self.COR_ENTRY_BG,
            fg=self.COR_ENTRY_FG,
            insertbackground=self.COR_SUBTITULO,
            relief="flat",
            highlightbackground=self.COR_ENTRY_BORDA,
            highlightcolor=self.COR_ENTRY_FOCUS,
            highlightthickness=1,
        )
        self.entry_login.grid(
            row=2, column=0, columnspan=2, ipady=8, sticky="ew", pady=(0, 14)
        )
        self.entry_login.focus()
        self.entry_login.bind("<FocusIn>", lambda e: self._foco_on(self.entry_login))
        self.entry_login.bind("<FocusOut>", lambda e: self._foco_off(self.entry_login))

        tk.Label(
            inner,
            text="🔒  Senha",
            font=("Arial", 9),
            anchor="w",
            bg=self.COR_CARD,
            fg=self.COR_LABEL,
        ).grid(row=3, column=0, columnspan=2, sticky="w", pady=(0, 4))

        self.entry_senha = tk.Entry(
            inner,
            show="●",
            font=("Arial", 11),
            width=30,
            bg=self.COR_ENTRY_BG,
            fg=self.COR_ENTRY_FG,
            insertbackground=self.COR_SUBTITULO,
            relief="flat",
            highlightbackground=self.COR_ENTRY_BORDA,
            highlightcolor=self.COR_ENTRY_FOCUS,
            highlightthickness=1,
        )
        self.entry_senha.grid(
            row=4, column=0, columnspan=2, ipady=8, sticky="ew", pady=(0, 6)
        )
        self.entry_senha.bind("<Return>", lambda e: self._login())
        self.entry_senha.bind("<FocusIn>", lambda e: self._foco_on(self.entry_senha))
        self.entry_senha.bind("<FocusOut>", lambda e: self._foco_off(self.entry_senha))

        inner.columnconfigure(0, weight=1)
        inner.columnconfigure(1, weight=1)

        self.btn = tk.Button(
            self.janela,
            text="Entrar",
            command=self._login,
            bg=self.COR_BTN,
            fg="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            activebackground=self.COR_BTN_HOVER,
            activeforeground="white",
        )
        self.btn.pack(padx=44, fill="x", ipady=10)
        self.btn.bind("<Enter>", lambda e: self.btn.config(bg=self.COR_BTN_HOVER))
        self.btn.bind("<Leave>", lambda e: self.btn.config(bg=self.COR_BTN))
        self.btn.bind(
            "<ButtonPress-1>", lambda e: self.btn.config(bg=self.COR_BTN_PRESS)
        )
        self.btn.bind(
            "<ButtonRelease-1>", lambda e: self.btn.config(bg=self.COR_BTN_HOVER)
        )

        tk.Label(
            self.janela,
            text="v1.0.0  ·  © 2025 Restaurante Sakura",
            font=("Arial", 8),
            bg=self.COR_FUNDO,
            fg=self.COR_VERSAO,
        ).pack(side="bottom", pady=14)

    def _foco_on(self, entry):
        entry.config(highlightbackground=self.COR_ENTRY_FOCUS)

    def _foco_off(self, entry):
        entry.config(highlightbackground=self.COR_ENTRY_BORDA)

    def _login(self):
        global USUARIO_LOGADO
        login = self.entry_login.get().strip()
        senha = self.entry_senha.get().strip()

        if not login or not senha:
            messagebox.showwarning("Atenção", "Preencha usuário e senha.")
            return

        usuario = self.ctrl.autenticar(login, senha)
        if usuario:
            USUARIO_LOGADO = usuario
            self.janela.destroy()
            self.on_login_success(usuario)
        else:
            messagebox.showerror("Acesso negado", "Usuário ou senha inválidos.")
            self.entry_senha.delete(0, "end")
            self.entry_senha.focus()

    def iniciar(self):
        self.janela.mainloop()
