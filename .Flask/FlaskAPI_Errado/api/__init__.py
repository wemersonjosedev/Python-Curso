from flask import Flask
from flask_restful import Api, Resource

# Instância do aplicativo Flask
app = Flask(__name__)

# Instância do Api do Flask-RESTful
api = Api(app)

# Definição da classe de recurso CursoList
class CursoList(Resource):
    def get(self):
        return {"message": "Estudando API com Flask e Flask-RESTful"}

# Registro do recurso CursoList com o endpoint /cursos
api.add_resource(CursoList, '/cursos')

# Função para criar e retornar o aplicativo Flask
def create_app():
    return app