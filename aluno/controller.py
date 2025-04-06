from flask import Blueprint, jsonify, request
from aluno.model import alunos
from Util.helpers import gerar_id, validar_campos, validar_numeros

alunos_bp = Blueprint('alunos', __name__)

@alunos_bp.route('/', methods=['GET'])
def get_alunos():
    return jsonify(alunos)

@alunos_bp.route('/<int:id_aluno>', methods=['GET'])
def get_aluno(id_aluno):
    aluno = next((a for a in alunos if a['id'] == id_aluno), None)
    if not aluno:
        return jsonify({'error': 'Aluno não encontrado'}), 404
    return jsonify(aluno)

@alunos_bp.route('/', methods=['POST'])
def post_aluno():
    dados = request.get_json()
    valido, erro = validar_campos(dados, ['nome', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre', 'turma_id'])
    if not valido:
        return jsonify({'error': erro}), 400
    valido, erro = validar_numeros(dados, ['nota_primeiro_semestre', 'nota_segundo_semestre'])
    if not valido:
        return jsonify({'error': erro}), 400

    aluno = {
        'id': gerar_id(alunos),
        'nome': dados['nome'],
        'data_nascimento': dados['data_nascimento'],
        'nota_primeiro_semestre': dados['nota_primeiro_semestre'],
        'nota_segundo_semestre': dados['nota_segundo_semestre'],
        'media_final': (dados['nota_primeiro_semestre'] + dados['nota_segundo_semestre']) / 2,
        'turma_id': dados['turma_id']
    }
    alunos.append(aluno)
    return jsonify(aluno), 201

@alunos_bp.route('/<int:id_aluno>', methods=['PUT'])
def put_aluno(id_aluno):
    aluno = next((a for a in alunos if a['id'] == id_aluno), None)
    if not aluno:
        return jsonify({'error': 'Aluno não encontrado'}), 404

    dados = request.get_json()
    valido, erro = validar_campos(dados, ['nome', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre', 'turma_id'])
    if not valido:
        return jsonify({'error': erro}), 400
    valido, erro = validar_numeros(dados, ['nota_primeiro_semestre', 'nota_segundo_semestre'])
    if not valido:
        return jsonify({'error': erro}), 400

    aluno.update({
        'nome': dados['nome'],
        'data_nascimento': dados['data_nascimento'],
        'nota_primeiro_semestre': dados['nota_primeiro_semestre'],
        'nota_segundo_semestre': dados['nota_segundo_semestre'],
        'media_final': (dados['nota_primeiro_semestre'] + dados['nota_segundo_semestre']) / 2,
        'turma_id': dados['turma_id']
    })
    return jsonify(aluno)

@alunos_bp.route('/<int:id_aluno>', methods=['DELETE'])
def delete_aluno(id_aluno):
    aluno = next((a for a in alunos if a['id'] == id_aluno), None)
    if not aluno:
        return jsonify({'error': 'Aluno não encontrado'}), 404
    alunos.remove(aluno)
    return jsonify({'message': 'Aluno excluído com sucesso'})
