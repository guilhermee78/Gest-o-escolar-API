from flask import Blueprint, jsonify, request
from aluno.model import (
    listar_alunos,
    buscar_aluno,
    criar_aluno,
    atualizar_aluno,
    excluir_aluno,
    AlunoNaoEncontrado
)
from Util.helpers import gerar_id, validar_campos, validar_numeros

alunos_bp = Blueprint('alunos', __name__)

@alunos_bp.route('/', methods=['GET'])
def get_alunos():
    return jsonify(listar_alunos())

@alunos_bp.route('/<int:id_aluno>', methods=['GET'])
def get_aluno(id_aluno):
    try:
        aluno = buscar_aluno(id_aluno)
        return jsonify(aluno)
    except AlunoNaoEncontrado:
        return jsonify({'error': 'Aluno não encontrado'}), 404

@alunos_bp.route('/', methods=['POST'])
def post_aluno():
    dados = request.get_json()
    valido, erro = validar_campos(dados, ['nome', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre', 'turma_id'])
    if not valido:
        return jsonify({'error': erro}), 400
    valido, erro = validar_numeros(dados, ['nota_primeiro_semestre', 'nota_segundo_semestre'])
    if not valido:
        return jsonify({'error': erro}), 400

    dados['id'] = gerar_id(listar_alunos())
    aluno = criar_aluno(dados)
    return jsonify(aluno), 201

@alunos_bp.route('/<int:id_aluno>', methods=['PUT'])
def put_aluno(id_aluno):
    dados = request.get_json()
    valido, erro = validar_campos(dados, ['nome', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre', 'turma_id'])
    if not valido:
        return jsonify({'error': erro}), 400
    valido, erro = validar_numeros(dados, ['nota_primeiro_semestre', 'nota_segundo_semestre'])
    if not valido:
        return jsonify({'error': erro}), 400

    try:
        aluno = atualizar_aluno(id_aluno, dados)
        return jsonify(aluno)
    except AlunoNaoEncontrado:
        return jsonify({'error': 'Aluno não encontrado'}), 404

@alunos_bp.route('/<int:id_aluno>', methods=['DELETE'])
def delete_aluno(id_aluno):
    try:
        excluir_aluno(id_aluno)
        return jsonify({'message': 'Aluno excluído com sucesso'})
    except AlunoNaoEncontrado:
        return jsonify({'error': 'Aluno não encontrado'}), 404
