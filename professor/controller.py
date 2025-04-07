from flask import Blueprint, jsonify, request
from professor.model import (
    listar_professores,
    buscar_professor,
    criar_professor,
    atualizar_professor,
    excluir_professor,
    ProfessorNaoEncontrado
)
from Util.helpers import gerar_id, validar_campos

professores_bp = Blueprint('professores', __name__)

@professores_bp.route('/', methods=['GET'])
def get_professores():
    return jsonify(listar_professores())

@professores_bp.route('/<int:id_professor>', methods=['GET'])
def get_professor(id_professor):
    try:
        professor = buscar_professor(id_professor)
        return jsonify(professor)
    except ProfessorNaoEncontrado:
        return jsonify({'error': 'Professor não encontrado'}), 404

@professores_bp.route('/', methods=['POST'])
def post_professor():
    dados = request.get_json()
    valido, erro = validar_campos(dados, ['nome', 'disciplina'])
    if not valido:
        return jsonify({'error': erro}), 400

    dados['id'] = gerar_id(listar_professores())
    professor = criar_professor(dados)
    return jsonify(professor), 201

@professores_bp.route('/<int:id_professor>', methods=['PUT'])
def put_professor(id_professor):
    dados = request.get_json()
    valido, erro = validar_campos(dados, ['nome', 'disciplina'])
    if not valido:
        return jsonify({'error': erro}), 400

    try:
        professor = atualizar_professor(id_professor, dados)
        return jsonify(professor)
    except ProfessorNaoEncontrado:
        return jsonify({'error': 'Professor não encontrado'}), 404

@professores_bp.route('/<int:id_professor>', methods=['DELETE'])
def delete_professor(id_professor):
    try:
        excluir_professor(id_professor)
        return jsonify({'message': 'Professor excluído com sucesso'})
    except ProfessorNaoEncontrado:
        return jsonify({'error': 'Professor não encontrado'}), 404
