import customtkinter as ctk

def main():
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("IAmém — Escalas da Mídia")
    root.geometry("900x600")

    root.mainloop()
if __name__ == "__main__":
    main()