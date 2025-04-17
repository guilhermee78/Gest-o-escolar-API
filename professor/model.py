from sql import db

class ProfessorModel(db.Model):
    __tablename__ = 'professores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    disciplina = db.Column(db.String(80))

    def __init__(self, nome, disciplina):
        self.nome = nome
        self.disciplina = disciplina

    def json(self):
        return {'id': self.id, 'nome': self.nome, 'disciplina': self.disciplina}

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