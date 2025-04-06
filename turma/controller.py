from flask import Blueprint, jsonify, request
from turma.model import turmas
from Util.helpers import gerar_id, validar_campos

turmas_bp = Blueprint('turmas', __name__)

@turmas_bp.route('/', methods=['GET'])
def get_turmas():
    return jsonify(turmas)

@turmas_bp.route('/<int:id_turma>', methods=['GET'])
def get_turma(id_turma):
    turma = next((t for t in turmas if t['id'] == id_turma), None)
    if not turma:
        return jsonify({'error': 'Turma não encontrada'}), 404
    return jsonify(turma)

@turmas_bp.route('/', methods=['POST'])
def post_turma():
    dados = request.get_json()
    valido, erro = validar_campos(dados, ['nome', 'turno', 'professor_id'])
    if not valido:
        return jsonify({'error': erro}), 400

    turma = {
        'id': gerar_id(turmas),
        'nome': dados['nome'],
        'turno': dados['turno'],
        'professor_id': dados['professor_id']
    }
    turmas.append(turma)
    return jsonify(turma), 201

@turmas_bp.route('/<int:id_turma>', methods=['PUT'])
def put_turma(id_turma):
    turma = next((t for t in turmas if t['id'] == id_turma), None)
    if not turma:
        return jsonify({'error': 'Turma não encontrada'}), 404

    dados = request.get_json()
    valido, erro = validar_campos(dados, ['nome', 'ano'])
    if not valido:
        return jsonify({'error': erro}), 400

    turma.update({
        'nome': dados['nome'],
        'ano': dados['ano']
    })
    return jsonify(turma)

@turmas_bp.route('/<int:id_turma>', methods=['DELETE'])
def delete_turma(id_turma):
    turma = next((t for t in turmas if t['id'] == id_turma), None)
    if not turma:
        return jsonify({'error': 'Turma não encontrada'}), 404
    turmas.remove(turma)
    return jsonify({'message': 'Turma excluída com sucesso'})
