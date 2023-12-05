# Arquivo onde iremos tratar das rotas da nossa aplicação
from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app, db
from models import Jogos, Usuarios
from helpers import recupera_imagem, deleta_arquivo, FormularioJogo, FormularioUsuario
import time

# render_template = Renderizar uma página html, possibilitando passagem de parâmetros
# request = nos auxilia em receber requisições post do servidor
# redirect = faz o redirecionamento para uma rota passada por parâmetro
# session = guardar informações no navegador (cookies)
# flash = usado para exibir uma mensagem para o usuário
# url_for = A função url_for serve para que a url do arquivo seja encontrada de acordo com o nome dele e a pasta em que ele está, independentemente da hierarquia dele, o primeiro parâmetro é a pasta e o "filename" é o nome do arquivo. São as URLs dinâmicas.
# send_from_directory = função para retornar alguma coisa de algum diretório

# Criando a página index
@app.route('/')
def index():

    # Recuperando lista de jogos a partir da model
    listaJogos = Jogos.query.order_by(Jogos.id)

    # Renderizando a página html com as variáveis
    return render_template('lista.html', titulo='Jogos', jogos=listaJogos)

# Criando umaa rota nova, que irá retornar um arquivo html com um formulário
@app.route('/novo')
def novo():
    # Verificando se NÂO há a chave usuario_logado na session ou a chave é None
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        # Fazendo o redirecionamento para a função que instancia a rota (página)
        # E Informando através de query string (?), qual é a página que eu estou tentando acessar, porém com a url for precisamos passar através de variáveis
        return redirect(url_for('login', proxima=url_for('novo')))
    
    form = FormularioJogo()
    
    # Renderizando a página html com as variáveis
    return render_template('novo.html', titulo='Novo Jogo', form= form)

# Criando uma rota responsável por receber a requisição do formulário de cadastro de jogo
# Foi deifinido o methods com um array contendo o valor 'POST' para possibilitar que esta rota realiza requisições post
@app.route('/criar', methods=['POST', ])
def criar():
    # Recuperando informações do formulário de acordo com o name do input e armazenando em variáveis
    form = FormularioJogo(request.form)
    
    if not form.validate_on_submit():
        return redirect(url_for('novo'))
    
    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data

    # Verificando se há um jogo com este nome
    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash('Jogo já existente')

        return redirect(url_for('index'))
    
    # Cadastrando um novo jogo    
    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa_{novo_jogo.id}-{timestamp}.jpg')

    # Fazendo o redirecionamento para a função que instancia a rota (página)
    return redirect(url_for('index'))

# Criando uma rota nova, que irá renderizar a página para editar um jogo
@app.route('/editar/<int:id>')
def editar(id):
    # Verificando se NÂO há a chave usuario_logado na session ou a chave é None
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        # Fazendo o redirecionamento para a função que instancia a rota (página)
        # E Informando através de query string (?), qual é a página que eu estou tentando acessar, porém com a url for precisamos passar através de variáveis
        return redirect(url_for('login', proxima=url_for('editar')))
    
    # Recuperando informações do jogo pelo id passado pela url
    jogo = Jogos.query.filter_by(id=id).first()

    form = FormularioJogo()
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console

    capa_jogo = recupera_imagem(id)
    
    # Renderizando a página html com as variáveis
    return render_template('editar.html', titulo='Editar Jogo', id=id, capa_jogo=capa_jogo, form=form)

@app.route('/atualizar', methods=['POST', ])
def atualizar():
    # Recuperando informações do formulário
    form = FormularioJogo(request.form)

    if form.validate_on_submit():
        id = request.form['id']
        nome = form.nome.data
        categoria = form.categoria.data
        console = form.console.data

        # Definindo novos valores a partir do valor recuperado
        jogo = Jogos.query.filter_by(id=id).first()
        jogo.nome = nome
        jogo.categoria = categoria
        jogo.console = console

        # Registrando alteração
        db.session.add(jogo)
        db.session.commit()

        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_arquivo(jogo.id)
        arquivo.save(f'{upload_path}/capa_{jogo.id}-{timestamp}.jpg')

    return redirect(url_for("index"))

@app.route('/deletar/<int:id>')
def deletar(id):
    # Verificando se NÂO há a chave usuario_logado na session ou a chave é None
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        # Fazendo o redirecionamento para a função que instancia a rota (página)
        # E Informando através de query string (?), qual é a página que eu estou tentando acessar, porém com a url for precisamos passar através de variáveis
        return redirect(url_for('login'))
    
    # Filtrando pelo jogo passado pela url e ja deletando ele
    Jogos.query.filter_by(id=id).delete()

    # Registrando exclusão
    db.session.commit()

    flash("Jogo deletado com sucesso")

    return redirect(url_for('index'))

# Criando uma rota nova, que irá retornar um arquivo html com um formulário de login
@app.route('/login')
def login():
    # Recupernado o valor que foi passado pela query string, antes definida na rota "novo"
    proxima = request.args.get('proxima')
    if proxima == None:
        proxima = '/'

    form = FormularioUsuario

    return render_template('login.html', titulo='Faça seu login', proxima=proxima, form=form)

# Criando uma rota responsável por receber a requisição do formulário de login
# Foi deifinido o methods com um array contendo o valor 'POST' para possibilitar que esta rota realiza requisições post
@app.route('/autenticar', methods=['POST', ])
def autenticar():

    form = FormularioUsuario(request.form)

    # Recuperando informações de um usuario
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()

    # Verificando se o usuario que veio do formulario de login está dentro do dicionário ceiado
    if usuario:
        # Verificando se a senha é daquele usuário
        if form.senha.data == usuario.senha:
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
    else:
        # Exibindo uma mensagem de erro de login
        flash(f"O Usuário não existe")

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

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):

    return send_from_directory('uploads', nome_arquivo)