"""
Aplicação principal Flask para processamento de notas fiscais.
"""
import os
from dotenv import load_dotenv
from flask import Flask
import google.generativeai as genai

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Importações dos modelos
from models import db, init_db

# Importações das rotas
from routes import api_bp, web_bp

# Configuração da API Gemini (agora vem do .env)
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-2.0-flash')


def create_app():
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__,
               template_folder='frontend/templates',
               static_folder='frontend/static')

    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['GEMINI_MODEL'] = GEMINI_MODEL

    # Configuração do banco de dados
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url

    # Inicialização do banco de dados
    init_db(app)

    # Inicializar sistema RAG
    from routes.api_routes import init_rag_system
    with app.app_context():
        init_rag_system(db)

    # Registro das rotas
    app.register_blueprint(api_bp)
    app.register_blueprint(web_bp)

    return app


# Criação da aplicação
app = create_app()

# Configuração da API Gemini
genai.configure(api_key=GEMINI_API_KEY)


if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', debug=True)
