from . import db
from datetime import datetime

class ParcelasContas(db.Model):
    """
    Modelo para representar parcelas de contas a pagar ou receber
    """
    id = db.Column(db.Integer, primary_key=True)
    identificacao = db.Column(db.String(100), unique=True, nullable=False)
    numero_nota = db.Column(db.String(50))
    data_emissao = db.Column(db.Date)
    data_vencimento = db.Column(db.Date)
    valor_total = db.Column(db.Float)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ParcelasContas {self.identificacao}>'
    
    @classmethod
    def criar_nova(cls, identificacao, numero_nota, data_emissao, data_vencimento, valor_total):
        """
        Cria uma nova parcela no banco de dados
        """
        parcela = cls(
            identificacao=identificacao,
            numero_nota=numero_nota,
            data_emissao=data_emissao,
            data_vencimento=data_vencimento,
            valor_total=valor_total
        )
        db.session.add(parcela)
        db.session.commit()
        return parcela