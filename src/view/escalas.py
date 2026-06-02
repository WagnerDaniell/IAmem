import customtkinter as ctk
from tkinter import messagebox
from src.services.gerador_escala import gerar_escala_semana, retreinar_modelo
from src.context.database import listar_integrantes

def mostrar_escalas(parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()

    titulo = ctk.CTkLabel(parent_frame, text="Escalas", font=("Segoe UI", 32, "bold"))
    titulo.pack(pady=(20, 10))

    btn_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    btn_frame.pack(fill="x", padx=20, pady=10)

    btn_gerar = ctk.CTkButton(
        btn_frame,
        text="Gerar Escala da Semana",
        command=lambda: gerar_e_mostrar_semana(parent_frame, resultado_frame)
    )
    btn_gerar.pack(side="left", padx=5)

    resultado_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    resultado_frame.pack(fill="both", expand=True, padx=20, pady=10)

def gerar_e_mostrar_semana(parent, result_frame):
    if not messagebox.askyesno("Gerar Escala Semanal", "Deseja gerar a escala para Quarta, Sexta e Domingo?"):
        return

    escala_semana = gerar_escala_semana()

    for widget in result_frame.winfo_children():
        widget.destroy()

    grid_frame = ctk.CTkFrame(result_frame, fg_color="transparent")
    grid_frame.pack(expand=True)

    ctk.CTkLabel(grid_frame, text="Escala da Semana", font=("Segoe UI", 20, "bold")).grid(
        row=0, column=0, columnspan=4, pady=10
    )

    dias = ["Domingo", "Quarta", "Sexta"]

    # Cabeçalho dos dias
    for idx, dia in enumerate(dias, start=1):
        data, _, _ = escala_semana[dia]
        ctk.CTkLabel(
            grid_frame,
            text=f"{dia}\n({data})",
            font=("Segoe UI", 14, "bold")
        ).grid(row=1, column=idx, padx=15, pady=5)

    areas_exibicao = ["Som", "Projeção", "Fotografia"]
    areas_chave = ["Som", "Projecao", "Fotografia"]

    for i, (area_exib, chave) in enumerate(zip(areas_exibicao, areas_chave), start=2):
        ctk.CTkLabel(
            grid_frame, text=area_exib,
            font=("Segoe UI", 13, "bold")
        ).grid(row=i, column=0, sticky="w", padx=10, pady=5)

        for j, dia in enumerate(dias, start=1):   # dia correto agora
            data, areas_dict, _ = escala_semana[dia]
            nome = areas_dict.get(chave)
            texto = nome if nome else "—"

            cell_frame = ctk.CTkFrame(grid_frame, fg_color="transparent")
            cell_frame.grid(row=i, column=j, padx=5, pady=2)

            lbl = ctk.CTkLabel(cell_frame, text=texto, font=("Segoe UI", 13))
            lbl.pack(side="left")

            if nome:
                # Encontra ID do integrante
                integrante_id = None
                for integ in listar_integrantes():
                    if integ[1] == nome and integ[2] == chave:
                        integrante_id = integ[0]
                        break

                if integrante_id:
                    btn_good = ctk.CTkButton(
                        cell_frame, text="👍", width=30, fg_color="green",
                        command=lambda d=data, a=chave, i=integrante_id, v=1: avaliar(d, a, i, v)
                    )
                    btn_good.pack(side="left", padx=2)

                    btn_bad = ctk.CTkButton(
                        cell_frame, text="👎", width=30, fg_color="#C0392B",
                        command=lambda d=data, a=chave, i=integrante_id, v=0: avaliar(d, a, i, v)
                    )
                    btn_bad.pack(side="left", padx=2)

def avaliar(data, area, integrante_id, avaliacao):
    import sqlite3
    from src.context.database import DB_PATH
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE feedback_escala SET avaliacao = ?
        WHERE data_escala = ? AND area = ? AND integrante_id = ?
          AND avaliacao IS NULL
          AND id = (
              SELECT id FROM feedback_escala
              WHERE data_escala = ? AND area = ? AND integrante_id = ?
              ORDER BY id DESC LIMIT 1
          )
    ''', (avaliacao, data, area, integrante_id, data, area, integrante_id))
    conn.commit()
    conn.close()

    retreinar_modelo()
    messagebox.showinfo("Feedback", "Avaliação registrada e IA atualizada!")
