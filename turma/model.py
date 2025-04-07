turmas = [
    {
        "id": 1,
        "nome": "1º Ano A",
        "turno": "Manhã",
        "professor_id": 1
    },
    {
        "id": 2,
        "nome": "2º Ano B",
        "turno": "Tarde",
        "professor_id": 2
    },
    {
        "id": 3,
        "nome": "3º Ano C",
        "turno": "Noite",
        "professor_id": 3
    }
]


class TurmaNaoEncontrada(Exception):
    pass

def listar_turmas():
    return turmas

def buscar_turma(id_turma):
    turma = next((t for t in turmas if t['id'] == id_turma), None)
    if not turma:
        raise TurmaNaoEncontrada
    return turma

def criar_turma(dados):
    turma = {
        'id': dados['id'],
        'nome': dados['nome'],
        'turno': dados['turno'],
        'professor_id': dados['professor_id']
    }
    turmas.append(turma)
    return turma

def atualizar_turma(id_turma, dados):
    turma = buscar_turma(id_turma)
    turma.update({
        'nome': dados['nome'],
        'ano': dados['ano']
    })
    return turma

def excluir_turma(id_turma):
    turma = buscar_turma(id_turma)
    turmas.remove(turma)
