from jogoteca import app
from flask import render_template, request, redirect, session, flash, url_for
from helpers import FormularioUsuario
from models import Usuarios
from flask_bcrypt import check_password_hash

# Criando uma rota nova, que irá retornar um arquivo html com um formulário de login
@app.route('/login')
def login():
    # Recupernado o valor que foi passado pela query string, antes definida na rota "novo"
    proxima = request.args.get('proxima')
    if proxima == None:
        proxima = '/'

    form = FormularioUsuario()

    return render_template('login.html', titulo='Faça seu login', proxima=proxima, form=form)

# Criando uma rota responsável por receber a requisição do formulário de login
# Foi deifinido o methods com um array contendo o valor 'POST' para possibilitar que esta rota realiza requisições post
@app.route('/autenticar', methods=['POST', ])
def autenticar():

    form = FormularioUsuario(request.form)

    # Recuperando informações de um usuario
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    senha = check_password_hash(usuario.senha, form.senha.data)

    # Verificando se o usuario que veio do formulario de login está dentro do dicionário ceiado
    # Verificando se a senha é daquele usuário
    if usuario and senha:
        # Armazenando o usuário na session com a chave usuario_logado
        session['usuario_logado'] = usuario.nickname

        # Exibindo uma mensagem para o usuário usando o valor armazenado na sessão
        flash(f"Usuário {usuario.nickname} logado com sucesso")

        # Recuperando a informação do input hidden do formulario para saber a próxima página
        proxima_pagina = request.form['proxima']

        return redirect(proxima_pagina)
    else:
        # Exibindo uma mensagem de erro de login
        flash(f"Usuário ou senha incorretos")

        # Fazendo o redirecionamento para a função que instancia a rota (página)
        return redirect(url_for('login'))

# Criando uma nova rota para realizar loggout
@app.route('/logout')
def logout():

    # Atribuindo None para a session criada para o usuario logado
    session['usuario_logado'] = None
    # Exibindo uma mensagem de sucesso
    flash("Loggout efetuado com sucesso!")

    # Fazendo o redirecionamento para a função que instancia a rota (página)
    return redirect(url_for('index'))
