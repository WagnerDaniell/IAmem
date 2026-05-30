import customtkinter as ctk

#Aparência
ctk.set_appearance_mode("dark")

#Tema
ctk.set_default_color_theme("blue")

#Janela
app = ctk.CTk()

app.geometry("1280x720")
app.title("IAmém")

#Sidebar

sidebar = ctk.CTkFrame(
    app,
    width=250,
    corner_radius=0
)

sidebar.pack(side="left", fill="y")

# Título do sistema
logo = ctk.CTkLabel(
    sidebar,
    text="IAmém",
    font=("Segoe UI", 28, "bold")
)

logo.pack(pady=40)

def limpar_frame():
    for widget in main_frame.winfo_children():
        widget.destroy()

def mostrar_dashboard():
    limpar_frame()

    titulo = ctk.CTkLabel(
        main_frame,
        text="Dashboard",
        font=("Segoe UI", 32, "bold")
    )

    titulo.pack(pady=40)


def mostrar_integrantes():
    limpar_frame()

    titulo = ctk.CTkLabel(
        main_frame,
        text="Integrantes",
        font=("Segoe UI", 32, "bold")
    )

    titulo.pack(pady=40)


def mostrar_escalas():
    limpar_frame()

    titulo = ctk.CTkLabel(
        main_frame,
        text="Escalas",
        font=("Segoe UI", 32, "bold")
    )

    titulo.pack(pady=40)

#Botões do menu
btn_dashboard = ctk.CTkButton(
    sidebar,
    text="Dashboard",
    command=mostrar_dashboard
)

btn_integrantes = ctk.CTkButton(
    sidebar,
    text="Integrantes",
    command=mostrar_integrantes
)

btn_escalas = ctk.CTkButton(
    sidebar,
    text="Escalas",
    command=mostrar_escalas
)
#Posicionamento
btn_dashboard.pack(pady=10, padx=20)
btn_integrantes.pack(pady=10, padx=20)
btn_escalas.pack(pady=10, padx=20)

#Área principal

main_frame = ctk.CTkFrame(app)

main_frame.pack(
    side="right",
    fill="both",
    expand=True
)

mostrar_dashboard()

#Rodar
app.mainloop()