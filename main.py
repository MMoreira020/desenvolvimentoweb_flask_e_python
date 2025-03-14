from flask import Flask, url_for, render_template

#inicializacao
app = Flask(__name__)

# rotas
@app.route('/')
def teste():
    titulo = "Gestão de Usuários"
    usuarios = [
        {"nome": "Moisés", "mebro_ativo": True},
        {"nome": "Pedro Lemos", "mebro_ativo": False},
        {"nome": "Otávio", "mebro_ativo": False},
    ]
    return render_template("index.html", titulo=titulo, usuarios=usuarios)

@app.route('/sobre')
def pagina_sobre():
    return """
        <b>MeuGitHub</b>: acesse os repositorios no
        <a href="https://github.com/MMoreira020?tab=repositories">GitHub</a>
    """
# execucao
app.run(debug=True) # modo desenvolvedor