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