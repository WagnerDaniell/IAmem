import customtkinter as ctk
from tkinter import messagebox
from src.context.database import (
    listar_integrantes,
    cadastrar_integrante,
    deletar_integrante,
    editar_integrante_completo
)

def mostrar_integrantes(parent_frame):
    """
    Monta toda a interface da aba Integrantes dentro do frame fornecido.
    parent_frame: frame principal onde os widgets serão inseridos.
    """
    # Limpa o frame antes de construir a tela
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Título
    titulo = ctk.CTkLabel(
        parent_frame,
        text="Integrantes",
        font=("Segoe UI", 32, "bold")
    )
    titulo.pack(pady=(20, 10))

    # Frame para o botão de adicionar
    top_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    top_frame.pack(fill="x", padx=20, pady=(0, 10))

    btn_adicionar = ctk.CTkButton(
        top_frame,
        text="+ Adicionar Integrante",
        command=lambda: janela_adicionar_integrante(parent_frame, atualizar_lista)
    )
    btn_adicionar.pack(side="left")

    # Frame rolável para a lista de integrantes
    scroll_frame = ctk.CTkScrollableFrame(parent_frame, width=800, height=400)
    scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def atualizar_lista():
        # Limpa o scroll_frame
        for widget in scroll_frame.winfo_children():
            widget.destroy()

        integrantes = listar_integrantes()
        if not integrantes:
            vazio = ctk.CTkLabel(
                scroll_frame,
                text="Nenhum integrante cadastrado.",
                font=("Segoe UI", 16)
            )
            vazio.pack(pady=20)
            return

        # Cabeçalho
        header = ctk.CTkFrame(scroll_frame, fg_color="gray20")
        header.pack(fill="x", pady=(0, 5))
        colunas = ["Nome", "Área", "Prioridade", "Qua", "Sex", "Dom", "Recente", "Seguido", "Ações"]
        pesos = [2, 1, 1, 1, 1, 1, 1, 1, 2]
        for col, peso in zip(colunas, pesos):
            lbl = ctk.CTkLabel(header, text=col, font=("Segoe UI", 13, "bold"))
            lbl.pack(side="left", expand=True, fill="x", padx=2)

        for integrante in integrantes:
            id_, nome, area, prioridade, disp_quarta, disp_sexta, disp_domingo, recente, seguidas = integrante
            row = ctk.CTkFrame(scroll_frame, fg_color="gray17")
            row.pack(fill="x", pady=2)

            rec_texto = "Sim" if recente else "Não"

            dados = [
                nome, 
                area, 
                prioridade, 
                "✓" if disp_quarta else "✗",
                "✓" if disp_sexta else "✗",
                "✓" if disp_domingo else "✗",
                rec_texto, 
                str(seguidas)
            ]
            for dado, peso in zip(dados, pesos[:-1]):  # último peso é para ações
                lbl = ctk.CTkLabel(row, text=dado, font=("Segoe UI", 12))
                lbl.pack(side="left", expand=True, fill="x", padx=2)

            acoes_frame = ctk.CTkFrame(row, fg_color="transparent")
            acoes_frame.pack(side="left", expand=True, fill="x", padx=2)

            btn_editar = ctk.CTkButton(
                acoes_frame,
                text="Editar",
                width=60,
                font=("Segoe UI", 11),
                command=lambda i=integrante: janela_editar_integrante(parent_frame, i, atualizar_lista)
            )
            btn_editar.pack(side="left", padx=2)

            btn_excluir = ctk.CTkButton(
                acoes_frame,
                text="Excluir",
                width=60,
                fg_color="#C0392B",
                hover_color="#E74C3C",
                font=("Segoe UI", 11),
                command=lambda id_i=id_: confirmar_exclusao(id_i, atualizar_lista)
            )
            btn_excluir.pack(side="left", padx=2)

    def confirmar_exclusao(id_integrante, atualizar_callback):
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este integrante?"):
            deletar_integrante(id_integrante)
            atualizar_callback()

    # Carrega a lista inicial
    atualizar_lista()


# --- Funções de popup (mantidas no mesmo módulo para organização) ---

