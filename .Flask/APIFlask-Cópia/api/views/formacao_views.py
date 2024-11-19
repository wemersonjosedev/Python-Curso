from flask_restful import Resource
from api import api
from ..schemas import formacao_schema
from flask import request, make_response, jsonify
from ..entidades import formacao
from ..services import formacao_service
from ..paginate import paginate
from ..models.formacao_model import Formacao
from flask_jwt_extended import jwt_required
from ..decorator import admin_required

class FormacaoList(Resource):

    @jwt_required()
    def get(self):
        fs = formacao_schema.FormacaoSchema(many=True)
        return paginate(Formacao, fs)

    @admin_required
    def post(self):
        fs = formacao_schema.FormacaoSchema()
        validate = fs.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            descricao = request.json["descricao"]
            professores = request.json["professores"]
            nova_formacao = formacao.Formacao(nome=nome, descricao=descricao, professores=professores)
            resultado = formacao_service.cadastrar_formacao(nova_formacao)
            x = fs.jsonify(resultado)
            return make_response(x, 201)

class FormacaoDetail(Resource):

    @jwt_required()
    def get(self, id):
        formacao = formacao_service.listar_formacao_id(id)
        if formacao is None:
            return make_response(jsonify("Formação não foi encontrado"), 404)
        fs = formacao_schema.FormacaoSchema()
        return make_response(fs.jsonify(formacao), 200)

    @admin_required
    def put(self, id):
        formacao_bd = formacao_service.listar_formacao_id(id)
        if formacao_bd is None:
            return make_response(jsonify("Formação não foi encontrado"), 404)
        fs = formacao_schema.FormacaoSchema()
        validate = fs.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            descricao = request.json["descricao"]
            professores = request.json["professores"]
            nova_formacao = formacao.Formacao(nome=nome, descricao=descricao, professores=professores)
            formacao_service.atualiza_formacao(formacao_bd, nova_formacao)
            formacao_atualizada = formacao_service.listar_formacao_id(id)
            return make_response(fs.jsonify(formacao_atualizada), 200)

    @admin_required
    def delete(self, id):
        formacao_bd = formacao_service.listar_formacao_id(id)
        if formacao_bd is None:
            return make_response(jsonify("Formação não encontrada"), 404)
        formacao_service.remove_formacao(formacao_bd)
        return make_response('Formação excluída com sucesso', 204)

api.add_resource(FormacaoList, '/formacoes')
api.add_resource(FormacaoDetail, '/formacoes/<int:id>')