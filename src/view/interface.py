import customtkinter as ctk
from src.view.integrantes import mostrar_integrantes
from src.view.escalas import mostrar_escalas

def exibirGUI():
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("IAmém — Escalas na igreja")
    root.geometry("900x600")

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

    def mostrar_welcome():
        limpar_frame()

        titulo = ctk.CTkLabel(
            main_frame,
            text="Welcome",
            font=("Segoe UI", 32, "bold")
        )

        titulo.pack(pady=40)

    def abrir_escalas():
        limpar_frame()
        mostrar_escalas(main_frame)

    def abrir_integrantes():
        limpar_frame()
        mostrar_integrantes(main_frame)

    #Botões do menu
    btn_welcome = ctk.CTkButton(
        sidebar,
        text="Welcome",
        command=mostrar_welcome
    )

    btn_integrantes = ctk.CTkButton(
        sidebar,
        text="Integrantes",
        command=abrir_integrantes
    )

    btn_escalas = ctk.CTkButton(
        sidebar,
        text="Escalas",
        command=abrir_escalas
    )
    #Posicionamento
    btn_welcome.pack(pady=10, padx=20)
    btn_integrantes.pack(pady=10, padx=20)
    btn_escalas.pack(pady=10, padx=20)

    #Área principal

    main_frame = ctk.CTkFrame(app)

    main_frame.pack(
        side="right",
        fill="both",
        expand=True
    )

    mostrar_welcome()

    #Rodar
    app.mainloop()