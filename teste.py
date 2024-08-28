from flask import Flask, request, render_template

class Funcionario:
    def __init__(self, nome, cpf, cargo):
        self.nome = nome
        self.cpf = cpf
        self.cargo = cargo
        self.registros_ponto = []

class RegistroPonto:
    def __init__(self, data, hora_entrada, hora_saida):
        self.data = data
        self.hora_entrada = hora_entrada
        self.hora_saida = hora_saida

class SistemaControlePonto:
    def __init__(self):
        self.funcionarios = []

    def cadastrar_funcionario(self, nome, cpf, cargo):
        funcionario = Funcionario(nome, cpf, cargo)
        self.funcionarios.append(funcionario)
        return funcionario

    def registrar_ponto(self, cpf, data, hora_entrada, hora_saida):
        for funcionario in self.funcionarios:
            if funcionario.cpf == cpf:
                registro_ponto = RegistroPonto(data, hora_entrada, hora_saida)
                funcionario.registros_ponto.append(registro_ponto)
                return registro_ponto
        return None

    def consultar_registros_ponto(self, cpf):
        for funcionario in self.funcionarios:
            if funcionario.cpf == cpf:
                return funcionario.registros_ponto
        return []

    def verificar_cpf(self, cpf):
        for funcionario in self.funcionarios:
            if funcionario.cpf == cpf:
                return True
        return False

app = Flask(__name__)

sistema = SistemaControlePonto()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastrar_funcionario", methods=["POST"])
def cadastrar_funcionario():
    nome = request.form["nome"]
    cpf = request.form["cpf"]
    cargo = request.form["cargo"]
    
    # Verificar se o CPF já existe
    if sistema.verificar_cpf(cpf):
        return "CPF já existe!"
    
    funcionario = sistema.cadastrar_funcionario(nome, cpf, cargo)
    return "Funcionário cadastrado com sucesso!"

@app.route("/registrar_ponto", methods=["POST"])
def registrar_ponto():
    cpf = request.form["cpf"]
    data = request.form["data"]
    hora_entrada = request.form["hora_entrada"]
    hora_saida = request.form["hora_saida"]
    
    # Verificar se o CPF existe
    if not sistema.verificar_cpf(cpf):
        return "CPF não existe!"
    
    registro_ponto = sistema.registrar_ponto(cpf, data, hora_entrada, hora_saida)
    return "Ponto registrado com sucesso!"

@app.route("/consultar_registros_ponto", methods=["POST"])
def consultar_registros_ponto():
    cpf = request.form["cpf"]
    
    # Verificar se o CPF existe
    if not sistema.verificar_cpf(cpf):
        return "CPF não existe!"
    
    registros_ponto = sistema.consultar_registros_ponto(cpf)
    return render_template("registros_ponto.html", registros_ponto=registros_ponto)

if __name__ == "__main__":
    app.run(debug=True)
    





