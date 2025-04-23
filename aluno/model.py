from sql import db
from datetime import datetime

class AlunoModel(db.Model):
    __tablename__ = 'alunos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    data_nascimento = db.Column(db.String(10))  # Formato DD/MM/AAAA
    nota_primeiro_semestre = db.Column(db.Float)
    nota_segundo_semestre = db.Column(db.Float)
    media_final = db.Column(db.Float)
    turma_id = db.Column(db.Integer, db.ForeignKey('turmas.id'))  # Chave estrangeira para Turma
    turma = db.relationship('TurmaModel')  # Para acessar os dados da turma relacionada (opcional)

    def __init__(self, nome, data_nascimento, nota_primeiro_semestre, nota_segundo_semestre, turma_id):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.nota_primeiro_semestre = nota_primeiro_semestre
        self.nota_segundo_semestre = nota_segundo_semestre
        self.media_final = (nota_primeiro_semestre + nota_segundo_semestre) / 2
        self.turma_id = turma_id

    def json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'data_nascimento': self.data_nascimento,
            'nota_primeiro_semestre': self.nota_primeiro_semestre,
            'nota_segundo_semestre': self.nota_segundo_semestre,
            'media_final': self.media_final,
            'turma_id': self.turma_id
        }

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'data_nascimento': self.data_nascimento,
            'nota_primeiro_semestre': self.nota_primeiro_semestre,
            'nota_segundo_semestre': self.nota_segundo_semestre,
            'media_final': self.media_final,
            'turma_id': self.turma_id
        }

    def listar_alunos():
        alunos = AlunoModel.query.all()
        print(alunos)
        return [aluno.to_dict() for aluno in alunos]

    def adicionar_aluno(novos_dados):
        turma = TurmaModel.query.get(novos_dados['turma_id'])
        if turma is None:
            return {"message": "Turma não existe"}, 404

        try:
            data_nascimento = datetime.strptime(novos_dados['data_nascimento'], "%Y-%m-%d").date()
            nota_1 = float(novos_dados['nota_primeiro_semestre'])
            nota_2 = float(novos_dados['nota_segundo_semestre'])

            novo_aluno = AlunoModel(
                nome=novos_dados['nome'],
                data_nascimento=data_nascimento.strftime("%d/%m/%Y"),  # Formata para DD/MM/AAAA ao salvar no dict
                nota_primeiro_semestre=nota_1,
                nota_segundo_semestre=nota_2,
                turma_id=int(novos_dados['turma_id'])
            )

            db.session.add(novo_aluno)
            db.session.commit()

            return {"message": "Aluno adicionado com sucesso!"}, 201

        except Exception as e:
            return {"message": f"Erro ao adicionar aluno: {str(e)}"}, 500

    @classmethod
    def find_by_id(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()