from flask_restful import Resource
from api import api
from ..schemas import curso_schema
from flask import request, make_response, jsonify
from ..entidades import curso
from ..services import curso_service, formacao_service
from ..paginate import paginate
from ..models.curso_model import Curso
from flask_jwt_extended import jwt_required, get_jwt
from ..decorator import admin_required, api_key_required

class CursoList(Resource):
    # Rota para listar todos os cursos com paginação
    def get(self):
        cs = curso_schema.CursoSchema(many=True) # Define o esquema para múltiplos cursos
        return paginate(Curso, cs) # Retorna os cursos paginados

    # Rota para cadastrar um novo curso
    @admin_required
    def post(self):
        cs = curso_schema.CursoSchema() # Define o esquema para um único curso
        validate = cs.validate(request.json) # Valida os dados recebidos na requisição
        if validate:
            return make_response(jsonify(validate), 400) # Retorna erro 400 Bad Request se houver erros de validação
        else:
            nome = request.json["nome"]
            descricao = request.json["descricao"]
            data_publicacao = request.json["data_publicacao"]
            formacao = request.json["formacao"]
            formacao_curso = formacao_service.listar_formacao_id(formacao) # Busca a formação pelo ID
            if formacao_curso is None:
                return make_response(jsonify("Formação não foi encontrada"), 404) # Retorna erro 404 Not Found se a formação não for encontrada

            novo_curso = curso.Curso(nome=nome, descricao=descricao,
                                     data_publicacao=data_publicacao,
                                     formacao=formacao_curso) # Cria um novo objeto Curso
            resultado = curso_service.cadastrar_curso(novo_curso) # Cadastra o curso no banco de dados
            x = cs.jsonify(resultado) # Converte o objeto Curso em JSON
            return make_response(x, 201) # Retorna o curso criado com status 201 Created

class CursoDetail(Resource):
    # Rota para obter detalhes de um curso específico
    @jwt_required()
    def get(self, id):
        curso = curso_service.listar_curso_id(id) # Busca o curso pelo ID
        if curso is None:
            return make_response(jsonify("Curso não foi encontrado"), 404) # Retorna erro 404 Not Found se o curso não for encontrado
        cs = curso_schema.CursoSchema()
        return make_response(cs.jsonify(curso), 200) # Retorna o curso encontrado com status 200 OK

    # Rota para atualizar um curso específico
    @admin_required
    def put(self, id):
        curso_bd = curso_service.listar_curso_id(id) # Busca o curso pelo ID
        if curso_bd is None:
            return make_response(jsonify("Curso não foi encontrado"), 404) # Retorna erro 404 Not Found se o curso não for encontrado
        cs = curso_schema.CursoSchema()
        validate = cs.validate(request.json) # Valida os dados recebidos na requisição
        if validate:
            return make_response(jsonify(validate), 400) # Retorna erro 400 Bad Request se houver erros de validação
        else:
            nome = request.json["nome"]
            descricao = request.json["descricao"]
            data_publicacao = request.json["data_publicacao"]
            formacao = request.json["formacao"]
            formacao_curso = formacao_service.listar_formacao_id(formacao) # Busca a formação pelo ID
            if formacao_curso is None:
                return make_response(jsonify("Formação não foi encontrada"), 404) # Retorna erro 404 Not Found se a formação não for encontrada

            novo_curso = curso.Curso(nome=nome, descricao=descricao,
                                     data_publicacao=data_publicacao,
                                     formacao=formacao_curso) # Cria um novo objeto Curso com os dados atualizados
            curso_service.atualiza_curso(curso_bd, novo_curso) # Atualiza o curso no banco de dados
            curso_atualizado = curso_service.listar_curso_id(id) # Busca o curso atualizado pelo ID
            return make_response(cs.jsonify(curso_atualizado), 200) # Retorna o curso atualizado com status 200 OK

    # Rota para excluir um curso específico
    def delete(self, id):
        curso_bd = curso_service.listar_curso_id(id) # Busca o curso pelo ID
        if curso_bd is None:
            return make_response(jsonify("Curso não encontrado"), 404) # Retorna erro 404 Not Found se o curso não for encontrado
        curso_service.remove_curso(curso_bd) # Remove o curso do banco de dados
        return make_response(jsonify(mensagem='Curso excluído com sucesso'), 204) # Retorna status 204 No Content

# Adiciona as rotas à API
api.add_resource(CursoList, '/cursos')
api.add_resource(CursoDetail, '/cursos/<int:id>')