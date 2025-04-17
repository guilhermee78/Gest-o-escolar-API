from sql import db


class AlunoModel(db.Model):
    __tablename__ = 'alunos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    data_nascimento = db.Column(db.String(10))  # Formato DD/MM/AAAA
    nota_primeiro_semestre = db.Column(db.Float)
    nota_segundo_semestre = db.Column(db.Float)
    media_final = db.Column(db.Float)
    turma_id = db.Column(db.Integer, db.ForeignKey('turmas.id')) # Chave estrangeira para Turma
    # turma = db.relationship('TurmaModel') # Para acessar os dados da turma relacionada (opcional)

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