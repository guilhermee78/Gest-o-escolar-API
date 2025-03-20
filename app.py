from flask import Flask, jsonify, request 

app = Flask(__name__)

alunos = [
    {'id': 1, 'nome': 'Ezequiel', 'data_nascimento': '2000-01-01', 'nota_primeiro_semestre': 7.5, 'nota_segundo_semestre': 8.0, 'media_final': 7.75, 'turma_id': 1},
    {'id': 2, 'nome': 'Jhow', 'data_nascimento': '2001-05-23', 'nota_primeiro_semestre': 6.0, 'nota_segundo_semestre': 7.0, 'media_final': 6.5, 'turma_id': 2},
    {'id': 3, 'nome': 'Maria', 'data_nascimento': '2000-11-15', 'nota_primeiro_semestre': 8.5, 'nota_segundo_semestre': 9.0, 'media_final': 8.75, 'turma_id': 3}
]

professores = [
    {'id': 1, 'nome': 'Julio', 'data_nascimento': '1985-06-12', 'disciplina': 'Matemática', 'salario': 5000},
    {'id': 2, 'nome': 'Bambam', 'data_nascimento': '1990-07-20', 'disciplina': 'História', 'salario': 4500},
    {'id': 3, 'nome': 'Sandra', 'data_nascimento': '1982-02-28', 'disciplina': 'Ciências', 'salario': 4800}
]

turmas = [
    {'id': 1, 'nome': 'Turma A', 'turno': 'Manhã', 'professor_id': 1},
    {'id': 2, 'nome': 'Turma B', 'turno': 'Tarde', 'professor_id': 2},
    {'id': 3, 'nome': 'Turma C', 'turno': 'Noite', 'professor_id': 3}
]

def gerar_id(lista):
    return len(lista) + 1 if lista else 1

def validar_campos(dados, campos_obrigatorios):
    for campo in campos_obrigatorios:
        if campo not in dados or dados[campo] is None:
            return False, f"O campo '{campo}' é obrigatório."
    return True, None

def validar_numeros(dados, campos_numericos):
    for campo in campos_numericos:
        if dados.get(campo) is not None and not isinstance(dados[campo], (int, float)):
            return False, f"O campo '{campo}' deve ser um número."
        if dados.get(campo, 0) < 0:
            return False, f"O campo '{campo}' deve ser um número positivo."
    return True, None
@app.route('/alunos', methods=['GET'])
def get_alunos():
    return jsonify(alunos)

@app.route('/alunos/<int:id_aluno>', methods=['GET'])
def get_aluno(id_aluno):
    aluno = next((a for a in alunos if a['id'] == id_aluno), None)
    if not aluno:
        return jsonify({'error': 'Aluno não encontrado'}), 404
    return jsonify(aluno)

@app.route('/alunos', methods=['POST'])
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

@app.route('/alunos/<int:id_aluno>', methods=['PUT'])
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
    return jsonify(aluno), 200

@app.route('/alunos/<int:id_aluno>', methods=['DELETE'])
def delete_aluno(id_aluno):
    aluno = next((a for a in alunos if a['id'] == id_aluno), None)
    if not aluno:
        return jsonify({'error': 'Aluno não encontrado'}), 404
    alunos.remove(aluno)
    return jsonify({'message': 'Aluno excluído com sucesso'}), 200

@app.route('/professores', methods=['GET'])
def get_professores():
    return jsonify(professores)

@app.route('/professores/<int:id_professor>', methods=['GET'])
def get_professor(id_professor):
    professor = next((p for p in professores if p['id'] == id_professor), None)
    if not professor:
        return jsonify({'error': 'Professor não encontrado'}), 404
    return jsonify(professor)

@app.route('/professores', methods=['POST'])
def post_professor():
    dados = request.get_json()
    
    valido, erro = validar_campos(dados, ['nome', 'data_nascimento', 'disciplina', 'salario'])
    if not valido:
        return jsonify({'error': erro}), 400

    valido, erro = validar_numeros(dados, ['salario'])
    if not valido:
        return jsonify({'error': erro}), 400

    professor = {
        'id': gerar_id(professores),
        'nome': dados['nome'],
        'data_nascimento': dados['data_nascimento'],
        'disciplina': dados['disciplina'],
        'salario': dados['salario']
    }
    professores.append(professor)
    return jsonify(professor), 201

@app.route('/professores/<int:id_professor>', methods=['PUT'])
def put_professor(id_professor):
    professor = next((p for p in professores if p['id'] == id_professor), None)
    if not professor:
        return jsonify({'error': 'Professor não encontrado'}), 404

    dados = request.get_json()

    valido, erro = validar_campos(dados, ['nome', 'data_nascimento', 'disciplina', 'salario'])
    if not valido:
        return jsonify({'error': erro}), 400

    valido, erro = validar_numeros(dados, ['salario'])
    if not valido:
        return jsonify({'error': erro}), 400

    professor.update({
        'nome': dados['nome'],
        'data_nascimento': dados['data_nascimento'],
        'disciplina': dados['disciplina'],
        'salario': dados['salario']
    })
    return jsonify(professor), 200

@app.route('/professores/<int:id_professor>', methods=['DELETE'])
def delete_professor(id_professor):
    professor = next((p for p in professores if p['id'] == id_professor), None)
    if not professor:
        return jsonify({'error': 'Professor não encontrado'}), 404
    professores.remove(professor)
    return jsonify({'message': 'Professor excluído com sucesso'}), 200
@app.route('/turmas', methods=['GET'])
def get_turmas():
    return jsonify(turmas)

@app.route('/turmas/<int:id_turma>', methods=['GET'])
def get_turma(id_turma):
    turma = next((t for t in turmas if t['id'] == id_turma), None)
    if not turma:
        return jsonify({'error': 'Turma não encontrada'}), 404
    return jsonify(turma)

@app.route('/turmas', methods=['POST'])
def post_turma():
    dados = request.get_json()
    
    valido, erro = validar_campos(dados, ['nome', 'turno', 'professor_id'])
    if not valido:
        return jsonify({'error': erro}), 400

    turma = {
        'id': gerar_id(turmas),
        'nome': dados['nome'],
        'turno': dados['turno'],
        'professor_id': dados['professor_id']
    }
    turmas.append(turma)
    return jsonify(turma), 201

@app.route('/turmas/<int:id_turma>', methods=['PUT'])
def put_turma(id_turma):
    turma = next((t for t in turmas if t['id'] == id_turma), None)
    if not turma:
        return jsonify({'error': 'Turma não encontrada'}), 404

    dados = request.get_json()

    valido, erro = validar_campos(dados, ['nome', 'turno', 'professor_id'])
    if not valido:
        return jsonify({'error': erro}), 400

    turma.update({
        'nome': dados['nome'],
        'turno': dados['turno'],
        'professor_id': dados['professor_id']
    })
    return jsonify(turma), 200

@app.route('/turmas/<int:id_turma>', methods=['DELETE'])
def delete_turma(id_turma):
    turma = next((t for t in turmas if t['id'] == id_turma), None)
    if not turma:
        return jsonify({'error': 'Turma não encontrada'}), 404
    turmas.remove(turma)
    return jsonify({'message': 'Turma excluída com sucesso'}), 200

if __name__ == '__main__':
    app.run(debug=True)