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
    status = db.Column(db.String(20), default='ATIVO', nullable=False)  # ATIVO, INATIVO
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Pessoas {self.razao_social}>'
    
    @classmethod
    def verificar_existencia(cls, tipo=None, cpf_cnpj=None, incluir_inativos=False):
        """
        Verifica se uma pessoa existe no banco de dados.
        Pode filtrar por tipo (CLIENTE-FORNECEDOR, FATURADO) e/ou CPF/CNPJ.
        Por padrão, retorna apenas registros com status ATIVO.
        """
        query = cls.query
        if not incluir_inativos:
            query = query.filter_by(status='ATIVO')
        if tipo is not None:
            query = query.filter_by(tipo=tipo)
        if cpf_cnpj is not None:
            query = query.filter_by(cpf_cnpj=cpf_cnpj)
        return query.first()
    
    @classmethod
    def criar_novo(cls, tipo, razao_social, cpf_cnpj, status='ATIVO'):
        """
        Cria uma nova pessoa no banco de dados
        """
        pessoa = cls(
            tipo=tipo,
            razao_social=razao_social,
            cpf_cnpj=cpf_cnpj,
            status=status
        )
        db.session.add(pessoa)
        db.session.commit()
        return pessoa

    @classmethod
    def listar_todos(cls, tipo=None, incluir_inativos=False):
        """
        Lista todas as pessoas, opcionalmente filtradas por tipo.
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
        Atualiza os campos da pessoa
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