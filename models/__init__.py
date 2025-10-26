from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importar modelos após a definição do db para evitar importações circulares
from . import pessoas
from . import classificacao
from . import parcelas_contas
from . import movimento_contas
from . import nota_fiscal

def init_db(app):
    db.init_app(app)
    with app.app_context():
        # Criar tabelas se não existirem
        db.create_all()
        
        # Inserir dados iniciais para teste se não existirem
        from .pessoas import Pessoas
        from .classificacao import Classificacao
        
        # Verificar se já existem registros
        if Pessoas.query.count() == 0:
            # Criar alguns fornecedores e faturados para teste
            fornecedor = Pessoas(tipo='CLIENTE-FORNECEDOR', razao_social='Fornecedor Teste', cpf_cnpj='12345678901234')
            faturado = Pessoas(tipo='FATURADO', razao_social='Faturado Teste', cpf_cnpj='12345678901')
            db.session.add(fornecedor)
            db.session.add(faturado)
            
        if Classificacao.query.count() == 0:
            # Criar algumas classificações para teste
            despesa = Classificacao(tipo='DESPESA', descricao='Despesa Teste')
            receita = Classificacao(tipo='RECEITA', descricao='Receita Teste')
            db.session.add(despesa)
            db.session.add(receita)
            
        db.session.commit()