from . import db
from datetime import datetime

class Classificacao(db.Model):
    """
    Modelo para representar classificações de despesas e receitas
    """
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))  # DESPESA, RECEITA
    descricao = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default='ATIVO', nullable=False)  # ATIVO, INATIVO
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Classificacao {self.descricao}>'
    
    @classmethod
    def verificar_existencia(cls, tipo, descricao, incluir_inativos=False):
        """
        Verifica se uma classificação existe no banco de dados pelo tipo e descrição
        Por padrão, retorna apenas registros com status ATIVO.
        """
        query = cls.query.filter_by(tipo=tipo, descricao=descricao)
        if not incluir_inativos:
            query = query.filter_by(status='ATIVO')
        return query.first()

    @classmethod
    def criar_nova(cls, tipo, descricao, status='ATIVO'):
        """
        Cria uma nova classificação no banco de dados
        """
        classificacao = cls(
            tipo=tipo,
            descricao=descricao,
            status=status
        )
        db.session.add(classificacao)
        db.session.commit()
        return classificacao

    @classmethod
    def listar_todos(cls, tipo=None, incluir_inativos=False):
        """
        Lista todas as classificações, opcionalmente filtradas por tipo.
        Por padrão, retorna apenas registros com status ATIVO.
        """
        query = cls.query
        if not incluir_inativos:
            query = query.filter_by(status='ATIVO')
        if tipo is not None:
            query = query.filter_by(tipo=tipo)
        return query.order_by(cls.data_cadastro.desc()).all()

    def atualizar(self, **kwargs):
        """
        Atualiza os campos da classificação
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
        return self

    def excluir_logico(self):
        """
        Realiza exclusão lógica, alterando o status para INATIVO
        """
        self.status = 'INATIVO'
        db.session.commit()
        return self