def janela_adicionar_integrante(parent, atualizar_callback):
    popup = ctk.CTkToplevel(parent)
    popup.title("Novo Integrante")
    popup.geometry("400x500")  # Aumentado para caber os novos campos
    popup.grab_set()

    ctk.CTkLabel(popup, text="Nome:").pack(pady=(15, 0))
    entry_nome = ctk.CTkEntry(popup, width=250)
    entry_nome.pack()

    ctk.CTkLabel(popup, text="Área:").pack(pady=(10, 0))
    area_var = ctk.StringVar(value="Som")
    opt_area = ctk.CTkOptionMenu(popup, values=["Som", "Projecao", "Fotografia"], variable=area_var)
    opt_area.pack()

    ctk.CTkLabel(popup, text="Prioridade:").pack(pady=(10, 0))
    prio_var = ctk.StringVar(value="Media")
    opt_prio = ctk.CTkOptionMenu(popup, values=["Baixa", "Media", "Alta", "Maxima"], variable=prio_var)
    opt_prio.pack()

    # Disponibilidade por dia
    ctk.CTkLabel(popup, text="Disponibilidade por dia:", font=("Segoe UI", 13, "bold")).pack(pady=(15, 5))

    disp_quarta = ctk.BooleanVar(value=True)
    chk_quarta = ctk.CTkSwitch(popup, text="Quarta-feira", variable=disp_quarta)
    chk_quarta.pack(pady=2)

    disp_sexta = ctk.BooleanVar(value=True)
    chk_sexta = ctk.CTkSwitch(popup, text="Sexta-feira", variable=disp_sexta)
    chk_sexta.pack(pady=2)

    disp_domingo = ctk.BooleanVar(value=True)
    chk_domingo = ctk.CTkSwitch(popup, text="Domingo", variable=disp_domingo)
    chk_domingo.pack(pady=2)

    # Participação recente
    rec_var = ctk.BooleanVar(value=False)
    chk_rec = ctk.CTkSwitch(popup, text="Participação recente", variable=rec_var)
    chk_rec.pack(pady=(15, 0))

    ctk.CTkLabel(popup, text="Escalas seguidas:").pack(pady=(10, 0))
    entry_seg = ctk.CTkEntry(popup, width=100)
    entry_seg.insert(0, "0")
    entry_seg.pack()

    def salvar():
        nome = entry_nome.get().strip()
        if not nome:
            messagebox.showerror("Erro", "Nome é obrigatório.")
            return
        try:
            seguidas = int(entry_seg.get())
        except ValueError:
            messagebox.showerror("Erro", "Escalas seguidas deve ser um número.")
            return

        cadastrar_integrante(
            nome=nome,
            area=area_var.get(),
            prioridade=prio_var.get(),
            disponivel_quarta=1 if disp_quarta.get() else 0,
            disponivel_sexta=1 if disp_sexta.get() else 0,
            disponivel_domingo=1 if disp_domingo.get() else 0,
            participacao_recente=1 if rec_var.get() else 0,
            escalas_seguidas=seguidas
        )
        popup.destroy()
        atualizar_callback()

    btn_salvar = ctk.CTkButton(popup, text="Salvar", command=salvar)
    btn_salvar.pack(pady=20)


def janela_editar_integrante(parent, integrante, atualizar_callback):
    # A tupla agora tem 9 elementos: id, nome, area, prioridade, disp_quarta, disp_sexta, disp_domingo, recente, seguidas
    id_, nome_atual, area_atual, prio_atual, disp_quarta_atual, disp_sexta_atual, disp_domingo_atual, rec_atual, seg_atual = integrante

    popup = ctk.CTkToplevel(parent)
    popup.title("Editar Integrante")
    popup.geometry("400x500")  # Aumentado para caber os novos campos
    popup.grab_set()

    ctk.CTkLabel(popup, text="Nome:").pack(pady=(15, 0))
    entry_nome = ctk.CTkEntry(popup, width=250)
    entry_nome.insert(0, nome_atual)
    entry_nome.pack()

    ctk.CTkLabel(popup, text="Área:").pack(pady=(10, 0))
    area_var = ctk.StringVar(value=area_atual)
    opt_area = ctk.CTkOptionMenu(popup, values=["Som", "Projecao", "Fotografia"], variable=area_var)
    opt_area.pack()

    ctk.CTkLabel(popup, text="Prioridade:").pack(pady=(10, 0))
    prio_var = ctk.StringVar(value=prio_atual)
    opt_prio = ctk.CTkOptionMenu(popup, values=["Baixa", "Media", "Alta", "Maxima"], variable=prio_var)
    opt_prio.pack()

    # Disponibilidade por dia
    ctk.CTkLabel(popup, text="Disponibilidade por dia:", font=("Segoe UI", 13, "bold")).pack(pady=(15, 5))

    disp_quarta = ctk.BooleanVar(value=bool(disp_quarta_atual))
    chk_quarta = ctk.CTkSwitch(popup, text="Quarta-feira", variable=disp_quarta)
    chk_quarta.pack(pady=2)

    disp_sexta = ctk.BooleanVar(value=bool(disp_sexta_atual))
    chk_sexta = ctk.CTkSwitch(popup, text="Sexta-feira", variable=disp_sexta)
    chk_sexta.pack(pady=2)

    disp_domingo = ctk.BooleanVar(value=bool(disp_domingo_atual))
    chk_domingo = ctk.CTkSwitch(popup, text="Domingo", variable=disp_domingo)
    chk_domingo.pack(pady=2)

    # Participação recente
    rec_var = ctk.BooleanVar(value=bool(rec_atual))
    chk_rec = ctk.CTkSwitch(popup, text="Participação recente", variable=rec_var)
    chk_rec.pack(pady=(15, 0))

    ctk.CTkLabel(popup, text="Escalas seguidas:").pack(pady=(10, 0))
    entry_seg = ctk.CTkEntry(popup, width=100)
    entry_seg.insert(0, str(seg_atual))
    entry_seg.pack()

    def salvar_edicao():
        nome = entry_nome.get().strip()
        if not nome:
            messagebox.showerror("Erro", "Nome é obrigatório.")
            return
        try:
            seguidas = int(entry_seg.get())
        except ValueError:
            messagebox.showerror("Erro", "Escalas seguidas deve ser um número.")
            return

        editar_integrante_completo(
            integrante_id=id_,
            nome=nome,
            area=area_var.get(),
            prioridade=prio_var.get(),
            disponivel_quarta=1 if disp_quarta.get() else 0,
            disponivel_sexta=1 if disp_sexta.get() else 0,
            disponivel_domingo=1 if disp_domingo.get() else 0,
            participacao_recente=1 if rec_var.get() else 0,
            escalas_seguidas=seguidas
        )
        popup.destroy()
        atualizar_callback()

    btn_salvar = ctk.CTkButton(popup, text="Salvar Alterações", command=salvar_edicao)
    btn_salvar.pack(pady=20)