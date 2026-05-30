import customtkinter as ctk
from models.database import init_db

def main():
    init_db()

    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("IAmém — Escalas da Mídia")
    root.geometry("900x600")

    root.mainloop()
if __name__ == "__main__":
    main()