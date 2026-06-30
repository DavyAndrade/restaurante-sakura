import tkinter as tk
from tkinter import messagebox

from views.cardapio_view import CardapioView
from views.categoria_view import CategoriaView
from views.conta_view import ContaView
from views.insumo_view import InsumoView
from views.mesa_view import MesaView
from views.pedido_view import PedidoView
from views.usuario_view import UsuarioView


class MainView:
    COR_FUNDO = "#141e2e"
    COR_HEADER = "#1a2535"
    COR_HEADER_BORDA = "#1e2d42"
    COR_TITULO = "#ffffff"
    COR_SUBTITULO = "#e8a0bf"
    COR_INFO = "#64748b"
    COR_DIVISOR = "#1e2d42"
    COR_VERSAO = "#3d5275"

    MODULOS = [
        ("Usuários", "👤", "#1a6ea8", "#2185c5"),
        ("Mesas", "🪑", "#147a6e", "#19a090"),
        ("Categorias", "📂", "#5a4a9e", "#7060c0"),
        ("Cardápio", "🍣", "#9b4a12", "#c0601a"),
        ("Insumos", "📦", "#7a6b10", "#a08e15"),
        ("Pedidos", "📋", "#8a3a6e", "#b04d90"),
        ("Contas", "💰", "#1e6b38", "#278a49"),
    ]

    def __init__(self, usuario):
        self.usuario = usuario

        self.janela = tk.Tk()
        self.janela.title("Sakura Management System")
        self.janela.configure(background=self.COR_FUNDO)
        self.janela.resizable(False, False)
        self.janela.protocol("WM_DELETE_WINDOW", self._sair)

        w, h = 620, 560
        sw = self.janela.winfo_screenwidth()
        sh = self.janela.winfo_screenheight()
        self.janela.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

        self._construir()

    def _construir(self):

        # HEADER
        header = tk.Frame(
            self.janela,
            bg=self.COR_HEADER,
            highlightbackground=self.COR_HEADER_BORDA,
            highlightthickness=1,
        )
        header.pack(fill="x")

        inner_h = tk.Frame(header, bg=self.COR_HEADER)
        inner_h.pack(padx=28, pady=18, fill="x")

        esq = tk.Frame(inner_h, bg=self.COR_HEADER)
        esq.pack(side="left")

        tk.Label(
            esq,
            text="🌸  Restaurante Sakura",
            font=("Arial", 17, "bold"),
            bg=self.COR_HEADER,
            fg=self.COR_TITULO,
        ).pack(anchor="w")

        tk.Label(
            esq,
            text="Sistema de Gestão Interno",
            font=("Arial", 8),
            bg=self.COR_HEADER,
            fg=self.COR_SUBTITULO,
        ).pack(anchor="w", pady=(2, 0))

        dir_ = tk.Frame(inner_h, bg=self.COR_HEADER)
        dir_.pack(side="right", anchor="e")

        nome = self.usuario[1] if len(self.usuario) > 1 else "—"
        cargo = self.usuario[2] if len(self.usuario) > 2 else "—"

        tk.Label(
            dir_,
            text=f"👤  {nome}",
            font=("Arial", 10, "bold"),
            bg=self.COR_HEADER,
            fg=self.COR_TITULO,
        ).pack(anchor="e")

        tk.Label(
            dir_,
            text=cargo.capitalize(),
            font=("Arial", 8),
            bg=self.COR_HEADER,
            fg=self.COR_INFO,
        ).pack(anchor="e", pady=(2, 0))

        # SUBTÍTULO
        tk.Label(
            self.janela,
            text="Módulos do sistema",
            font=("Arial", 9),
            bg=self.COR_FUNDO,
            fg=self.COR_INFO,
        ).pack(anchor="w", padx=30, pady=(22, 6))

        # GRID DE MÓDULOS
        grid = tk.Frame(self.janela, bg=self.COR_FUNDO)
        grid.pack(padx=24, fill="both")

        acoes = [
            self._abrir_usuarios,
            self._abrir_mesas,
            self._abrir_categorias,
            self._abrir_cardapio,
            self._abrir_insumos,
            self._abrir_pedidos,
            self._abrir_contas,
        ]

        total = len(self.MODULOS)
        for i, ((label, emoji, cor, cor_h), acao) in enumerate(
            zip(self.MODULOS, acoes)
        ):
            col = i % 3
            row = i // 3
            # Último card sozinho: centraliza na coluna do meio
            if i == total - 1 and total % 3 != 0:
                col = 1
            self._card_modulo(grid, row, col, emoji, label, cor, cor_h, acao)

        for c in range(3):
            grid.columnconfigure(c, weight=1)

        # RODAPÉ
        tk.Frame(self.janela, height=1, bg=self.COR_DIVISOR).pack(
            fill="x", pady=(20, 0)
        )

        rodape = tk.Frame(self.janela, bg=self.COR_FUNDO)
        rodape.pack(fill="x", padx=28, pady=14)

        tk.Label(
            rodape,
            text="v1.0.0  ·  © 2025 Restaurante Sakura",
            font=("Arial", 8),
            bg=self.COR_FUNDO,
            fg=self.COR_VERSAO,
        ).pack(side="left")

        btn_sair = tk.Button(
            rodape,
            text="⏻  Sair do sistema",
            command=self._sair,
            bg="#2d1a1a",
            fg="#e57373",
            font=("Arial", 9, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            activebackground="#3d2020",
            activeforeground="#ef9a9a",
            padx=14,
            pady=5,
        )
        btn_sair.pack(side="right")
        btn_sair.bind("<Enter>", lambda e: btn_sair.config(bg="#3d2020"))
        btn_sair.bind("<Leave>", lambda e: btn_sair.config(bg="#2d1a1a"))

    def _card_modulo(self, parent, row, col, emoji, label, cor, cor_hover, comando):
        COR_CARD_BG = "#1a2535"
        COR_CARD_BORDA = "#243348"

        frame = tk.Frame(
            parent,
            bg=COR_CARD_BG,
            highlightbackground=COR_CARD_BORDA,
            highlightthickness=1,
            cursor="hand2",
        )
        frame.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

        inner = tk.Frame(frame, bg=COR_CARD_BG)
        inner.pack(padx=16, pady=18, fill="both")

        lbl_emoji = tk.Label(
            inner, text=emoji, font=("Arial", 24), bg=COR_CARD_BG, fg=cor
        )
        lbl_emoji.pack()

        lbl_texto = tk.Label(
            inner, text=label, font=("Arial", 10, "bold"), bg=COR_CARD_BG, fg="#cbd5e1"
        )
        lbl_texto.pack(pady=(6, 0))

        def on_enter(e):
            for w in [frame, inner, lbl_emoji, lbl_texto]:
                w.config(bg=cor_hover)
            lbl_emoji.config(fg="white")
            lbl_texto.config(fg="white")
            frame.config(highlightbackground=cor)

        def on_leave(e):
            for w in [frame, inner, lbl_emoji, lbl_texto]:
                w.config(bg=COR_CARD_BG)
            lbl_emoji.config(fg=cor)
            lbl_texto.config(fg="#cbd5e1")
            frame.config(highlightbackground=COR_CARD_BORDA)

        for widget in [frame, inner, lbl_emoji, lbl_texto]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", lambda e, c=comando: c())

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
        if messagebox.askyesno("Sair", "Deseja encerrar o sistema?"):
            self.janela.quit()
            self.janela.destroy()

    def iniciar(self):
        self.janela.mainloop()
