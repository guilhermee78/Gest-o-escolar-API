import time
import requests
import pytest

BASE_URL = "http://127.0.0.1:5000"

# Função para esperar a API estar ativa
def espera_api_estar_ativa(url='http://127.0.0.1:5000'):
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("API está ativa e pronta!")
                break
        except requests.exceptions.RequestException:
            print("API ainda não está respondendo, tentando novamente...")
            time.sleep(5)  # Tenta novamente após 5 segundos

# Função pytest para chamar antes de rodar os testes
@pytest.fixture(scope="module", autouse=True)
def setup_module():
    espera_api_estar_ativa()

# Fixtures para dados de testes
@pytest.fixture
def aluno_data():
    return {
        "nome": "Carlos",
        "data_nascimento": "2002-08-15",
        "nota_primeiro_semestre": 9.0,
        "nota_segundo_semestre": 8.5,
        "turma_id": 1
    }

@pytest.fixture
def turma_data():
    return {
        "nome": "Turma A",
        "turno": "Manhã",
        "professor_id": 1
    }

@pytest.fixture
def professor_data():
    return {
        "nome": "Ana Paula",
        "data_nascimento": "1980-09-10",
        "disciplina": "Física",
        "salario": 5200
    }

# Funções auxiliares para verificar status da resposta
def verificar_status_ok(response):
    assert response.status_code == 200

def verificar_status_criado(response):
    assert response.status_code == 201

# Testes de Alunos
def test_get_alunos():
    response = requests.get(f"{BASE_URL}/alunos")
    response.raise_for_status()
    verificar_status_ok(response)
    assert isinstance(response.json(), list)

def test_post_aluno(aluno_data):
    response = requests.post(f"{BASE_URL}/alunos", json=aluno_data)
    response.raise_for_status()
    verificar_status_criado(response)
    assert "id" in response.json()

def test_get_aluno():
    aluno_id = 1
    response = requests.get(f"{BASE_URL}/alunos/{aluno_id}")
    response.raise_for_status()
    verificar_status_ok(response)

def test_put_aluno():
    aluno_id = 1
    aluno_update = {
        "nome": "Carlos Eduardo",
        "data_nascimento": "2002-08-15",
        "nota_primeiro_semestre": 9.5,
        "nota_segundo_semestre": 9.0,
        "turma_id": 1
    }
    response = requests.put(f"{BASE_URL}/alunos/{aluno_id}", json=aluno_update)
    response.raise_for_status()
    verificar_status_ok(response)

def test_delete_aluno():
    aluno_id = 1
    response = requests.delete(f"{BASE_URL}/alunos/{aluno_id}")
    response.raise_for_status()
    verificar_status_ok(response)

# Testes de Professores
def test_get_professores():
    response = requests.get(f"{BASE_URL}/professores")
    response.raise_for_status()
    verificar_status_ok(response)
    assert isinstance(response.json(), list)

def test_post_professor(professor_data):
    response = requests.post(f"{BASE_URL}/professores", json=professor_data)
    response.raise_for_status()
    verificar_status_criado(response)
    assert "id" in response.json()

def test_get_professor():
    professor_id = 1
    response = requests.get(f"{BASE_URL}/professores/{professor_id}")
    response.raise_for_status()
    verificar_status_ok(response)

def test_put_professor():
    professor_id = 1
    professor_update = {
        "nome": "Ana Paula Lima",
        "data_nascimento": "1980-09-10",
        "disciplina": "Física",
        "salario": 5300
    }
    response = requests.put(f"{BASE_URL}/professores/{professor_id}", json=professor_update)
    response.raise_for_status()
    verificar_status_ok(response)

def test_delete_professor():
    professor_id = 1
    response = requests.delete(f"{BASE_URL}/professores/{professor_id}")
    response.raise_for_status()
    verificar_status_ok(response)

# Testes de Turmas
def test_get_turmas():
    response = requests.get(f"{BASE_URL}/turmas")
    response.raise_for_status()
    verificar_status_ok(response)
    assert isinstance(response.json(), list)

def test_post_turma(turma_data):
    response = requests.post(f"{BASE_URL}/turmas", json=turma_data)
    response.raise_for_status()
    verificar_status_criado(response)
    assert "id" in response.json()

def test_get_turma():
    turma_id = 1
    response = requests.get(f"{BASE_URL}/turmas/{turma_id}")
    response.raise_for_status()
    verificar_status_ok(response)

def test_put_turma():
    turma_id = 1
    turma_update = {
        "nome": "Turma A - Avançada",
        "turno": "Tarde",
        "professor_id": 1
    }
    response = requests.put(f"{BASE_URL}/turmas/{turma_id}", json=turma_update)
    response.raise_for_status()
    verificar_status_ok(response)

def test_delete_turma():
    turma_id = 1
    response = requests.delete(f"{BASE_URL}/turmas/{turma_id}")
    response.raise_for_status()
    verificar_status_ok(response)

