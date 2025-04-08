import time
import requests
import pytest

BASE_URL = "http://127.0.0.1:5000"

def espera_api_estar_ativa(url=BASE_URL, timeout=30, poll_interval=5):

    print("ENTRANDO NA FUNÇÃO espera_api_estar_ativa")
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            print(f"TENTANDO CONECTAR EM: {url}")
            response = requests.get(url)
            response.raise_for_status()  
            print("API ESTÁ ATIVA E PRONTA!")
            print("SAINDO DA FUNÇÃO espera_api_estar_ativa")
            return
        except requests.exceptions.RequestException as e:
            print(f"API AINDA NÃO ESTÁ RESPONDENDO, TENTANDO NOVAMENTE EM {poll_interval} SEGUNDOS... ERRO: {e}")
            time.sleep(poll_interval)
    pytest.fail(f"TEMPO LIMITE ({timeout} segundos) EXCEDIDO ESPERANDO PELA API EM {url}")

@pytest.fixture(scope="module", autouse=True)
def setup_module():
    
    espera_api_estar_ativa()

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
        "disciplina": "Física",
        "salario": 5200
    }

def verificar_status_ok(response):
    
    assert response.status_code == 200

def verificar_status_criado(response):
    
    assert response.status_code == 201

def test_get_alunos():
    
    print("\nEXECUTANDO TESTE: test_get_alunos")
    try:
        response = requests.get(f"{BASE_URL}/alunos")
        response.raise_for_status()
        verificar_status_ok(response)
        assert isinstance(response.json(), list)
        print("TESTE: test_get_alunos CONCLUÍDO")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Erro ao obter alunos: {e}")
        print(f"TESTE: test_get_alunos FALHOU COM ERRO: {e}")

def test_post_aluno(aluno_data):
    
    print("\nEXECUTANDO TESTE: test_post_aluno")
    try:
        response = requests.post(f"{BASE_URL}/alunos", json=aluno_data)
        response.raise_for_status()
        verificar_status_criado(response)
        response_json = response.json()
        assert "id" in response_json
        assert response_json["nome"] == aluno_data["nome"]
        assert response_json["data_nascimento"] == aluno_data["data_nascimento"]
        assert response_json["nota_primeiro_semestre"] == aluno_data["nota_primeiro_semestre"]
        assert response_json["nota_segundo_semestre"] == aluno_data["nota_segundo_semestre"]
        assert response_json["turma_id"] == aluno_data["turma_id"]
        print("TESTE: test_post_aluno CONCLUÍDO")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Erro ao criar aluno: {e}")
        print(f"TESTE: test_post_aluno FALHOU COM ERRO: {e}")

def test_get_aluno():
    
    aluno_id = 1  
    print("\nEXECUTANDO TESTE: test_get_aluno")
    try:
        response = requests.get(f"{BASE_URL}/alunos/{aluno_id}")
        response.raise_for_status()
        verificar_status_ok(response)
        response_json = response.json()
        assert "id" in response_json
        print("TESTE: test_get_aluno CONCLUÍDO")
    except requests.exceptions.RequestException as e:
        if hasattr(response, 'status_code') and response.status_code == 404:
            assert response.status_code == 404
            print("TESTE: test_get_aluno CONCLUÍDO (Aluno não encontrado, esperado)")
        else:
            pytest.fail(f"Erro ao obter aluno com ID {aluno_id}: {e}")
            print(f"TESTE: test_get_aluno FALHOU COM ERRO: {e}")

def test_put_aluno():
    
    aluno_id = 1 
    aluno_update = {
        "nome": "Carlos Eduardo",
        "data_nascimento": "2002-08-15",
        "nota_primeiro_semestre": 9.5,
        "nota_segundo_semestre": 9.0,
        "turma_id": 1
    }
    print("\nEXECUTANDO TESTE: test_put_aluno")
    try:
        response = requests.put(f"{BASE_URL}/alunos/{aluno_id}", json=aluno_update)
        response.raise_for_status()
        verificar_status_ok(response)
        response_json = response.json()
        assert response_json["nome"] == aluno_update["nome"]
        assert response_json["nota_primeiro_semestre"] == aluno_update["nota_primeiro_semestre"]
        assert response_json["nota_segundo_semestre"] == aluno_update["nota_segundo_semestre"]
        print("TESTE: test_put_aluno CONCLUÍDO")
    except requests.exceptions.RequestException as e:
        if hasattr(response, 'status_code') and response.status_code == 404:
            assert response.status_code == 404
            print("TESTE: test_put_aluno CONCLUÍDO (Aluno não encontrado, esperado)")
        else:
            pytest.fail(f"Erro ao atualizar aluno com ID {aluno_id}: {e}")
            print(f"TESTE: test_put_aluno FALHOU COM ERRO: {e}")

