import pyotp
import time
import os
import json

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
        
if __name__ == "__main__":
    app = Autenticador()
