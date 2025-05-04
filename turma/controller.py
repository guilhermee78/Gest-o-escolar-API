from flask import Blueprint, jsonify, request
from turma.model import TurmaModel
from professor.model import ProfessorModel
from Util.helpers import validar_campos
import re

turmas_bp = Blueprint('turmas', __name__)

def validar_nome_turma(nome):
    if not isinstance(nome, str):
        return False, "Nome da turma deve ser uma string."
    if not nome.strip():
        return False, "Nome da turma não pode estar vazio."
    if len(nome) > 80:
        return False, "Nome da turma não pode exceder 80 caracteres."
    return True, None

def validar_turno(turno):
    if turno is not None and not isinstance(turno, str):
        return False, "Turno deve ser uma string."
    if turno is not None and len(turno) > 20:
        return False, "Turno não pode exceder 20 caracteres."
    turnos_permitidos = ["Manhã", "Tarde", "Noite", "Integral"]
    if turno is not None and turno not in turnos_permitidos:
        return False, f"Turno inválido. Deve ser um dos seguintes: {', '.join(turnos_permitidos)}."
    return True, None

def validar_professor_id(professor_id):
    if not isinstance(professor_id, int):
        return False, "ID do professor deve ser um número inteiro."
    if professor_id <= 0:
        return False, "ID do professor deve ser um número inteiro positivo."
    return True, None

@turmas_bp.route('/turmas', methods=['GET'])
def get_turmas():
    turmas = TurmaModel.find_all()
    return jsonify([turma.to_dict() for turma in turmas])

@turmas_bp.route('/turmas/<int:id_turma>', methods=['GET'])
def get_turma(id_turma):
    turma = TurmaModel.find_by_id(id_turma)
    if turma:
        return jsonify(turma.to_dict())
    return jsonify({'error': 'Turma não encontrada'}), 404

@turmas_bp.route('/turmas', methods=['POST'])
def post_turma():
    if request.content_type != 'application/json':
        print(f"Content-Type incorreto: {request.content_type}")
        return jsonify({'error': 'Content-Type deve ser application/json'}), 415

    dados = request.get_json(force=True, silent=True)
    print(f"Dados recebidos (force=True, silent=True): {dados}")

    if dados is None:
        print("Erro: Dados JSON inválidos ou não foram recebidos.")
        return jsonify({'error': 'Dados JSON inválidos'}), 400

    if 'nome' not in dados:
        return jsonify({'error': 'O campo nome é obrigatório.'}), 400
    if 'professor_id' not in dados:
        return jsonify({'error': 'O campo professor_id é obrigatório.'}), 400

    # Validação do nome
    valido, erro = validar_nome_turma(dados['nome'])
    if not valido:
        return jsonify({'error': erro}), 400

    # Validação do turno (opcional, mas valida se presente)
    turno = None
    if 'turno' in dados:
        valido, erro = validar_turno(dados['turno'])
        if not valido:
            return jsonify({'error': erro}), 400
        turno = dados['turno']

    # Validação do professor_id
    valido, erro = validar_professor_id(dados['professor_id'])
    if not valido:
        return jsonify({'error': erro}), 400

    # Verificar se o professor_id existe no banco de dados
    professor = ProfessorModel.find_by_id(dados['professor_id'])
    if not professor:
        return jsonify({'error': f"Professor com ID {dados['professor_id']} não encontrado."}), 400

    turma = TurmaModel(
        nome=dados['nome'],
        turno=turno,
        professor_id=dados['professor_id']
    )
    turma.save_to_db()
    return jsonify(turma.to_dict()), 201

@turmas_bp.route('/turmas/<int:id_turma>', methods=['PUT'])
def put_turma(id_turma):
    dados = request.get_json()
    turma = TurmaModel.find_by_id(id_turma)
    if not turma:
        return jsonify({'error': 'Turma não encontrada'}), 404

    if 'nome' in dados:
        valido, erro = validar_nome_turma(dados['nome'])
        if not valido:
            return jsonify({'error': erro}), 400
        turma.nome = dados['nome']

    if 'turno' in dados:
        valido, erro = validar_turno(dados['turno'])
        if not valido:
            return jsonify({'error': erro}), 400
        turma.turno = dados['turno']

    if 'professor_id' in dados:
        valido, erro = validar_professor_id(dados['professor_id'])
        if not valido:
            return jsonify({'error': erro}), 400

        professor = ProfessorModel.find_by_id(dados['professor_id'])
        if not professor:
            return jsonify({'error': f"Professor com ID {dados['professor_id']} não encontrado."}), 400
        turma.professor_id = dados['professor_id']

    turma.save_to_db()
    return jsonify(turma.to_dict())

@turmas_bp.route('/turmas/<int:id_turma>', methods=['DELETE'])
def delete_turma(id_turma):
    turma = TurmaModel.find_by_id(id_turma)
    if turma:
        turma.delete_from_db()
        return jsonify({'message': 'Turma excluída com sucesso'})
    return jsonify({'error': 'Turma não encontrada'}), 404