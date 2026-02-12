import tkinter as tk
from tkinter import simpledialog, messagebox
from autenticador import Autenticador

class Aplicacao:
    def __init__(self, root):
        self.root = root
        self.root.title("Autenticador")
        self.root.geometry("360x600")  
        self.root.configure(bg='#121212')  
        self.root.resizable(False, False)

        self.auth = Autenticador()

        self.frame_lista = tk.Frame(self.root, bg='#121212')
        self.frame_lista.pack(pady=20)

        self.lista_codigos = tk.Listbox(
            self.frame_lista, bg='#2a2a2a', fg='white', 
            font=("Arial", 14), height=10, width=40, bd=0, 
            highlightthickness=0, selectmode=tk.SINGLE
        )
        self.lista_codigos.pack(side="left", fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(
            self.frame_lista, orient="vertical", command=self.lista_codigos.yview
        )
        self.scrollbar.pack(side="right", fill="y")
        self.lista_codigos.config(yscrollcommand=self.scrollbar.set)

        self.botao_adicionar = tk.Button(
            self.root, text='+', bg='#2a2a2a', fg='white', 
            font=("Arial", 16), width=3, height=2, command=self.adicionar_conta,
            bd=0, relief="flat", padx=10, pady=10
        )
        self.botao_adicionar.place(x=300, y=530)  

        self.atualizar_lista()

    def adicionar_conta(self):
        dialogo = tk.Toplevel(self.root) 
        dialogo.geometry("300x200")
        dialogo.title("Adicionar Conta")
        dialogo.configure(bg='#121212')

        tk.Label(dialogo, text="Nome da Conta:", bg='#121212', fg='white', font=("Arial", 12)).pack(pady=10)
        nome_entry = tk.Entry(dialogo, bg='#2a2a2a', fg='white', font=("Arial", 12), bd=0, highlightthickness=0)
        nome_entry.pack(pady=5)

        tk.Label(dialogo, text="Ticket (Secret):", bg='#121212', fg='white', font=("Arial", 12)).pack(pady=10)
        secret_entry = tk.Entry(dialogo, bg='#2a2a2a', fg='white', font=("Arial", 12), bd=0, highlightthickness=0)
        secret_entry.pack(pady=5)

        def salvar():
            nome = nome_entry.get()
            secret = secret_entry.get()
            if nome and secret:
                self.auth.adicionar_conta(nome, secret)
                self.atualizar_lista()
                dialogo.destroy()  
            else:
                messagebox.showerror("Erro", "Por favor, preencha todos os campos.", parent=dialogo)

        ok_button = tk.Button(dialogo, text="OK", bg='#4CAF50', fg='white', font=("Arial", 12), command=salvar)
        ok_button.pack(pady=20)

    def atualizar_lista(self):
        self.lista_codigos.delete(0, tk.END)

        codigos = self.auth.gerar_todos_codigos()

        for nome, codigo in codigos.items():
            display_text = f"{nome}: {codigo}"
            self.lista_codigos.insert(tk.END, display_text)

        self.root.after(30000, self.atualizar_lista)