def test_delete_aluno():
    
    aluno_id = 1  
    print("\nEXECUTANDO TESTE: test_delete_aluno")
    try:
        response = requests.delete(f"{BASE_URL}/alunos/{aluno_id}")
        response.raise_for_status()
        verificar_status_ok(response)
        print("TESTE: test_delete_aluno CONCLUÍDO")
        
        response_get = requests.get(f"{BASE_URL}/alunos/{aluno_id}")
        assert response_get.status_code == 404
    except requests.exceptions.RequestException as e:
        if hasattr(response, 'status_code') and response.status_code == 404:
            assert response.status_code == 404
            print("TESTE: test_delete_aluno CONCLUÍDO (Aluno não encontrado, esperado)")
        else:
            pytest.fail(f"Erro ao deletar aluno com ID {aluno_id}: {e}")
            print(f"TESTE: test_delete_aluno FALHOU COM ERRO: {e}")

def test_get_professores():
    
    print("\nEXECUTANDO TESTE: test_get_professores")
    try:
        response = requests.get(f"{BASE_URL}/professores")
        response.raise_for_status()
        verificar_status_ok(response)
        assert isinstance(response.json(), list)
        print("TESTE: test_get_professores CONCLUÍDO")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Erro ao obter professores: {e}")
        print(f"TESTE: test_get_professores FALHOU COM ERRO: {e}")

def test_post_professor(professor_data):
    
    print("\nEXECUTANDO TESTE: test_post_professor")
    try:
        response = requests.post(f"{BASE_URL}/professores", json=professor_data)
        response.raise_for_status()
        verificar_status_criado(response)
        response_json = response.json()
        assert "id" in response_json
        assert response_json["nome"] == professor_data["nome"]
        assert response_json["disciplina"] == professor_data["disciplina"]
       
        print("TESTE: test_post_professor CONCLUÍDO")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Erro ao criar professor: {e}")
        print(f"TESTE: test_post_professor FALHOU COM ERRO: {e}")

def test_get_professor():
    
    professor_id = 1  
    print("\nEXECUTANDO TESTE: test_get_professor")
    try:
        response = requests.get(f"{BASE_URL}/professores/{professor_id}")
        response.raise_for_status()
        verificar_status_ok(response)
        response_json = response.json()
        assert "id" in response_json
        print("TESTE: test_get_professor CONCLUÍDO")
    except requests.exceptions.RequestException as e:
        if hasattr(response, 'status_code') and response.status_code == 404:
            assert response.status_code == 404
            print("TESTE: test_get_professor CONCLUÍDO (Professor não encontrado, esperado)")
        else:
            pytest.fail(f"Erro ao obter professor com ID {professor_id}: {e}")
            print(f"TESTE: test_get_professor FALHOU COM ERRO: {e}")

def test_put_professor():
    
    professor_id = 1  
    professor_update = {
        "nome": "Ana Paula Lima",
        "disciplina": "Física",
        "salario": 5300
        
    }
    print("\nEXECUTANDO TESTE: test_put_professor")
    try:
        response = requests.put(f"{BASE_URL}/professores/{professor_id}", json=professor_update)
        response.raise_for_status()
        verificar_status_ok(response)
        response_json = response.json()
        assert response_json["nome"] == professor_update["nome"]
        assert response_json["disciplina"] == professor_update["disciplina"]
        
        print("TESTE: test_put_professor CONCLUÍDO")
    except requests.exceptions.RequestException as e:
        if hasattr(response, 'status_code') and response.status_code == 404:
            assert response.status_code == 404
            print("TESTE: test_put_professor CONCLUÍDO (Professor não encontrado, esperado)")
        else:
            pytest.fail(f"Erro ao atualizar professor com ID {professor_id}: {e}")
            print(f"TESTE: test_put_professor FALHOU COM ERRO: {e}")

