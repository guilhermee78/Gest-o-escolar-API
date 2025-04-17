from flask import Blueprint, jsonify, request
from aluno.model import AlunoModel  # Importe o AlunoModel do SQLAlchemy
from Util.helpers import validar_campos, validar_numeros

alunos_bp = Blueprint('alunos', __name__)

@alunos_bp.route('/', methods=['GET'])
def get_alunos():
    alunos = AlunoModel.find_all()
    return jsonify([aluno.json() for aluno in alunos])

@alunos_bp.route('/<int:id_aluno>', methods=['GET'])
def get_aluno(id_aluno):
    aluno = AlunoModel.find_by_id(id_aluno)
    return jsonify(aluno.json())

@alunos_bp.route('/', methods=['POST'])
def post_aluno():
    dados = request.get_json()
    valido, erro = validar_campos(dados, ['nome', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre', 'turma_id'])
    if not valido:
        return jsonify({'error': erro}), 400
    valido, erro = validar_numeros(dados, ['nota_primeiro_semestre', 'nota_segundo_semestre'])
    if not valido:
        return jsonify({'error': erro}), 400

    aluno = AlunoModel(
        nome=dados['nome'],
        data_nascimento=dados['data_nascimento'],
        nota_primeiro_semestre=dados['nota_primeiro_semestre'],
        nota_segundo_semestre=dados['nota_segundo_semestre'],
        turma_id=dados['turma_id']
    )
    aluno.save_to_db()
    return jsonify(aluno.json()), 201

@alunos_bp.route('/<int:id_aluno>', methods=['PUT'])
def put_aluno(id_aluno):
    dados = request.get_json()
    valido, erro = validar_campos(dados, ['nome', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre', 'turma_id'])
    if not valido:
        return jsonify({'error': erro}), 400
    valido, erro = validar_numeros(dados, ['nota_primeiro_semestre', 'nota_segundo_semestre'])
    if not valido:
        return jsonify({'error': erro}), 400

    aluno = AlunoModel.find_by_id(id_aluno)
    aluno.nome = dados['nome']
    aluno.data_nascimento = dados['data_nascimento']
    aluno.nota_primeiro_semestre = dados['nota_primeiro_semestre']
    aluno.nota_segundo_semestre = dados['nota_segundo_semestre']
    aluno.turma_id = dados['turma_id']
    aluno.save_to_db()
    return jsonify(aluno.json())

@alunos_bp.route('/<int:id_aluno>', methods=['DELETE'])
def delete_aluno(id_aluno):
    aluno = AlunoModel.find_by_id(id_aluno)
    aluno.delete_from_db()
    return jsonify({'message': 'Aluno excluído com sucesso'})