from flask_restx import Namespace, Resource, fields
from turma.model import TurmaModel  # Certifique-se de ter este model criado
from Util.helpers import validar_campos  # Reutilizando a validação de campos

turmas_ns = Namespace("turmas", description="Operações relacionadas às turmas")

turma_model = turmas_ns.model("Turma", {
    "nome": fields.String(required=True, description="Nome da turma"),
    "turno": fields.String(required=True, description="Turno da turma (Manhã, Tarde, Noite)"),
    "professor_id": fields.Integer(required=True, description="ID do professor responsável"),
})

turma_output_model = turmas_ns.model("TurmaOutput", {
    "id": fields.Integer(description="ID da turma"),
    "nome": fields.String(description="Nome da turma"),
    "turno": fields.String(description="Turno da turma (Manhã, Tarde, Noite)"),
    "professor_id": fields.Integer(description="ID do professor responsável"),
})

@turmas_ns.route("/")
class TurmasResource(Resource):
    @turmas_ns.marshal_list_with(turma_output_model)
    def get(self):
        """Lista todas as turmas"""
        turmas = TurmaModel.find_all()
        return [turma.to_dict() for turma in turmas]

    @turmas_ns.expect(turma_model)
    @turmas_ns.marshal_with(turma_output_model, code=201)
    def post(self):
        """Cria uma nova turma"""
        dados = turmas_ns.payload

        valido, erro = validar_campos(dados, ['nome', 'turno', 'professor_id'])
        if not valido:
            turmas_ns.abort(400, erro)

        turma = TurmaModel(
            nome=dados['nome'],
            turno=dados['turno'],
            professor_id=dados['professor_id']
        )
        turma.save_to_db()
        return turma.to_dict(), 201

@turmas_ns.route("/<int:id_turma>")
class TurmaIdResource(Resource):
    @turmas_ns.marshal_with(turma_output_model)
    def get(self, id_turma):
        """Obtém uma turma pelo ID"""
        turma = TurmaModel.find_by_id(id_turma)
        if turma:
            return turma.to_dict()
        turmas_ns.abort(404, "Turma não encontrada")

    @turmas_ns.expect(turma_model)
    @turmas_ns.marshal_with(turma_output_model)
    def put(self, id_turma):
        """Atualiza uma turma pelo ID"""
        dados = turmas_ns.payload

        valido, erro = validar_campos(dados, ['nome', 'turno', 'professor_id'])
        if not valido:
            turmas_ns.abort(400, erro)

        turma = TurmaModel.find_by_id(id_turma)
        if turma:
            turma.nome = dados['nome']
            turma.turno = dados['turno']
            turma.professor_id = dados['professor_id']
            turma.save_to_db()
            return turma.to_dict(), 200

        turmas_ns.abort(404, "Turma não encontrada")

    def delete(self, id_turma):
        """Exclui uma turma pelo ID"""
        turma = TurmaModel.find_by_id(id_turma)
        if turma:
            turma.delete_from_db()
            return {"message": "Turma excluída com sucesso"}, 200
        turmas_ns.abort(404, "Turma não encontrada")