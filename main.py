#pip3 install flask==0.12.2
from flask import Flask, render_template, request, redirect,session,flash, url_for

app = Flask(__name__)
app.secret_key = "alura"


class Jogo:
    def __init__(self, nome, categoria,console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha

#criando os jogos
jogo1 = Jogo("Super mario", "ação", "nitendo")
jogo2 = Jogo("Super mario", "ação", "nitendo")
lista = [jogo1,jogo2]

#criando os usuarios
usuario1 = Usuario("ste","Adna", "123")
usuario2 = Usuario("vit","Vitor", "321")
usuarios = {usuario1.id: usuario1,usuario2.id: usuario2}

@app.route("/novo")
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for("login", proxima = url_for("novo"))) #define que vc vai pra pagina de novo depois da rota de login
    return render_template('novo.html', titulo='Novo jogo')

#rota inicial
@app.route("/")
def index():
    return render_template("lista.html",titulo ="Jogos", jogos = lista)

#para criar um novo jogo
@app.route("/criar", methods =['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome,categoria,console)
    lista.append(jogo)
    return redirect(url_for("index"))

#rota para realizar o login
@app.route("/login")
def login():
    proxima = request.args.get('proxima')
    return render_template("login.html", proxima = proxima)

#para remover o usuario logado
@app.route("/logout")
def logout():
    session['usuario_logado'] = None
    flash("Usuario removido")
    return redirect(url_for("index"))

#para autenticar se a senha do usuario está correta
@app.route("/autenticar", methods=["Post",])
def autenticar():
    #verificando se o usuario existe e está correto
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if usuario.senha == request.form["senha"]:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + " Logou com sucesso")
            proxima_pagina = request.form["proxima"]
            if proxima_pagina == "None":
                return redirect(url_for("index"))
            return redirect(proxima_pagina)
    else:
        flash("Não logado")
        return redirect(url_for("login"))

app.run(debug=True)#para n ter q ficar compilando o codigo varias e varias vezes então colocar o "debug=True" dentro do run


#usuario.senha == request.form["senha"]