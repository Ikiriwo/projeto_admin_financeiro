from . import db
from datetime import datetime

class Classificacao(db.Model):
    """
    Modelo para representar classificações de despesas e receitas
    """
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))  # DESPESA, RECEITA
    descricao = db.Column(db.String(255), nullable=False)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Classificacao {self.descricao}>'
    
    @classmethod
    def verificar_existencia(cls, tipo, descricao):
        """
        Verifica se uma classificação existe no banco de dados pelo tipo e descrição
        """
        return cls.query.filter_by(tipo=tipo, descricao=descricao).first()
    
    @classmethod
    def criar_nova(cls, tipo, descricao):
        """
        Cria uma nova classificação no banco de dados
        """
        classificacao = cls(
            tipo=tipo,
            descricao=descricao
        )
        db.session.add(classificacao)
        db.session.commit()
        return classificacao