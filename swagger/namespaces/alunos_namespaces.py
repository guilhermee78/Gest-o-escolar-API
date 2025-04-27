from flask_restx import Namespace, Resource, fields
from aluno.model import AlunoModel  # Corrigido o import
from Util.helpers import validar_campos, validar_numeros  # Para validar os dados

alunos_ns = Namespace("alunos", description="Operações relacionadas aos alunos")

aluno_model = alunos_ns.model("Aluno", {
    "nome": fields.String(required=True, description="Nome do aluno"),
    "data_nascimento": fields.String(required=True, description="Data de nascimento (YYYY-MM-DD)"),
    "nota_primeiro_semestre": fields.Float(required=True, description="Nota do primeiro semestre"),
    "nota_segundo_semestre": fields.Float(required=True, description="Nota do segundo semestre"),
    "turma_id": fields.Integer(required=True, description="ID da turma associada"),
})

aluno_output_model = alunos_ns.model("AlunoOutput", {
    "id": fields.Integer(description="ID do aluno"),
    "nome": fields.String(description="Nome do aluno"),
    "data_nascimento": fields.String(description="Data de nascimento (YYYY-MM-DD)"),
    "nota_primeiro_semestre": fields.Float(description="Nota do primeiro semestre"),
    "nota_segundo_semestre": fields.Float(description="Nota do segundo semestre"),
    "turma_id": fields.Integer(description="ID da turma associada"),
})

@alunos_ns.route("/")
class AlunosResource(Resource):
    @alunos_ns.marshal_list_with(aluno_output_model)
    def get(self):
        """Lista todos os alunos"""
        alunos = AlunoModel.find_all()
        return [aluno.to_dict() for aluno in alunos]

    @alunos_ns.expect(aluno_model)
    @alunos_ns.marshal_with(aluno_output_model, code=201)
    def post(self):
        """Cria um novo aluno"""
        dados = alunos_ns.payload

        valido, erro = validar_campos(dados, ['nome', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre', 'turma_id'])
        if not valido:
            alunos_ns.abort(400, erro)

        valido, erro = validar_numeros(dados, ['nota_primeiro_semestre', 'nota_segundo_semestre'])
        if not valido:
            alunos_ns.abort(400, erro)

        aluno = AlunoModel(
            nome=dados['nome'],
            data_nascimento=dados['data_nascimento'],
            nota_primeiro_semestre=dados['nota_primeiro_semestre'],
            nota_segundo_semestre=dados['nota_segundo_semestre'],
            turma_id=dados['turma_id']
        )
        aluno.save_to_db()
        return aluno.to_dict(), 201

@alunos_ns.route("/<int:id_aluno>")
class AlunoIdResource(Resource):
    @alunos_ns.marshal_with(aluno_output_model)
    def get(self, id_aluno):
        """Obtém um aluno pelo ID"""
        aluno = AlunoModel.find_by_id(id_aluno)
        if aluno:
            return aluno.to_dict()
        alunos_ns.abort(404, "Aluno não encontrado")

    @alunos_ns.expect(aluno_model)
    @alunos_ns.marshal_with(aluno_output_model)
    def put(self, id_aluno):
        """Atualiza um aluno pelo ID"""
        dados = alunos_ns.payload

        valido, erro = validar_campos(dados, ['nome', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre', 'turma_id'])
        if not valido:
            alunos_ns.abort(400, erro)

        valido, erro = validar_numeros(dados, ['nota_primeiro_semestre', 'nota_segundo_semestre'])
        if not valido:
            alunos_ns.abort(400, erro)

        aluno = AlunoModel.find_by_id(id_aluno)
        if aluno:
            aluno.nome = dados['nome']
            aluno.data_nascimento = dados['data_nascimento']
            aluno.nota_primeiro_semestre = dados['nota_primeiro_semestre']
            aluno.nota_segundo_semestre = dados['nota_segundo_semestre']
            aluno.turma_id = dados['turma_id']
            aluno.save_to_db()
            return aluno.to_dict(), 200

        alunos_ns.abort(404, "Aluno não encontrado")

    def delete(self, id_aluno):
        """Exclui um aluno pelo ID"""
        aluno = AlunoModel.find_by_id(id_aluno)
        if aluno:
            aluno.delete_from_db()
            return {"message": "Aluno excluído com sucesso"}, 200
        alunos_ns.abort(404, "Aluno não encontrado")
