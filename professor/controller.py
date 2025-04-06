from flask import Blueprint, jsonify, request
from professor.model import professores
from Util.helpers import gerar_id, validar_campos

professores_bp = Blueprint('professores', __name__)

@professores_bp.route('/', methods=['GET'])
def get_professores():
    return jsonify(professores)

@professores_bp.route('/<int:id_professor>', methods=['GET'])
def get_professor(id_professor):
    professor = next((p for p in professores if p['id'] == id_professor), None)
    if not professor:
        return jsonify({'error': 'Professor não encontrado'}), 404
    return jsonify(professor)

@professores_bp.route('/', methods=['POST'])
def post_professor():
    dados = request.get_json()
    valido, erro = validar_campos(dados, ['nome', 'disciplina'])
    if not valido:
        return jsonify({'error': erro}), 400

    professor = {
        'id': gerar_id(professores),
        'nome': dados['nome'],
        'disciplina': dados['disciplina']
    }
    professores.append(professor)
    return jsonify(professor), 201

@professores_bp.route('/<int:id_professor>', methods=['PUT'])
def put_professor(id_professor):
    professor = next((p for p in professores if p['id'] == id_professor), None)
    if not professor:
        return jsonify({'error': 'Professor não encontrado'}), 404

    dados = request.get_json()
    valido, erro = validar_campos(dados, ['nome', 'disciplina'])
    if not valido:
        return jsonify({'error': erro}), 400

    professor.update({
        'nome': dados['nome'],
        'disciplina': dados['disciplina']
    })
    return jsonify(professor)

@professores_bp.route('/<int:id_professor>', methods=['DELETE'])
def delete_professor(id_professor):
    professor = next((p for p in professores if p['id'] == id_professor), None)
    if not professor:
        return jsonify({'error': 'Professor não encontrado'}), 404
    professores.remove(professor)
    return jsonify({'message': 'Professor excluído com sucesso'})
