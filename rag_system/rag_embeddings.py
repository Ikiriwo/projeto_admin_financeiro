"""
Implementação do RAG com Embeddings.

Esta abordagem usa vetorização semântica para buscar documentos relevantes
e combina com LLM para gerar respostas contextualizadas.
"""

import os
import numpy as np
import google.generativeai as genai
from typing import Dict, Any, List, Tuple
from models.document_embeddings import DocumentEmbedding
from models.nota_fiscal import NotaFiscal
from models import db


class RAGEmbeddings:
    """
    Implementação do RAG com Embeddings para busca semântica.

    Usa Google Gemini Embeddings API para gerar embeddings e busca por similaridade.
    """

    def __init__(self, database, model_name='models/text-embedding-004'):
        """
        Inicializa o sistema RAG com Embeddings.

        Args:
            database: Instância do SQLAlchemy database
            model_name: Nome do modelo de embeddings (padrão: models/text-embedding-004)
        """
        self.db = database
        self.model_name = model_name

        # Configura o Gemini
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY não encontrada nas variáveis de ambiente")

        genai.configure(api_key=api_key)

        print(f"Usando modelo de embeddings: {model_name}")

        # Modelo para geração de respostas
        self.llm_model = genai.GenerativeModel(
            os.environ.get('GEMINI_MODEL', 'gemini-2.0-flash')
        )

    def generate_embedding(self, text: str) -> List[float]:
        """
        Gera um embedding vetorial para um texto usando a API do Gemini.

        Args:
            text: Texto para gerar embedding

        Returns:
            Lista de floats representando o vetor
        """
        try:
            # Usa a API de embeddings do Gemini
            result = genai.embed_content(
                model=self.model_name,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            print(f"Erro ao gerar embedding: {e}")
            raise

    def index_nota_fiscal(self, nota_fiscal_id: int) -> bool:
        """
        Indexa uma nota fiscal criando seu embedding.

        Args:
            nota_fiscal_id: ID da nota fiscal

        Returns:
            True se indexou com sucesso, False caso contrário
        """
        try:
            # Busca a nota fiscal
            nota = NotaFiscal.query.get(nota_fiscal_id)
            if not nota:
                print(f"Nota fiscal {nota_fiscal_id} não encontrada")
                return False

            # Cria texto da nota fiscal
            content = self._format_nota_fiscal_text(nota)

            # Gera embedding
            embedding = self.generate_embedding(content)

            # Metadados
            meta = {
                'numero_nota': nota.numero_nota,
                'fornecedor': nota.razao_social_fornecedor,
                'valor_total': float(nota.valor_total) if nota.valor_total else 0,
                'classificacao': nota.classificacao_despesa
            }

            # Remove embeddings antigos (se existirem)
            DocumentEmbedding.deletar_por_documento(nota_fiscal_id)

            # Cria novo embedding
            DocumentEmbedding.criar_novo(
                document_id=nota_fiscal_id,
                document_type='nota_fiscal',
                content=content,
                embedding=embedding,
                meta=meta,
                embedding_model=self.model_name
            )

            print(f"Nota fiscal {nota_fiscal_id} indexada com sucesso")
            return True

        except Exception as e:
            print(f"Erro ao indexar nota fiscal {nota_fiscal_id}: {e}")
            return False

    def index_all_notas_fiscais(self) -> Dict[str, Any]:
        """
        Indexa todas as notas fiscais do banco de dados.

        Returns:
            Dicionário com estatísticas da indexação
        """
        try:
            notas = NotaFiscal.query.all()
            total = len(notas)
            success_count = 0

            print(f"Iniciando indexação de {total} notas fiscais...")

            for i, nota in enumerate(notas, 1):
                print(f"Indexando nota {i}/{total}...")
                if self.index_nota_fiscal(nota.id):
                    success_count += 1

            print(f"Indexação concluída: {success_count}/{total} notas indexadas")

            return {
                'success': True,
                'total_notas': total,
                'indexed': success_count,
                'failed': total - success_count
            }

        except Exception as e:
            print(f"Erro ao indexar notas fiscais: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def _format_nota_fiscal_text(self, nota: NotaFiscal) -> str:
        """
        Formata uma nota fiscal como texto para indexação.

        Args:
            nota: Instância de NotaFiscal

        Returns:
            Texto formatado da nota fiscal
        """
        parts = []

        if nota.razao_social_fornecedor:
            parts.append(f"Fornecedor: {nota.razao_social_fornecedor}")

        if nota.cnpj_fornecedor:
            parts.append(f"CNPJ: {nota.cnpj_fornecedor}")

        if nota.numero_nota:
            parts.append(f"Nota Fiscal: {nota.numero_nota}")

        if nota.data_emissao:
            parts.append(f"Data de Emissão: {nota.data_emissao.strftime('%d/%m/%Y')}")

        if nota.valor_total:
            parts.append(f"Valor Total: R$ {nota.valor_total:,.2f}")

        if nota.classificacao_despesa:
            parts.append(f"Classificação: {nota.classificacao_despesa}")

        # Adiciona produtos se houver
        if nota.produtos:
            produtos_desc = ", ".join([p.descricao for p in nota.produtos if p.descricao])
            if produtos_desc:
                parts.append(f"Produtos: {produtos_desc}")

        return " | ".join(parts)

    def search_similar_documents(self, query: str, top_k: int = 5) -> List[Tuple[DocumentEmbedding, float]]:
        """
        Busca documentos similares à query usando embeddings.

        Args:
            query: Texto da consulta
            top_k: Número de documentos a retornar

        Returns:
            Lista de tuplas (DocumentEmbedding, similaridade)
        """
        try:
            # Gera embedding da query usando task_type específico para queries
            result = genai.embed_content(
                model=self.model_name,
                content=query,
                task_type="retrieval_query"
            )
            query_embedding = result['embedding']

            # Busca todos os embeddings
            all_embeddings = DocumentEmbedding.query.all()

            if not all_embeddings:
                return []

            # Calcula similaridades
            similarities = []
            for doc_emb in all_embeddings:
                similarity = self._cosine_similarity(query_embedding, doc_emb.embedding)
                similarities.append((doc_emb, similarity))

            # Ordena por similaridade (maior primeiro)
            similarities.sort(key=lambda x: x[1], reverse=True)

            # Retorna top_k
            return similarities[:top_k]

        except Exception as e:
            print(f"Erro ao buscar documentos similares: {e}")
            return []

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calcula a similaridade de cosseno entre dois vetores.

        Args:
            vec1: Primeiro vetor
            vec2: Segundo vetor

        Returns:
            Similaridade entre 0 e 1
        """
        vec1_np = np.array(vec1)
        vec2_np = np.array(vec2)

        dot_product = np.dot(vec1_np, vec2_np)
        norm1 = np.linalg.norm(vec1_np)
        norm2 = np.linalg.norm(vec2_np)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return float(dot_product / (norm1 * norm2))

    def answer_question(self, question: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Responde uma pergunta usando busca semântica + LLM.

        Args:
            question: Pergunta do usuário
            top_k: Número de documentos a recuperar

        Returns:
            Dicionário com resposta e metadados
        """
        try:
            # 1. Busca documentos similares
            similar_docs = self.search_similar_documents(question, top_k)

            if not similar_docs:
                return {
                    'success': False,
                    'question': question,
                    'error': 'Nenhum documento encontrado no banco de dados',
                    'answer': 'Não há documentos indexados no sistema. Por favor, indexe as notas fiscais primeiro.',
                    'method': 'RAG_EMBEDDINGS'
                }

            # 2. Formata o contexto
            context = self._format_context_from_docs(similar_docs)

            # 3. Cria o prompt para o LLM
            prompt = f"""
Você é um assistente financeiro especializado em análise de dados.
O usuário fez a seguinte pergunta sobre o sistema financeiro:

PERGUNTA: {question}

Aqui estão os documentos mais relevantes encontrados no banco de dados (ordenados por relevância):

{context}

Sua tarefa é fornecer uma resposta clara, objetiva e profissional:
- Responda diretamente a pergunta do usuário
- Use os dados fornecidos no contexto dos documentos
- Formate valores monetários corretamente (R$)
- Seja conciso mas completo
- Se houver insights interessantes nos dados, mencione-os
- Use bullet points quando apropriado para melhor legibilidade
- Indique o nível de confiança da resposta baseado na relevância dos documentos

RESPOSTA:
"""

            # 4. Gera a resposta com o LLM
            response = self.llm_model.generate_content(prompt)

            # 5. Prepara metadados
            documents_metadata = [
                {
                    'content': doc.content[:200] + '...' if len(doc.content) > 200 else doc.content,
                    'similarity': float(sim),
                    'metadata': doc.meta if doc.meta else {}
                }
                for doc, sim in similar_docs
            ]

            return {
                'success': True,
                'question': question,
                'answer': response.text,
                'method': 'RAG_EMBEDDINGS',
                'documents_retrieved': len(similar_docs),
                'documents': documents_metadata
            }

        except Exception as e:
            return {
                'success': False,
                'question': question,
                'error': str(e),
                'answer': f'Erro ao processar a pergunta: {str(e)}',
                'method': 'RAG_EMBEDDINGS'
            }

    def _format_context_from_docs(self, docs_with_similarity: List[Tuple[DocumentEmbedding, float]]) -> str:
        """
        Formata os documentos recuperados em contexto para o LLM.

        Args:
            docs_with_similarity: Lista de tuplas (DocumentEmbedding, similaridade)

        Returns:
            Contexto formatado como string
        """
        context_parts = []

        for i, (doc, similarity) in enumerate(docs_with_similarity, 1):
            context_parts.append(f"\n--- DOCUMENTO {i} (Relevância: {similarity:.2%}) ---")
            context_parts.append(doc.content)

            # Adiciona metadados se houver
            if doc.meta:
                context_parts.append(f"Metadados: {doc.meta}")

        return "\n".join(context_parts)

    def get_index_status(self) -> Dict[str, Any]:
        """
        Retorna o status da indexação.

        Returns:
            Dicionário com estatísticas do índice
        """
        total_embeddings = DocumentEmbedding.query.count()
        total_notas = NotaFiscal.query.count()

        return {
            'total_documents_indexed': total_embeddings,
            'total_notas_fiscais': total_notas,
            'indexation_percentage': (total_embeddings / total_notas * 100) if total_notas > 0 else 0,
            'model_used': self.model_name
        }
