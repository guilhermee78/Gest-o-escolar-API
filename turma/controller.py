from flask import Blueprint, jsonify, request
from turma.model import (
    listar_turmas,
    buscar_turma,
    criar_turma,
    atualizar_turma,
    excluir_turma,
    TurmaNaoEncontrada
)
from Util.helpers import gerar_id, validar_campos

turmas_bp = Blueprint('turmas', __name__)

@turmas_bp.route('/', methods=['GET'])
def get_turmas():
    return jsonify(listar_turmas())

@turmas_bp.route('/<int:id_turma>', methods=['GET'])
def get_turma(id_turma):
    try:
        turma = buscar_turma(id_turma)
        return jsonify(turma)
    except TurmaNaoEncontrada:
        return jsonify({'error': 'Turma não encontrada'}), 404

@turmas_bp.route('/', methods=['POST'])
def post_turma():
    dados = request.get_json()
    valido, erro = validar_campos(dados, ['nome', 'turno', 'professor_id'])
    if not valido:
        return jsonify({'error': erro}), 400

    dados['id'] = gerar_id(listar_turmas())
    turma = criar_turma(dados)
    return jsonify(turma), 201

@turmas_bp.route('/<int:id_turma>', methods=['PUT'])
def put_turma(id_turma):
    dados = request.get_json()
    valido, erro = validar_campos(dados, ['nome', 'ano'])
    if not valido:
        return jsonify({'error': erro}), 400

    try:
        turma = atualizar_turma(id_turma, dados)
        return jsonify(turma)
    except TurmaNaoEncontrada:
        return jsonify({'error': 'Turma não encontrada'}), 404

@turmas_bp.route('/<int:id_turma>', methods=['DELETE'])
def delete_turma(id_turma):
    try:
        excluir_turma(id_turma)
        return jsonify({'message': 'Turma excluída com sucesso'})
    except TurmaNaoEncontrada:
        return jsonify({'error': 'Turma não encontrada'}), 404
