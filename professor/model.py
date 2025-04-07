professores = [
    {
        "id": 1,
        "nome": "Carlos Silva",
        "disciplina": "Matemática"
    },
    {
        "id": 2,
        "nome": "Fernanda Lima",
        "disciplina": "Português"
    },
    {
        "id": 3,
        "nome": "João Pedro",
        "disciplina": "História"
    }
]

class ProfessorNaoEncontrado(Exception):
    pass

def listar_professores():
    return professores

def buscar_professor(id_professor):
    professor = next((p for p in professores if p['id'] == id_professor), None)
    if not professor:
        raise ProfessorNaoEncontrado
    return professor

def criar_professor(dados):
    professor = {
        'id': dados['id'],
        'nome': dados['nome'],
        'disciplina': dados['disciplina']
    }
    professores.append(professor)
    return professor

def atualizar_professor(id_professor, dados):
    professor = buscar_professor(id_professor)
    professor.update({
        'nome': dados['nome'],
        'disciplina': dados['disciplina']
    })
    return professor

def excluir_professor(id_professor):
    professor = buscar_professor(id_professor)
    professores.remove(professor)
