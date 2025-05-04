from flask import Blueprint, jsonify, request
from aluno.model import AlunoModel
from Util.helpers import validar_campos, validar_numeros
import re
from datetime import datetime

alunos_bp = Blueprint('alunos', __name__)


def validar_nome(nome):
    if not isinstance(nome, str) or not re.match("^[A-Za-záéíóúãõçÁÉÍÓÚÃÕÇ ]+$", nome):
        return False, "Nome inválido. Deve ser uma string contendo apenas letras e espaços."
    return True, None

def validar_data_nascimento(data):
    if not isinstance(data, str):
        return False, "Data de nascimento inválida. Deve ser uma string no formato AAAA-MM-DD."
    if not data:
        return False, "A data de nascimento não pode estar vazia."
    try:
        datetime.strptime(data, '%Y-%m-%d')
        return True, None
    except ValueError:
        return False, "Formato de data de nascimento inválido. Use o formato AAAA-MM-DD."

def validar_nota(nota):
    if not isinstance(nota, (int, float, str)):
        return False, "A nota deve ser um número."
    try:
        nota_float = float(nota)
        if 0 <= nota_float <= 10:
            return True, None
        return False, "A nota deve estar entre 0 e 10."
    except ValueError:
        return False, "A nota deve ser um número válido."

def validar_turma_id(turma_id):
    if not isinstance(turma_id, int):
        return False, "ID da turma inválido. Deve ser um número inteiro."
    if turma_id <= 0:
        return False, "ID da turma inválido. Deve ser um número inteiro positivo."
    return True, None

@alunos_bp.route('/alunos', methods=['GET'])
def get_alunos():
    alunos = AlunoModel.find_all()
    return jsonify([aluno.to_dict() for aluno in alunos])

@alunos_bp.route('/alunos/<int:id_aluno>', methods=['GET'])
def get_aluno(id_aluno):
    aluno = AlunoModel.find_by_id(id_aluno)
    return jsonify(aluno.to_dict())

@alunos_bp.route('/alunos', methods=['POST'])
def post_aluno():
    dados = request.get_json()

    
    valido, erro = validar_nome(dados.get('nome'))
    if not valido:
        return jsonify({'error': erro}), 400

    
    valido, erro = validar_data_nascimento(dados.get('data_nascimento'))
    if not valido:
        return jsonify({'error': erro}), 400

    
    valido, erro = validar_nota(dados.get('nota_primeiro_semestre'))
    if not valido:
        return jsonify({'error': f"Nota do primeiro semestre inválida: {erro}"}), 400

    
    valido, erro = validar_nota(dados.get('nota_segundo_semestre'))
    if not valido:
        return jsonify({'error': f"Nota do segundo semestre inválida: {erro}"}), 400

    
    valido, erro = validar_turma_id(dados.get('turma_id'))
    if not valido:
        return jsonify({'error': f"ID da turma inválido: {erro}"}), 400

    aluno = AlunoModel(
        nome=dados['nome'],
        data_nascimento=dados['data_nascimento'],
        nota_primeiro_semestre=float(dados['nota_primeiro_semestre']),
        nota_segundo_semestre=float(dados['nota_segundo_semestre']),
        turma_id=int(dados['turma_id'])
    )
    aluno.save_to_db()
    return jsonify(aluno.to_dict()), 201

@alunos_bp.route('/alunos/<int:id_aluno>', methods=['PUT'])
def put_aluno(id_aluno):
    dados = request.get_json()

    aluno = AlunoModel.find_by_id(id_aluno)
    if not aluno:
        return jsonify({'error': 'Aluno não encontrado'}), 404

    
    if 'nome' in dados:
        valido, erro = validar_nome(dados['nome'])
        if not valido:
            return jsonify({'error': erro}), 400
        aluno.nome = dados['nome']

    
    if 'data_nascimento' in dados:
        valido, erro = validar_data_nascimento(dados['data_nascimento'])
        if not valido:
            return jsonify({'error': erro}), 400
        aluno.data_nascimento = dados['data_nascimento']

    
    if 'nota_primeiro_semestre' in dados:
        valido, erro = validar_nota(dados['nota_primeiro_semestre'])
        if not valido:
            return jsonify({'error': f"Nota do primeiro semestre inválida: {erro}"}), 400
        aluno.nota_primeiro_semestre = float(dados['nota_primeiro_semestre'])

    
    if 'nota_segundo_semestre' in dados:
        valido, erro = validar_nota(dados['nota_segundo_semestre'])
        if not valido:
            return jsonify({'error': f"Nota do segundo semestre inválida: {erro}"}), 400
        aluno.nota_segundo_semestre = float(dados['nota_segundo_semestre'])

    
    if 'turma_id' in dados:
        valido, erro = validar_turma_id(dados['turma_id'])
        if not valido:
            return jsonify({'error': f"ID da turma inválido: {erro}"}), 400
        aluno.turma_id = int(dados['turma_id'])

    aluno.save_to_db()
    return jsonify(aluno.to_dict())

@alunos_bp.route('/alunos/<int:id_aluno>', methods=['DELETE'])
def delete_aluno(id_aluno):
    aluno = AlunoModel.find_by_id(id_aluno)
    if aluno:
        aluno.delete_from_db()
        return jsonify({'message': 'Aluno excluído com sucesso'})
    return jsonify({'error': 'Aluno não encontrado'}), 404