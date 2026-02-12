from interface import Aplicacao
import tkinter as tk

def iniciar_aplicacao():
    root = tk.Tk()
    app = Aplicacao(root)
    root.mainloop()

if __name__ == "__main__":
    iniciar_aplicacao()

