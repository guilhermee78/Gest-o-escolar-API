alunos = [
    {
        "id": 1,
        "nome": "Ana Clara",
        "data_nascimento": "12/03/2008",
        "nota_primeiro_semestre": 8.5,
        "nota_segundo_semestre": 7.0,
        "media_final": 7.75,
        "turma_id": 1
    },
    {
        "id": 2,
        "nome": "Lucas Oliveira",
        "data_nascimento": "23/07/2007",
        "nota_primeiro_semestre": 6.0,
        "nota_segundo_semestre": 5.5,
        "media_final": 5.75,
        "turma_id": 2
    },
    {
        "id": 3,
        "nome": "Mariana Costa",
        "data_nascimento": "30/01/2006",
        "nota_primeiro_semestre": 9.0,
        "nota_segundo_semestre": 8.0,
        "media_final": 8.5,
        "turma_id": 3
    }
]

class AlunoNaoEncontrado(Exception):
    pass

def listar_alunos():
    return alunos

def buscar_aluno(id_aluno):
    aluno = next((a for a in alunos if a['id'] == id_aluno), None)
    if not aluno:
        raise AlunoNaoEncontrado
    return aluno

def criar_aluno(dados):
    aluno = {
        'id': dados['id'],
        'nome': dados['nome'],
        'data_nascimento': dados['data_nascimento'],
        'nota_primeiro_semestre': dados['nota_primeiro_semestre'],
        'nota_segundo_semestre': dados['nota_segundo_semestre'],
        'media_final': (dados['nota_primeiro_semestre'] + dados['nota_segundo_semestre']) / 2,
        'turma_id': dados['turma_id']
    }
    alunos.append(aluno)
    return aluno

def atualizar_aluno(id_aluno, dados):
    aluno = buscar_aluno(id_aluno)
    aluno.update({
        'nome': dados['nome'],
        'data_nascimento': dados['data_nascimento'],
        'nota_primeiro_semestre': dados['nota_primeiro_semestre'],
        'nota_segundo_semestre': dados['nota_segundo_semestre'],
        'media_final': (dados['nota_primeiro_semestre'] + dados['nota_segundo_semestre']) / 2,
        'turma_id': dados['turma_id']
    })
    return aluno

def excluir_aluno(id_aluno):
    aluno = buscar_aluno(id_aluno)
    alunos.remove(aluno)
