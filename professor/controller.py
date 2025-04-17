from flask import Blueprint, jsonify, request
from professor.model import ProfessorModel  # Importe o ProfessorModel do SQLAlchemy
from Util.helpers import validar_campos

professores_bp = Blueprint('professores', __name__)

@professores_bp.route('/', methods=['GET'])
def get_professores():
    professores = ProfessorModel.find_all()
    return jsonify([professor.json() for professor in professores])

@professores_bp.route('/<int:id_professor>', methods=['GET'])
def get_professor(id_professor):
    professor = ProfessorModel.find_by_id(id_professor)
    return jsonify(professor.json())

@professores_bp.route('/', methods=['POST'])
def post_professor():
    dados = request.get_json()
    valido, erro = validar_campos(dados, ['nome', 'disciplina'])
    if not valido:
        return jsonify({'error': erro}), 400

    professor = ProfessorModel(
        nome=dados['nome'],
        disciplina=dados['disciplina']
    )
    professor.save_to_db()
    return jsonify(professor.json()), 201

@professores_bp.route('/<int:id_professor>', methods=['PUT'])
def put_professor(id_professor):
    dados = request.get_json()
    valido, erro = validar_campos(dados, ['nome', 'disciplina'])
    if not valido:
        return jsonify({'error': erro}), 400

    professor = ProfessorModel.find_by_id(id_professor)
    professor.nome = dados['nome']
    professor.disciplina = dados['disciplina']
    professor.save_to_db()
    return jsonify(professor.json())

@professores_bp.route('/<int:id_professor>', methods=['DELETE'])
def delete_professor(id_professor):
    professor = ProfessorModel.find_by_id(id_professor)
    professor.delete_from_db()
    return jsonify({'message': 'Professor excluído com sucesso'})