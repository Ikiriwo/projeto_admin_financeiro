"""
Modelo para armazenar embeddings de documentos para busca semântica.
"""

from datetime import datetime
from . import db
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Text, Index


class DocumentEmbedding(db.Model):
    """
    Armazena embeddings vetoriais de documentos (notas fiscais).

    Esta tabela permite busca semântica usando pgvector ou busca por similaridade.
    """
    __tablename__ = 'document_embeddings'

    id = db.Column(db.Integer, primary_key=True)

    # Referência ao documento original
    document_id = db.Column(db.Integer, db.ForeignKey('nota_fiscal.id'), nullable=True)
    document_type = db.Column(db.String(50), nullable=False, default='nota_fiscal')

    # Conteúdo textual do documento
    content = db.Column(Text, nullable=False)

    # Embedding vetorial (array de floats)
    # Para pgvector, seria: db.Column(Vector(768))
    # Por ora, usamos ARRAY de floats do PostgreSQL
    embedding = db.Column(ARRAY(db.Float), nullable=False)

    # Dimensionalidade do vetor (768 para text-embedding-004 do Gemini)
    embedding_dimension = db.Column(db.Integer, nullable=False, default=768)

    # Modelo usado para gerar o embedding
    embedding_model = db.Column(db.String(100), nullable=False, default='models/text-embedding-004')

    # Metadados adicionais em JSON
    meta = db.Column(db.JSON, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamento com nota fiscal
    nota_fiscal = db.relationship('NotaFiscal', backref='embeddings', lazy=True)

    def __repr__(self):
        return f'<DocumentEmbedding {self.id} - {self.document_type}>'

    @classmethod
    def criar_novo(cls, document_id, document_type, content, embedding, meta=None, embedding_model=None):
        """
        Cria um novo embedding de documento.

        Args:
            document_id: ID do documento de origem
            document_type: Tipo do documento (nota_fiscal, etc)
            content: Conteúdo textual do documento
            embedding: Lista/array de floats representando o vetor
            meta: Metadados adicionais (dict)
            embedding_model: Nome do modelo usado (opcional)

        Returns:
            Instância do DocumentEmbedding criado
        """
        embedding_obj = cls(
            document_id=document_id,
            document_type=document_type,
            content=content,
            embedding=embedding,
            embedding_dimension=len(embedding),
            embedding_model=embedding_model or 'models/text-embedding-004',
            meta=meta or {}
        )

        db.session.add(embedding_obj)
        db.session.commit()

        return embedding_obj

    @classmethod
    def buscar_por_documento(cls, document_id):
        """
        Busca embeddings de um documento específico.

        Args:
            document_id: ID do documento

        Returns:
            Lista de embeddings do documento
        """
        return cls.query.filter_by(document_id=document_id).all()

    @classmethod
    def deletar_por_documento(cls, document_id):
        """
        Remove todos os embeddings de um documento.

        Args:
            document_id: ID do documento
        """
        cls.query.filter_by(document_id=document_id).delete()
        db.session.commit()

    def calcular_similaridade_cosseno(self, outro_embedding):
        """
        Calcula a similaridade de cosseno entre este embedding e outro.

        Args:
            outro_embedding: Lista de floats representando outro vetor

        Returns:
            Float entre -1 e 1 representando a similaridade
        """
        import numpy as np

        vec1 = np.array(self.embedding)
        vec2 = np.array(outro_embedding)

        # Calcula o produto escalar
        dot_product = np.dot(vec1, vec2)

        # Calcula as normas
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        # Evita divisão por zero
        if norm1 == 0 or norm2 == 0:
            return 0.0

        # Similaridade de cosseno
        similarity = dot_product / (norm1 * norm2)

        return float(similarity)


# Criar índice para melhorar performance nas buscas
Index('idx_document_embeddings_type', DocumentEmbedding.document_type)
Index('idx_document_embeddings_document_id', DocumentEmbedding.document_id)
