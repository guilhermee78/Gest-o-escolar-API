from flask import Blueprint, jsonify, request
from turma.model import TurmaModel  # Importe o TurmaModel do SQLAlchemy
from Util.helpers import validar_campos

turmas_bp = Blueprint('turmas', __name__)

@turmas_bp.route('/', methods=['GET'])
def get_turmas():
    turmas = TurmaModel.find_all()
    return jsonify([turma.json() for turma in turmas])

@turmas_bp.route('/<int:id_turma>', methods=['GET'])
def get_turma(id_turma):
    turma = TurmaModel.find_by_id(id_turma)
    return jsonify(turma.json())

@turmas_bp.route('/', methods=['POST'])
def post_turma():
    dados = request.get_json()
    valido, erro = validar_campos(dados, ['nome', 'turno', 'professor_id'])
    if not valido:
        return jsonify({'error': erro}), 400

    turma = TurmaModel(
        nome=dados['nome'],
        turno=dados['turno'],
        professor_id=dados['professor_id']
    )
    turma.save_to_db()
    return jsonify(turma.json()), 201

@turmas_bp.route('/<int:id_turma>', methods=['PUT'])
def put_turma(id_turma):
    dados = request.get_json()
    valido, erro = validar_campos(dados, ['nome', 'turno', 'professor_id'])
    if not valido:
        return jsonify({'error': erro}), 400

    turma = TurmaModel.find_by_id(id_turma)
    if 'nome' in dados:
        turma.nome = dados['nome']
    if 'turno' in dados:
        turma.turno = dados['turno']
    if 'professor_id' in dados:
        turma.professor_id = dados['professor_id']
    turma.save_to_db()
    return jsonify(turma.json())

@turmas_bp.route('/<int:id_turma>', methods=['DELETE'])
def delete_turma(id_turma):
    turma = TurmaModel.find_by_id(id_turma)
    turma.delete_from_db()
    return jsonify({'message': 'Turma excluída com sucesso'})