def test_delete_professor():
    
    professor_id = 1  
    print("\nEXECUTANDO TESTE: test_delete_professor")
    try:
        response = requests.delete(f"{BASE_URL}/professores/{professor_id}")
        response.raise_for_status()
        verificar_status_ok(response)
        print("TESTE: test_delete_professor CONCLUÍDO")
        
        response_get = requests.get(f"{BASE_URL}/professores/{professor_id}")
        assert response_get.status_code == 404
    except requests.exceptions.RequestException as e:
        if hasattr(response, 'status_code') and response.status_code == 404:
            assert response.status_code == 404
            print("TESTE: test_delete_professor CONCLUÍDO (Professor não encontrado, esperado)")
        else:
            pytest.fail(f"Erro ao deletar professor com ID {professor_id}: {e}")
            print(f"TESTE: test_delete_professor FALHOU COM ERRO: {e}")

def test_get_turmas():
    
    print("\nEXECUTANDO TESTE: test_get_turmas")
    try:
        response = requests.get(f"{BASE_URL}/turmas")
        response.raise_for_status()
        verificar_status_ok(response)
        assert isinstance(response.json(), list)
        print("TESTE: test_get_turmas CONCLUÍDO")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Erro ao obter turmas: {e}")
        print(f"TESTE: test_get_turmas FALHOU COM ERRO: {e}")

def test_post_turma(turma_data):
    
    print("\nEXECUTANDO TESTE: test_post_turma")
    try:
        response = requests.post(f"{BASE_URL}/turmas", json=turma_data)
        response.raise_for_status()
        verificar_status_criado(response)
        response_json = response.json()
        assert "id" in response_json
        assert response_json["nome"] == turma_data["nome"]
        assert response_json["turno"] == turma_data["turno"]
        assert response_json["professor_id"] == turma_data["professor_id"]
        print("TESTE: test_post_turma CONCLUÍDO")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Erro ao criar turma: {e}")
        print(f"TESTE: test_post_turma FALHOU COM ERRO: {e}")

def test_get_turma():
    
    turma_id = 1 
    print("\nEXECUTANDO TESTE: test_get_turma")
    try:
        response = requests.get(f"{BASE_URL}/turmas/{turma_id}")
        response.raise_for_status()
        verificar_status_ok(response)
        response_json = response.json()
        assert "id" in response_json
        print("TESTE: test_get_turma CONCLUÍDO")
    except requests.exceptions.RequestException as e:
        if hasattr(response, 'status_code') and response.status_code == 404:
            assert response.status_code == 404
            print("TESTE: test_get_turma CONCLUÍDO (Turma não encontrada, esperado)")
        else:
            pytest.fail(f"Erro ao obter turma com ID {turma_id}: {e}")
            print(f"TESTE: test_get_turma FALHOU COM ERRO: {e}")


def test_put_turma():
    
    turma_id = 1 
    turma_update = {
        "nome": "Turma A - Avançada",
        "turno": "Tarde",
        "professor_id": 1
    }
    print("\nEXECUTANDO TESTE: test_put_turma")
    try:
        response = requests.put(f"{BASE_URL}/turmas/{turma_id}", json=turma_update)
        response.raise_for_status()
        verificar_status_ok(response)
        response_json = response.json()
        assert response_json["nome"] == turma_update["nome"]
        assert response_json["turno"] == turma_update["turno"]
        assert response_json["professor_id"] == turma_update["professor_id"]
        print("TESTE: test_put_turma CONCLUÍDO")
    except requests.exceptions.RequestException as e:
        if hasattr(response, 'status_code') and response.status_code == 404:
            assert response.status_code == 404
            print("TESTE: test_put_turma CONCLUÍDO (Turma não encontrada, esperado)")
        else:
            pytest.fail(f"Erro ao atualizar turma com ID {turma_id}: {e}")
            print(f"TESTE: test_put_turma FALHOU COM ERRO: {e}")


def test_delete_turma():
    
    turma_id = 1  
    print("\nEXECUTANDO TESTE: test_delete_turma")
    try:
        response = requests.delete(f"{BASE_URL}/turmas/{turma_id}")
        response.raise_for_status()
        verificar_status_ok(response)
        print("TESTE: test_delete_turma CONCLUÍDO")
        
        response_get = requests.get(f"{BASE_URL}/turmas/{turma_id}")
        assert response_get.status_code == 404
    except requests.exceptions.RequestException as e:
        if hasattr(response, 'status_code') and response.status_code == 404:
            assert response.status_code == 404
            print("TESTE: test_delete_turma CONCLUÍDO (Turma não encontrada, esperado)")
        else:
            pytest.fail(f"Erro ao deletar turma com ID {turma_id}: {e}")
            print(f"TESTE: test_delete_turma FALHOU COM ERRO: {e}")