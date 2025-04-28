import unittest
import requests


BASE_URL = "http://127.0.0.1:5001/api"

class TestBaseAPI(unittest.TestCase):
    
    def verificar_status_ok(self, response):
        self.assertEqual(response.status_code, 200)

    def verificar_status_criado(self, response):
        self.assertEqual(response.status_code, 201)

class TestAlunosAPI(TestBaseAPI):
    
    def test_get_alunos(self):
        try:
            response = requests.get(f"{BASE_URL}/alunos")
            response.raise_for_status()  
            self.verificar_status_ok(response)
            self.assertIsInstance(response.json(), list)
        except requests.exceptions.RequestException as e:
            self.fail(f"Erro ao obter alunos: {e}")

    def test_post_aluno(self):
        aluno_data = {
            "nome": "Carlos",
            "data_nascimento": "2002-08-15",
            "nota_primeiro_semestre": 9.0,
            "nota_segundo_semestre": 8.5,
            "turma_id": 1
        }
        try:
            response = requests.post(f"{BASE_URL}/alunos", json=aluno_data)
            response.raise_for_status()
            self.verificar_status_criado(response)
            self.assertIn("id", response.json())
        except requests.exceptions.RequestException as e:
            self.fail(f"Erro ao criar aluno: {e}")

    def test_get_aluno(self):
        aluno_id = 1
        try:
            response = requests.get(f"{BASE_URL}/alunos/{aluno_id}")
            response.raise_for_status()
            self.verificar_status_ok(response)
        except requests.exceptions.RequestException as e:
            if response.status_code == 404:
                self.assertEqual(response.status_code, 404)
            else:
                self.fail(f"Erro ao obter aluno com ID {aluno_id}: {e}")

    def test_put_aluno(self):
        aluno_id = 1
        aluno_update = {
            "nome": "Carlos Eduardo",
            "data_nascimento": "2002-08-15",
            "nota_primeiro_semestre": 9.5,
            "nota_segundo_semestre": 9.0,
            "turma_id": 1
        }
        try:
            response = requests.put(f"{BASE_URL}/alunos/{aluno_id}", json=aluno_update)
            response.raise_for_status()
            self.verificar_status_ok(response)
        except requests.exceptions.RequestException as e:
            if response.status_code == 404:
                self.assertEqual(response.status_code, 404)
            else:
                self.fail(f"Erro ao atualizar aluno com ID {aluno_id}: {e}")

    def test_delete_aluno(self):
        aluno_id = 1
        try:
            response = requests.delete(f"{BASE_URL}/alunos/{aluno_id}")
            response.raise_for_status()
            self.verificar_status_ok(response)
        except requests.exceptions.RequestException as e:
            if response.status_code == 404:
                self.assertEqual(response.status_code, 404)
            else:
                self.fail(f"Erro ao deletar aluno com ID {aluno_id}: {e}")

class TestProfessoresAPI(TestBaseAPI):
    
    def test_get_professores(self):
        try:
            response = requests.get(f"{BASE_URL}/professores")
            response.raise_for_status() 
            self.verificar_status_ok(response)
            self.assertIsInstance(response.json(), list)
        except requests.exceptions.RequestException as e:
            self.fail(f"Erro ao obter professores: {e}")
    
    def test_post_professor(self):
        professor_data = {
            "nome": "Ana Paula",
            "data_nascimento": "1980-09-10",
            "disciplina": "Física",
            "salario": 5200
        }
        try:
            response = requests.post(f"{BASE_URL}/professores", json=professor_data)
            response.raise_for_status()
            self.verificar_status_criado(response)
            self.assertIn("id", response.json())
        except requests.exceptions.RequestException as e:
            self.fail(f"Erro ao criar professor: {e}")
    
    def test_get_professor(self):
        professor_id = 1
        try:
            response = requests.get(f"{BASE_URL}/professores/{professor_id}")
            response.raise_for_status()
            self.verificar_status_ok(response)
        except requests.exceptions.RequestException as e:
            if response.status_code == 404:
                self.assertEqual(response.status_code, 404)
            else:
                self.fail(f"Erro ao obter professor com ID {professor_id}: {e}")
    
    def test_put_professor(self):
        professor_id = 1
        professor_update = {
            "nome": "Ana Paula Lima",
            "data_nascimento": "1980-09-10",
            "disciplina": "Física",
            "salario": 5300
        }
        try:
            response = requests.put(f"{BASE_URL}/professores/{professor_id}", json=professor_update)
            response.raise_for_status()
            self.verificar_status_ok(response)
        except requests.exceptions.RequestException as e:
            if response.status_code == 404:
                self.assertEqual(response.status_code, 404)
            else:
                self.fail(f"Erro ao atualizar professor com ID {professor_id}: {e}")
    
    def test_delete_professor(self):
        professor_id = 1
        try:
            response = requests.delete(f"{BASE_URL}/professores/{professor_id}")
            response.raise_for_status()
            self.verificar_status_ok(response)
        except requests.exceptions.RequestException as e:
            if response.status_code == 404:
                self.assertEqual(response.status_code, 404)
            else:
                self.fail(f"Erro ao deletar professor com ID {professor_id}: {e}")



class TestTurmasAPI(TestBaseAPI):
    
    def test_get_turmas(self):
        try:
            response = requests.get(f"{BASE_URL}/turmas")
            response.raise_for_status()  
            self.verificar_status_ok(response)
            self.assertIsInstance(response.json(), list)
        except requests.exceptions.RequestException as e:
            self.fail(f"Erro ao obter turmas: {e}")

    def test_post_turma(self):
        turma_data = {
            "nome": "Turma A",
            "turno": "Manhã",
            "professor_id": 1
        }
        try:
            response = requests.post(f"{BASE_URL}/turmas", json=turma_data)
            response.raise_for_status()
            self.verificar_status_criado(response)
            self.assertIn("id", response.json())
        except requests.exceptions.RequestException as e:
            self.fail(f"Erro ao criar turma: {e}")

    def test_get_turma(self):
        turma_id = 1
        try:
            response = requests.get(f"{BASE_URL}/turmas/{turma_id}")
            response.raise_for_status()
            self.verificar_status_ok(response)
        except requests.exceptions.RequestException as e:
            if response.status_code == 404:
                self.assertEqual(response.status_code, 404)
            else:
                self.fail(f"Erro ao obter turma com ID {turma_id}: {e}")

    def test_put_turma(self):
        turma_id = 1
        turma_update = {
            "nome": "Turma A - Avançada",
            "turno": "Tarde",
            "professor_id": 1
        }
        try:
            response = requests.put(f"{BASE_URL}/turmas/{turma_id}", json=turma_update)
            response.raise_for_status()
            self.verificar_status_ok(response)
        except requests.exceptions.RequestException as e:
            if response.status_code == 404:
                self.assertEqual(response.status_code, 404)
            else:
                self.fail(f"Erro ao atualizar turma com ID {turma_id}: {e}")

    def test_delete_turma(self):
        turma_id = 1
        try:
            response = requests.delete(f"{BASE_URL}/turmas/{turma_id}")
            response.raise_for_status()
            self.verificar_status_ok(response)
        except requests.exceptions.RequestException as e:
            if response.status_code == 404:
                self.assertEqual(response.status_code, 404)
            else:
                self.fail(f"Erro ao deletar turma com ID {turma_id}: {e}")

if __name__ == "__main__":
    unittest.main()
