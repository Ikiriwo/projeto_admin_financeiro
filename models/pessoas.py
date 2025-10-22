from . import db
from datetime import datetime

class Pessoas(db.Model):
    """
    Modelo para representar pessoas (fornecedores, clientes ou faturados)
    """
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))  # CLIENTE-FORNECEDOR, FATURADO
    razao_social = db.Column(db.String(255), nullable=False)
    cpf_cnpj = db.Column(db.String(20), nullable=False, unique=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Pessoas {self.razao_social}>'
    
    @classmethod
    def verificar_existencia(cls, cpf_cnpj):
        """
        Verifica se uma pessoa existe no banco de dados pelo CPF/CNPJ
        """
        return cls.query.filter_by(cpf_cnpj=cpf_cnpj).first()
    
    @classmethod
    def criar_novo(cls, tipo, razao_social, cpf_cnpj):
        """
        Cria uma nova pessoa no banco de dados
        """
        pessoa = cls(
            tipo=tipo,
            razao_social=razao_social,
            cpf_cnpj=cpf_cnpj
        )
        db.session.add(pessoa)
        db.session.commit()
        return pessoa