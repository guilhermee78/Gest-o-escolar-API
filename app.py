from flask import Flask
from config import Config
from sql import db  # Importe a instância db do extensions.py
from aluno.controller import alunos_bp
from professor.controller import professores_bp
from turma.controller import turmas_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)  # Inicialize a extensão db com a aplicação Flask


# Registrar os Blueprints
app.register_blueprint(alunos_bp, url_prefix='/api')
app.register_blueprint(professores_bp, url_prefix='/api')
app.register_blueprint(turmas_bp, url_prefix='/api')

@app.route('/')
def health_check():
    return "API is running", 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)