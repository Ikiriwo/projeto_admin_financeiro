from . import db
from datetime import datetime

# Tabela de relacionamento N:N entre MovimentoContas e Classificacao
movimento_classificacao = db.Table('movimento_classificacao',
    db.Column('movimento_id', db.Integer, db.ForeignKey('movimento_contas.id'), primary_key=True),
    db.Column('classificacao_id', db.Integer, db.ForeignKey('classificacao.id'), primary_key=True)
)

class MovimentoContas(db.Model):
    """
    Modelo para representar movimentos contábeis (contas a pagar ou receber)
    """
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))  # APAGAR, ARECEBER
    parcela_id = db.Column(db.Integer, db.ForeignKey('parcelas_contas.id'))
    fornecedor_cliente_id = db.Column(db.Integer, db.ForeignKey('pessoas.id'))
    faturado_id = db.Column(db.Integer, db.ForeignKey('pessoas.id'))
    valor = db.Column(db.Float)
    status = db.Column(db.String(20), default='ATIVO', nullable=False)  # ATIVO, INATIVO
    data_movimento = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    parcela = db.relationship('ParcelasContas', backref=db.backref('movimentos', lazy=True))
    fornecedor_cliente = db.relationship('Pessoas', foreign_keys=[fornecedor_cliente_id], backref=db.backref('movimentos_fornecedor', lazy=True))
    faturado = db.relationship('Pessoas', foreign_keys=[faturado_id], backref=db.backref('movimentos_faturado', lazy=True))
    classificacoes = db.relationship('Classificacao', secondary=movimento_classificacao, lazy='subquery',
                                    backref=db.backref('movimentos', lazy=True))
    
    def __repr__(self):
        return f'<MovimentoContas {self.id}>'
    
    @classmethod
    def criar_novo(cls, tipo, parcela_id, fornecedor_cliente_id, faturado_id, valor, classificacoes=None, status='ATIVO'):
        """
        Cria um novo movimento contábil no banco de dados
        """
        movimento = cls(
            tipo=tipo,
            parcela_id=parcela_id,
            fornecedor_cliente_id=fornecedor_cliente_id,
            faturado_id=faturado_id,
            valor=valor,
            status=status
        )

        db.session.add(movimento)

        # Adiciona as classificações ao movimento
        if classificacoes:
            for classificacao in classificacoes:
                movimento.classificacoes.append(classificacao)

        db.session.commit()
        return movimento

    @classmethod
    def listar_todos(cls, tipo=None, incluir_inativos=False):
        """
        Lista todos os movimentos, opcionalmente filtrados por tipo.
        Por padrão, retorna apenas registros com status ATIVO.
        """
        query = cls.query
        if not incluir_inativos:
            query = query.filter_by(status='ATIVO')
        if tipo is not None:
            query = query.filter_by(tipo=tipo)
        return query.order_by(cls.data_movimento.desc()).all()

    def atualizar(self, **kwargs):
        """
        Atualiza os campos do movimento
        """
        for key, value in kwargs.items():
            if hasattr(self, key) and key != 'classificacoes':
                setattr(self, key, value)

        # Tratar classificações separadamente
        if 'classificacoes' in kwargs:
            self.classificacoes = kwargs['classificacoes']

        db.session.commit()
        return self

    def excluir_logico(self):
        """
        Realiza exclusão lógica, alterando o status para INATIVO
        """
        self.status = 'INATIVO'
        db.session.commit()
        return self