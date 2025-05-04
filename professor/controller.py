from flask import Blueprint, jsonify, request
from professor.model import ProfessorModel
from Util.helpers import validar_campos
import re

professores_bp = Blueprint('professores', __name__)

def validar_nome_professor(nome):
    if not isinstance(nome, str):
        return False, "Nome deve ser uma string."
    if not nome.strip():
        return False, "Nome não pode estar vazio."
    if not re.match("^[A-Za-záéíóúãõçÁÉÍÓÚÃÕÇ ]+$", nome):
        return False, "Nome inválido. Deve conter apenas letras e espaços."
    if len(nome) > 80:
        return False, "Nome não pode exceder 80 caracteres."
    return True, None

def validar_disciplina(disciplina):
    if not isinstance(disciplina, str):
        return False, "Disciplina deve ser uma string."
    if not disciplina.strip():
        return False, "Disciplina não pode estar vazia."
    if len(disciplina) > 80:
        return False, "Disciplina não pode exceder 80 caracteres."
    
    return True, None

@professores_bp.route('/professores', methods=['GET'])
def get_professores():
    professores = ProfessorModel.find_all()
    return jsonify([professor.to_dict() for professor in professores])

@professores_bp.route('/professores/<int:id_professor>', methods=['GET'])
def get_professor(id_professor):
    professor = ProfessorModel.find_by_id(id_professor)
    return jsonify(professor.to_dict())

@professores_bp.route('/professores', methods=['POST'])
def post_professor():
    dados = request.get_json()

    
    valido, erro = validar_nome_professor(dados.get('nome'))
    if not valido:
        return jsonify({'error': erro}), 400

    
    valido, erro = validar_disciplina(dados.get('disciplina'))
    if not valido:
        return jsonify({'error': erro}), 400

    professor = ProfessorModel(
        nome=dados['nome'],
        disciplina=dados.get('disciplina') 
    )
    professor.save_to_db()
    return jsonify(professor.to_dict()), 201

@professores_bp.route('/professores/<int:id_professor>', methods=['PUT'])
def put_professor(id_professor):
    dados = request.get_json()
    professor = ProfessorModel.find_by_id(id_professor)
    if not professor:
        return jsonify({'error': 'Professor não encontrado'}), 404

    
    if 'nome' in dados:
        valido, erro = validar_nome_professor(dados['nome'])
        if not valido:
            return jsonify({'error': erro}), 400
        professor.nome = dados['nome']

    
    if 'disciplina' in dados:
        valido, erro = validar_disciplina(dados['disciplina'])
        if not valido:
            return jsonify({'error': erro}), 400
        professor.disciplina = dados['disciplina']

    professor.save_to_db()
    return jsonify(professor.to_dict())

@professores_bp.route('/professores/<int:id_professor>', methods=['DELETE'])
def delete_professor(id_professor):
    professor = ProfessorModel.find_by_id(id_professor)
    if professor:
        professor.delete_from_db()
        return jsonify({'message': 'Professor excluído com sucesso'});
    return jsonify({'error': 'Professor não encontrado'}), 404