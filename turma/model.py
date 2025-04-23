from sql import db
from professor.model import ProfessorModel

class TurmaModel(db.Model):
    __tablename__ = 'turmas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    turno = db.Column(db.String(20))
    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'))
    alunos = db.relationship('AlunoModel', back_populates='turma', cascade="all, delete-orphan")
    professor = db.relationship('ProfessorModel', backref=db.backref('turmas', lazy=True)) # Adicionado relacionamento com Professor

    def __init__(self, nome, turno, professor_id):
        self.nome = nome
        self.turno = turno
        self.professor_id = professor_id

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'turno': self.turno,
            'professor_id': self.professor_id,
            'alunos': [aluno.to_dict() for aluno in self.alunos], # Inclui a lista de alunos
            'professor': self.professor.to_dict() if self.professor else None # Inclui informações do professor
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