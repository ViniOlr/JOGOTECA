from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
# Flask = Instancia a aplicação


# Iniciar uma aplicaçlão Flask 
app = Flask(__name__)

# Fazendo configurações a partir de um aqruivo python, através de variáveis
app.config.from_pyfile('config.py')

# Instanciando o banco de dados
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

# Importantando as views
from views_game import *
from views_user import *

# Rodando a aplicação
# O debug é para recompilar assim que salvar algum arquivo
if __name__ == '__main__':
    app.run(debug=True)