from flask import Flask
from config import Config
from aluno.controller import alunos_bp
from professor.controller import professores_bp
from turma.controller import turmas_bp

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(alunos_bp, url_prefix='/alunos')
app.register_blueprint(professores_bp, url_prefix='/professores')
app.register_blueprint(turmas_bp, url_prefix='/turmas')

@app.route('/')
def health_check():
    return "API is running", 200

if __name__ == '__main__':
    app.run(debug=True)