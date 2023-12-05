import os

# Definindo um secret key para utilizar a session de uma forma segura
SECRET_KEY = 'alura'

# Configurações do banco de dados
SQLALCHEMY_DATABASE_URI = \
    'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(
        user='root',
        password='admin',
        server='localhost',
        database='jogoteca'
    )

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'