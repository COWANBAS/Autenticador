import pyotp
import time
import os
import json

ARQUIVO = "contas.json"

def carregar_contas():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r") as f:
            return json.load(f)
    return {}

def salvar_contas(contas):
    with open(ARQUIVO, "w") as f:
        json.dump(contas, f)

def adicionar_conta():
    nome = input("Nome da conta: ")
    secret = input("Chave secreta: ").replace(" ", "")
    contas = carregar_contas()
    contas[nome] = secret
    salvar_contas(contas)
    print("Conta adicionada!")

def mostrar_codigos():
    contas = carregar_contas()
    if not contas:
        print("Nenhuma conta cadastrada.")
        return

    while True:
        os.system("clear")
        print("=== AUTENTICADOR LINUX ===\n")

        restante = 30 - int(time.time()) % 30

        for nome, secret in contas.items():
            totp = pyotp.TOTP(secret)
            print(f"{nome}: {totp.now()}")

        print(f"\nExpira em: {restante} segundos")
        time.sleep(1)

def menu():
    while True:
        print("\n1 - Adicionar conta")
        print("2 - Mostrar códigos")
        print("3 - Sair")
        opcao = input("Escolha: ")

        if opcao == "1":
            adicionar_conta()
        elif opcao == "2":
            mostrar_codigos()
        elif opcao == "3":
            break

if __name__ == "__main__":
    menu()
