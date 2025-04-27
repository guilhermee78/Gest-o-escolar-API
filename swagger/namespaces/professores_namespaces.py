from flask_restx import Namespace, Resource, fields
from professor.model import ProfessorModel  # Certifique-se de ter este model criado
from Util.helpers import validar_campos  # Para validar os dados

professores_ns = Namespace("professores", description="Operações relacionadas aos professores")

professor_model = professores_ns.model("Professor", {
    "nome": fields.String(required=True, description="Nome do professor"),
    "disciplina": fields.String(required=True, description="Disciplina lecionada"),
})

professor_output_model = professores_ns.model("ProfessorOutput", {
    "id": fields.Integer(description="ID do professor"),
    "nome": fields.String(description="Nome do professor"),
    "disciplina": fields.String(description="Disciplina lecionada"),
})

@professores_ns.route("/")
class ProfessoresResource(Resource):
    @professores_ns.marshal_list_with(professor_output_model)
    def get(self):
        """Lista todos os professores"""
        professores = ProfessorModel.find_all()
        return [professor.to_dict() for professor in professores]

    @professores_ns.expect(professor_model)
    @professores_ns.marshal_with(professor_output_model, code=201)
    def post(self):
        """Cria um novo professor"""
        dados = professores_ns.payload

        valido, erro = validar_campos(dados, ['nome', 'disciplina'])
        if not valido:
            professores_ns.abort(400, erro)

        professor = ProfessorModel(
            nome=dados['nome'],
            disciplina=dados['disciplina']
        )
        professor.save_to_db()
        return professor.to_dict(), 201

@professores_ns.route("/<int:id_professor>")
class ProfessorIdResource(Resource):
    @professores_ns.marshal_with(professor_output_model)
    def get(self, id_professor):
        """Obtém um professor pelo ID"""
        professor = ProfessorModel.find_by_id(id_professor)
        if professor:
            return professor.to_dict()
        professores_ns.abort(404, "Professor não encontrado")

    @professores_ns.expect(professor_model)
    @professores_ns.marshal_with(professor_output_model)
    def put(self, id_professor):
        """Atualiza um professor pelo ID"""
        dados = professores_ns.payload

        valido, erro = validar_campos(dados, ['nome', 'disciplina'])
        if not valido:
            professores_ns.abort(400, erro)

        professor = ProfessorModel.find_by_id(id_professor)
        if professor:
            professor.nome = dados['nome']
            professor.disciplina = dados['disciplina']
            professor.save_to_db()
            return professor.to_dict(), 200

        professores_ns.abort(404, "Professor não encontrado")

    def delete(self, id_professor):
        """Exclui um professor pelo ID"""
        professor = ProfessorModel.find_by_id(id_professor)
        if professor:
            professor.delete_from_db()
            return {"message": "Professor excluído com sucesso"}, 200
        professores_ns.abort(404, "Professor não encontrado")