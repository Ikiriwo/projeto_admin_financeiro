"""
Aplicação principal Flask para processamento de notas fiscais.
"""
import os
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, request
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


def check_api_key():
    """Verifica se a chave API está configurada."""
    api_key = os.environ.get('GEMINI_API_KEY')
    return bool(api_key and api_key not in ['sua_chave_api_aqui', '', 'YOUR_API_KEY_HERE'])


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

    # Registro das rotas de setup ANTES de tudo
    from routes.setup_routes import setup_bp
    app.register_blueprint(setup_bp)

    # Middleware removido: Agora mostramos avisos contextuais ao invés de redirecionar
    # O usuário pode navegar livremente e verá avisos nas páginas que precisam da API

    # Inicializar sistema RAG (apenas se chave estiver configurada)
    if check_api_key():
        from routes.api_routes import init_rag_system
        with app.app_context():
            init_rag_system(db)

    # Registro das outras rotas
    app.register_blueprint(api_bp)
    app.register_blueprint(web_bp)

    # Popular banco de dados automaticamente se estiver vazio
    with app.app_context():
        try:
            from sqlalchemy import text
            # Verificar se o banco está vazio
            count = db.session.execute(text("SELECT COUNT(*) FROM pessoas")).scalar()
            if count == 0:
                print("=" * 70)
                print("🔄 Banco de dados vazio. Populando automaticamente...")
                print("=" * 70)
                import sys
                from pathlib import Path
                sys.path.insert(0, str(Path(__file__).parent / 'scripts'))
                from populate_database import populate_database
                success, message, stats = populate_database(clear_first=False)
                if success:
                    print(f"✅ {message}")
                else:
                    print(f"⚠️  Aviso: {message}")
        except Exception as e:
            print(f"⚠️  Aviso ao verificar/popular banco: {e}")

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
