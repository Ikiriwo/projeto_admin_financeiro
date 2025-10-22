from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)
    
    # Importar os modelos para que sejam registrados pelo SQLAlchemy
    from . import pessoas
    from . import classificacao
    from . import parcelas_contas
    from . import movimento_contas
    from . import nota_fiscal
    
    # Criar as tabelas no banco de dados
    with app.app_context():
        db.create_all()