from flask import Blueprint, jsonify, request
from aluno.model import AlunoModel
from Util.helpers import validar_campos, validar_numeros
import re

alunos_bp = Blueprint('alunos', __name__)


def validar_nome(nome):
   
    if re.match("^[A-Za-záéíóúãõçÁÉÍÓÚÃÕÇ ]+$", nome):
        return True
    return False

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
    
    
    valido, erro = validar_campos(dados, ['nome', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre', 'turma_id'])
    if not valido:
        return jsonify({'error': erro}), 400
    
   
    valido, erro = validar_numeros(dados, ['nota_primeiro_semestre', 'nota_segundo_semestre'])
    if not valido:
        return jsonify({'error': erro}), 400

   
    if not validar_nome(dados['nome']):
        return jsonify({'error': 'Nome inválido. O nome deve conter apenas letras.'}), 400

    aluno = AlunoModel(
        nome=dados['nome'],
        data_nascimento=dados['data_nascimento'],
        nota_primeiro_semestre=dados['nota_primeiro_semestre'],
        nota_segundo_semestre=dados['nota_segundo_semestre'],
        turma_id=dados['turma_id']
    )
    aluno.save_to_db()
    return jsonify(aluno.to_dict()), 201 

@alunos_bp.route('/alunos/<int:id_aluno>', methods=['PUT'])
def put_aluno(id_aluno):
    dados = request.get_json()
    

    valido, erro = validar_campos(dados, ['nome', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre', 'turma_id'])
    if not valido:
        return jsonify({'error': erro}), 400
    
    valido, erro = validar_numeros(dados, ['nota_primeiro_semestre', 'nota_segundo_semestre'])
    if not valido:
        return jsonify({'error': erro}), 400

 
    if not validar_nome(dados['nome']):
        return jsonify({'error': 'Nome inválido. O nome deve conter apenas letras.'}), 400

    aluno = AlunoModel.find_by_id(id_aluno)
    if aluno:
        aluno.nome = dados['nome']
        aluno.data_nascimento = dados['data_nascimento']
        aluno.nota_primeiro_semestre = dados['nota_primeiro_semestre']
        aluno.nota_segundo_semestre = dados['nota_segundo_semestre']
        aluno.turma_id = dados['turma_id']
        aluno.save_to_db()
        return jsonify(aluno.to_dict()) 
    return jsonify({'error': 'Aluno não encontrado'}), 404

@alunos_bp.route('/alunos/<int:id_aluno>', methods=['DELETE'])
def delete_aluno(id_aluno):
    aluno = AlunoModel.find_by_id(id_aluno)
    if aluno:
        aluno.delete_from_db()
        return jsonify({'message': 'Aluno excluído com sucesso'})
    return jsonify({'error': 'Aluno não encontrado'}), 404
