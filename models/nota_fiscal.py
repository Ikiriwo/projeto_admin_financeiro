from . import db
from datetime import datetime

class NotaFiscal(db.Model):
    """
    Modelo para representar notas fiscais (mantido para compatibilidade com código existente)
    """
    id = db.Column(db.Integer, primary_key=True)
    razao_social_fornecedor = db.Column(db.String(255))
    cnpj_fornecedor = db.Column(db.String(20))
    nome_faturado = db.Column(db.String(255))
    cpf_faturado = db.Column(db.String(20))
    numero_nota = db.Column(db.String(50))
    data_emissao = db.Column(db.Date)
    data_validade = db.Column(db.Date)
    valor_total = db.Column(db.Float)
    quantidade_parcelas = db.Column(db.Integer)
    classificacao_despesa = db.Column(db.String(50))
    data_processamento = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<NotaFiscal {self.numero_nota}>'

class ProdutoNotaFiscal(db.Model):
    """
    Modelo para representar produtos de uma nota fiscal
    """
    id = db.Column(db.Integer, primary_key=True)
    nota_fiscal_id = db.Column(db.Integer, db.ForeignKey('nota_fiscal.id'))
    descricao = db.Column(db.String(255))
    
    # Relacionamento com NotaFiscal
    nota_fiscal = db.relationship('NotaFiscal', backref=db.backref('produtos', lazy=True))
    
    def __repr__(self):
        return f'<ProdutoNotaFiscal {self.descricao}>'