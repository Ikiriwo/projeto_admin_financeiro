"""
Implementação do RAG Simples.

Esta abordagem usa consultas SQL diretas ao banco de dados e o LLM (Gemini)
para elaborar respostas naturais e informativas.
"""

import os
import google.generativeai as genai
from typing import Dict, Any, List
from .database_retriever import DatabaseRetriever


class RAGSimple:
    """
    Implementação do RAG Simples que combina busca SQL com LLM.

    O sistema analisa a pergunta do usuário, executa consultas relevantes
    no banco de dados e usa o Gemini para elaborar uma resposta natural.
    """

    def __init__(self, db):
        """
        Inicializa o sistema RAG Simples.

        Args:
            db: Instância do SQLAlchemy database
        """
        self.db = db
        self.retriever = DatabaseRetriever(db)

        # Configura o Gemini
        api_key = os.environ.get('GEMINI_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            os.environ.get('GEMINI_MODEL', 'gemini-2.0-flash')
        )

    def _analyze_question(self, question: str) -> Dict[str, Any]:
        """
        Analisa a pergunta para determinar o tipo de consulta necessária.

        Args:
            question: Pergunta do usuário

        Returns:
            Dicionário com tipo de consulta e parâmetros
        """
        question_lower = question.lower()

        # Identifica o tipo de pergunta
        if any(word in question_lower for word in ['total', 'quanto', 'soma', 'valor', 'gasto']):
            if any(word in question_lower for word in ['fornecedor', 'fornecedores']):
                return {'type': 'maiores_fornecedores', 'params': {}}
            elif any(word in question_lower for word in ['classificação', 'classificacao', 'categoria']):
                return {'type': 'por_classificacao', 'params': {}}
            elif any(word in question_lower for word in ['período', 'periodo', 'dias', 'mês', 'mes']):
                # Tenta extrair número de dias
                dias = 30  # padrão
                words = question_lower.split()
                for i, word in enumerate(words):
                    if word.isdigit():
                        dias = int(word)
                        break
                return {'type': 'total_periodo', 'params': {'dias': dias}}
            else:
                return {'type': 'resumo_geral', 'params': {}}

        elif any(word in question_lower for word in ['fornecedor', 'empresa']):
            # Busca por fornecedor específico
            palavras = question_lower.replace('fornecedor', '').replace('empresa', '').strip().split()
            termo = ' '.join([p for p in palavras if len(p) > 3])
            return {'type': 'buscar_fornecedor', 'params': {'termo': termo}}

        elif any(word in question_lower for word in ['nota', 'notas', 'fiscal', 'fiscais']):
            return {'type': 'listar_notas', 'params': {}}

        elif any(word in question_lower for word in ['resumo', 'overview', 'visão geral', 'visao geral']):
            return {'type': 'resumo_geral', 'params': {}}

        elif any(word in question_lower for word in ['estrutura', 'esquema', 'tabelas', 'banco']):
            return {'type': 'esquema', 'params': {}}

        # Pergunta genérica
        return {'type': 'resumo_geral', 'params': {}}

    def _retrieve_data(self, query_type: str, params: Dict[str, Any]) -> Any:
        """
        Recupera dados do banco de dados baseado no tipo de consulta.

        Args:
            query_type: Tipo de consulta a executar
            params: Parâmetros para a consulta

        Returns:
            Dados recuperados do banco
        """
        if query_type == 'maiores_fornecedores':
            return self.retriever.get_maiores_fornecedores()

        elif query_type == 'por_classificacao':
            return self.retriever.get_despesas_por_classificacao()

        elif query_type == 'total_periodo':
            dias = params.get('dias', 30)
            return self.retriever.get_total_despesas_por_periodo(dias)

        elif query_type == 'buscar_fornecedor':
            termo = params.get('termo', '')
            return self.retriever.search_by_fornecedor(termo)

        elif query_type == 'listar_notas':
            return self.retriever.search_notas_fiscais()

        elif query_type == 'esquema':
            return self.retriever.get_database_schema()

        elif query_type == 'resumo_geral':
            return self.retriever.get_resumo_financeiro()

        return None

    def _format_context(self, data: Any, query_type: str) -> str:
        """
        Formata os dados recuperados em um contexto para o LLM.

        Args:
            data: Dados recuperados do banco
            query_type: Tipo de consulta executada

        Returns:
            Contexto formatado como string
        """
        if query_type == 'esquema':
            return f"CONTEXTO DO BANCO DE DADOS:\n{data}"

        elif query_type == 'resumo_geral':
            return f"""
RESUMO FINANCEIRO:
- Total de notas fiscais: {data['total_notas_fiscais']}
- Valor total geral: R$ {data['valor_total_geral']:,.2f}
- Valor últimos 30 dias: R$ {data['valor_ultimos_30_dias']:,.2f}
- Total de fornecedores únicos: {data['total_fornecedores_unicos']}
"""

        elif query_type == 'total_periodo':
            return f"""
DESPESAS NO PERÍODO ({data['periodo_dias']} dias):
- Quantidade de notas: {data['quantidade_notas']}
- Total de despesas: R$ {data['total_despesas']:,.2f}
"""

        elif query_type == 'maiores_fornecedores':
            context = "MAIORES FORNECEDORES:\n"
            for i, fornecedor in enumerate(data, 1):
                context += f"{i}. {fornecedor['fornecedor']} (CNPJ: {fornecedor['cnpj']})\n"
                context += f"   - Notas: {fornecedor['quantidade_notas']}\n"
                context += f"   - Total gasto: R$ {fornecedor['total_gasto']:,.2f}\n"
            return context

        elif query_type == 'por_classificacao':
            context = "DESPESAS POR CLASSIFICAÇÃO:\n"
            for i, item in enumerate(data, 1):
                context += f"{i}. {item['classificacao']}\n"
                context += f"   - Quantidade: {item['quantidade']}\n"
                context += f"   - Total: R$ {item['total']:,.2f}\n"
            return context

        elif query_type == 'buscar_fornecedor':
            if not data:
                return "Nenhuma nota fiscal encontrada para este fornecedor."
            context = f"NOTAS FISCAIS ENCONTRADAS ({len(data)}):\n"
            for nota in data[:10]:  # Limita a 10 para não sobrecarregar
                context += f"- Nota {nota['numero_nota']}: R$ {nota['valor_total']:,.2f} "
                context += f"({nota['data_emissao']}) - {nota['classificacao']}\n"
            return context

        elif query_type == 'listar_notas':
            if not data:
                return "Nenhuma nota fiscal encontrada."
            context = f"ÚLTIMAS NOTAS FISCAIS ({len(data)}):\n"
            for nota in data[:15]:  # Limita a 15
                context += f"- Nota {nota['numero_nota']}: {nota['fornecedor']}\n"
                context += f"  Valor: R$ {nota['valor_total']:,.2f} - {nota['data_emissao']}\n"
                context += f"  Classificação: {nota['classificacao']}\n"
            return context

        return str(data)

    def answer_question(self, question: str) -> Dict[str, Any]:
        """
        Processa uma pergunta e retorna uma resposta elaborada.

        Args:
            question: Pergunta do usuário

        Returns:
            Dicionário com resposta e metadados
        """
        try:
            # 1. Analisa a pergunta
            query_info = self._analyze_question(question)

            # 2. Recupera dados relevantes
            data = self._retrieve_data(query_info['type'], query_info['params'])

            # 3. Formata o contexto
            context = self._format_context(data, query_info['type'])

            # 4. Cria o prompt para o LLM
            prompt = f"""
Você é um assistente financeiro especializado em análise de dados.
O usuário fez a seguinte pergunta sobre o sistema financeiro:

PERGUNTA: {question}

Aqui estão os dados relevantes do banco de dados:

{context}

Sua tarefa é fornecer uma resposta clara, objetiva e profissional:
- Responda diretamente a pergunta do usuário
- Use os dados fornecidos no contexto
- Formate valores monetários corretamente (R$)
- Seja conciso mas completo
- Se houver insights interessantes nos dados, mencione-os
- Use bullet points quando apropriado para melhor legibilidade

RESPOSTA:
"""

            # 5. Gera a resposta com o LLM
            response = self.model.generate_content(prompt)

            return {
                'success': True,
                'question': question,
                'answer': response.text,
                'query_type': query_info['type'],
                'data_retrieved': data,
                'method': 'RAG_SIMPLE'
            }

        except Exception as e:
            return {
                'success': False,
                'question': question,
                'error': str(e),
                'answer': f'Erro ao processar a pergunta: {str(e)}',
                'method': 'RAG_SIMPLE'
            }

    def get_available_queries(self) -> List[str]:
        """
        Retorna exemplos de perguntas que o sistema pode responder.

        Returns:
            Lista com exemplos de perguntas
        """
        return [
            "Qual é o resumo financeiro geral?",
            "Quais são os maiores fornecedores?",
            "Qual o total de despesas dos últimos 30 dias?",
            "Mostre as despesas por classificação",
            "Liste as últimas notas fiscais processadas",
            "Qual é a estrutura do banco de dados?",
            "Busque notas do fornecedor [nome]",
            "Quanto foi gasto nos últimos 60 dias?"
        ]
