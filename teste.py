import traceback
import unittest
import requests

BASE_URL = "http://127.0.0.1:5000"

class TestAlunosAPI(unittest.TestCase):

    def verificar_status_ok(self, response):
        self.assertEqual(response.status_code, 200)

    def verificar_status_criado(self, response):
        self.assertEqual(response.status_code, 201)

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
            self.assertEqual(response.status_code, 200)
            
        except requests.exceptions.RequestException as e:
            if response is not None and response.status_code == 404:
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
            self.assertEqual(response.status_code, 200)
            
        except requests.exceptions.RequestException as e:
            if response is not None and response.status_code == 404:
                self.assertEqual(response.status_code, 404)
            else:
                self.fail(f"Erro ao atualizar aluno com ID {aluno_id}: {e}")

    def test_delete_aluno(self):
        aluno_id = 1
        try:
            response = requests.delete(f"{BASE_URL}/alunos/{aluno_id}")
            response.raise_for_status()
            self.assertEqual(response.status_code, 200)
        except requests.exceptions.RequestException as e:
            if response is not None and response.status_code == 404:
                self.assertEqual(response.status_code, 404)
            else:
                self.fail(f"Erro ao deletar aluno com ID {aluno_id}: {e}")

#     # Teste PROFESSORES
#     def test_get_professores(self):
#         response = requests.get(f"{BASE_URL}/professores")
#         self.assertEqual(response.status_code, 200)
#         self.assertIsInstance(response.json(), list)

#     def test_post_professor(self):
#         professor_data = {
#             "nome": "Ana Paula",
#             "data_nascimento": "1980-09-10",
#             "disciplina": "Física",
#             "salario": 5200
#         }
#         response = requests.post(f"{BASE_URL}/professores", json=professor_data)
#         self.assertEqual(response.status_code, 201)
#         self.assertIn("id", response.json())

#     def test_get_professor(self):
#         response = requests.get(f"{BASE_URL}/professores/1")
#         self.assertIn(response.status_code, [200, 404])

#     def test_put_professor(self):
#         professor_update = {
#             "nome": "Ana Paula Lima",
#             "data_nascimento": "1980-09-10",
#             "disciplina": "Física",
#             "salario": 5300
#         }
#         response = requests.put(f"{BASE_URL}/professores/1", json=professor_update)
#         self.assertIn(response.status_code, [200, 404])

#     def test_delete_professor(self):
#         response = requests.delete(f"{BASE_URL}/professores/1")
#         self.assertIn(response.status_code, [200, 404])

#     # Teste TURMAS
#     def test_get_turmas(self):
#         response = requests.get(f"{BASE_URL}/turmas")
#         self.assertEqual(response.status_code, 200)
#         self.assertIsInstance(response.json(), list)

#     def test_post_turma(self):
#         turma_data = {
#             "nome": "Turma D",
#             "turno": "Tarde",
#             "professor_id": 1
#         }
#         response = requests.post(f"{BASE_URL}/turmas", json=turma_data)
#         self.assertEqual(response.status_code, 201)
#         self.assertIn("id", response.json())

#     def test_get_turma(self):
#         response = requests.get(f"{BASE_URL}/turmas/1")
#         self.assertIn(response.status_code, [200, 404])

#     def test_put_turma(self):
#         turma_update = {
#             "nome": "Turma D - Avançada",
#             "turno": "Tarde",
#             "professor_id": 1
#         }
#         response = requests.put(f"{BASE_URL}/turmas/1", json=turma_update)
#         self.assertIn(response.status_code, [200, 404])

#     def test_delete_turma(self):
#         response = requests.delete(f"{BASE_URL}/turmas/1")
#         self.assertIn(response.status_code, [200, 404])

if __name__ == "__main__":
    unittest.main()