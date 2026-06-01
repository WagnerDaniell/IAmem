import customtkinter as ctk
from src.view.interface import exibirGUI
from src.context.database import init_db

def main():
    init_db()

    exibirGUI()

if __name__ == "__main__":
    main()