"""
Sistema RAG (Retrieval-Augmented Generation) para consultas inteligentes ao banco de dados.

Este módulo implementa duas abordagens:
1. RAG Simples: Busca direta no banco de dados usando SQL + LLM para elaborar respostas
2. RAG com Embeddings: Busca semântica usando vetorização para encontrar informações relevantes
"""

from .rag_simple import RAGSimple
from .rag_embeddings import RAGEmbeddings
from .database_retriever import DatabaseRetriever

__all__ = ['RAGSimple', 'RAGEmbeddings', 'DatabaseRetriever']
