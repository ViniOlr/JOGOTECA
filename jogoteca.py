from flask import Flask, render_template, request, redirect, session, flash, url_for
# Flask = Instancia a aplicação
# Renderizar uma página html, possibilitando passagem de parâmetros
# request = nos auxilia em receber requisições post do servidor
# redirect = faz o redirecionamento para uma rota passada por parâmetro
# session = guardar informações no navegador (cookies)
# flash = usado para exibir uma mensagem para o usuário
# url_for = A função url_for serve para que a url do arquivo seja encontrada de acordo com o nome dele e a pasta em que ele está, independentemente da hierarquia dele, o primeiro parâmetro é a pasta e o "filename" é o nome do arquivo. São as URLs dinâmicas.



# Classe parea definir um Jogo
class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome=nome
        self.categoria=categoria
        self.console=console 

# Classe para usuário
class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome=nome
        self.nickname=nickname
        self.senha=senha

# Instanciando jogos em variáveis globais
jogo1 = Jogo('Tretris', 'Puzzle', 'Ataria')
jogo2 = Jogo('God of War', 'Rack n Slash', 'PlayStation')
jogo3 = Jogo('Mortal Kombate', 'Luta', 'PlayStation')

listaJogos = [jogo1, jogo2, jogo3]

# Instanciando usuários inicias
usuario1 = Usuario('Vinicius', 'Vini', '123')
usuario2 = Usuario('Fulano', 'Ful', '456')
usuario3 = Usuario('Ciclano', 'Cic', '789')

usuarios = {
    usuario1.nickname : usuario1,
    usuario2.nickname : usuario2,
    usuario3.nickname : usuario3,
}

# Iniciar uma aplicaçlão Flask 
app = Flask(__name__)

# Definindo um secret key para utilizar a session de uma forma segura
app.secret_key = 'alura'

# Criando a página index
@app.route('/')
def index():    
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
    
    # Renderizando a página html com as variáveis
    return render_template('novo.html', titulo='Novo Jogo')


# Criando uma rota responsável por receber a requisição do formulário de cadastro de jogo
# Foi deifinido o methods com um array contendo o valor 'POST' para possibilitar que esta rota realiza requisições post
@app.route('/criar', methods=['POST', ])
def criar():
    # Recuperando informações do formulário de acordo com o name do input e armazenando em variáveis
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    # Instanciando um jogo com as variáveis
    jogo = Jogo(nome, categoria, console)

    # Adicionando um jogo
    listaJogos.append(jogo)

    # Fazendo o redirecionamento para a função que instancia a rota (página)
    return redirect(url_for('index'))


# Criando uma rota nova, que irá retornar um arquivo html com um formulário de login
@app.route('/login')
def login():
    # Recupernado o valor que foi passado pela query string, antes definida na rota "novo"
    proxima = request.args.get('proxima')
    if proxima == None:
        proxima = '/'

    return render_template('login.html', titulo='Faça seu login', proxima=proxima)


# Criando uma rota responsável por receber a requisição do formulário de login
# Foi deifinido o methods com um array contendo o valor 'POST' para possibilitar que esta rota realiza requisições post
@app.route('/autenticar', methods=['POST', ])
def autenticar():

    # Verificando se o usuario que veio do formulario de login está dentro do dicionário ceiado
    if request.form['usuario'] in usuarios:
        # Recuperando informações do usuario no dicionaio pelo nickname dele
        usuario = usuarios[request.form['usuario']]
        # Verificando se a senha é daquele usuário
        if request.form['senha'] == usuario.senha:
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


# Rodando a aplicação
# O debug é para recompilar assim que salvar algum arquivo
app.run(debug=True)