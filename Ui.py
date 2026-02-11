import pyotp
import time
import os
import json
import tkinter as tk
from tkinter import simpledialog, messagebox

ARQUIVO = "contas.json"

class Autenticador:
    def __init__(self, arquivo=ARQUIVO):
        self.arquivo = arquivo
        self.contas = self.carregar_contas()

    def carregar_contas(self):
        if os.path.exists(self.arquivo):
            with open(self.arquivo, "r") as f:
                return json.load(f)
        return {}

    def salvar_contas(self):
        with open(self.arquivo, "w") as f:
            json.dump(self.contas, f)

    def adicionar_conta(self, nome, secret):
        secret = secret.replace(" ", "")
        self.contas[nome] = secret
        self.salvar_contas()

    def remover_conta(self, nome):
        if nome in self.contas:
            del self.contas[nome]
            self.salvar_contas()

    def listar_contas(self):
        return list(self.contas.keys())

    def gerar_codigo(self, nome):
        if nome not in self.contas:
            return None
        totp = pyotp.TOTP(self.contas[nome])
        return totp.now()

    def gerar_todos_codigos(self):
        codigos = {}
        for nome, secret in self.contas.items():
            totp = pyotp.TOTP(secret)
            codigos[nome] = totp.now()
        return codigos

    def tempo_restante(self):
        return 30 - int(time.time()) % 30

class Aplicacao:
    def __init__(self, root):
        self.root = root
        self.root.title("Autenticador")
        self.root.geometry("400x400")
        self.root.configure(bg='black')
        
        self.auth = Autenticador()
        
        self.frame_lista = tk.Frame(self.root, bg='black')
        self.frame_lista.pack(pady=20)
        
        self.lista_codigos = tk.Listbox(self.frame_lista, bg='#2e2e2e', fg='white', font=("Arial", 14), height=10, width=40)
        self.lista_codigos.pack(side="left")
        
        self.scrollbar = tk.Scrollbar(self.frame_lista, orient="vertical", command=self.lista_codigos.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.lista_codigos.config(yscrollcommand=self.scrollbar.set)
        
        self.botao_adicionar = tk.Button(self.root, text='+', bg='#4CAF50', fg='white', font=("Arial", 16), width=3, height=2, command=self.adicionar_conta)
        self.botao_adicionar.place(x=350, y=350)

        self.atualizar_lista()

    def adicionar_conta(self):
        nome = simpledialog.askstring("Adicionar Conta", "Nome da conta:")
        if nome:
            secret = simpledialog.askstring("Adicionar Conta", "Secret:")
            if secret:
                self.auth.adicionar_conta(nome, secret)
                self.atualizar_lista()

    def atualizar_lista(self):
        self.lista_codigos.delete(0, tk.END)
        codigos = self.auth.gerar_todos_codigos()
        
        for nome, codigo in codigos.items():
            self.lista_codigos.insert(tk.END, f"{nome}: {codigo}")

        self.root.after(30000, self.atualizar_lista)

def iniciar_aplicacao():
    root = tk.Tk()
    app = Aplicacao(root)
    root.mainloop()

if __name__ == "__main__":
    iniciar_aplicacao()
