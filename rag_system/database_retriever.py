"""
Módulo para recuperação de dados do banco de dados PostgreSQL.
Realiza consultas SQL otimizadas para buscar informações relevantes.
"""

from sqlalchemy import text, func
from datetime import datetime, timedelta
from typing import Dict, List, Any


class DatabaseRetriever:
    """Classe responsável por recuperar dados do banco de dados para o sistema RAG."""

    def __init__(self, db):
        """
        Inicializa o recuperador de dados.

        Args:
            db: Instância do SQLAlchemy database
        """
        self.db = db

    def get_database_schema(self) -> str:
        """
        Retorna uma descrição do esquema do banco de dados.

        Returns:
            str: Descrição textual do esquema do banco de dados
        """
        schema_description = """
        ESQUEMA DO BANCO DE DADOS:

        1. Tabela 'pessoas':
           - Armazena fornecedores e clientes
           - Campos: id, tipo (CLIENTE-FORNECEDOR/FATURADO), razao_social, cpf_cnpj, data_cadastro

        2. Tabela 'classificacao':
           - Categorias de despesas e receitas
           - Campos: id, tipo (DESPESA/RECEITA), descricao, data_cadastro

        3. Tabela 'nota_fiscal':
           - Notas fiscais processadas
           - Campos: id, razao_social_fornecedor, cnpj_fornecedor, nome_faturado, cpf_faturado,
                    numero_nota, data_emissao, data_validade, valor_total, quantidade_parcelas,
                    classificacao_despesa, data_processamento

        4. Tabela 'parcelas_contas':
           - Parcelas a pagar/receber
           - Campos: id, identificacao, numero_nota, data_emissao, data_vencimento,
                    valor_total, data_cadastro

        5. Tabela 'movimento_contas':
           - Movimentos contábeis
           - Campos: id, tipo (APAGAR/ARECEBER), parcela_id, fornecedor_cliente_id,
                    faturado_id, valor, data_movimento
        """
        return schema_description

    def search_notas_fiscais(self, filters: Dict[str, Any] = None) -> List[Dict]:
        """
        Busca notas fiscais com filtros opcionais.

        Args:
            filters: Dicionário com filtros (fornecedor, data_inicio, data_fim, etc.)

        Returns:
            Lista de dicionários com dados das notas fiscais
        """
        query = text("""
            SELECT
                id,
                razao_social_fornecedor,
                cnpj_fornecedor,
                nome_faturado,
                numero_nota,
                data_emissao,
                valor_total,
                quantidade_parcelas,
                classificacao_despesa,
                data_processamento
            FROM nota_fiscal
            WHERE 1=1
            ORDER BY data_emissao DESC
            LIMIT 50
        """)

        result = self.db.session.execute(query)
        rows = result.fetchall()

        return [
            {
                'id': row[0],
                'fornecedor': row[1],
                'cnpj': row[2],
                'faturado': row[3],
                'numero_nota': row[4],
                'data_emissao': row[5].strftime('%d/%m/%Y') if row[5] else None,
                'valor_total': float(row[6]) if row[6] else 0,
                'parcelas': row[7],
                'classificacao': row[8],
                'data_processamento': row[9].strftime('%d/%m/%Y %H:%M') if row[9] else None
            }
            for row in rows
        ]

    def get_total_despesas_por_periodo(self, dias: int = 30) -> Dict[str, Any]:
        """
        Calcula o total de despesas em um período.

        Args:
            dias: Número de dias para considerar no cálculo

        Returns:
            Dicionário com total de despesas e quantidade de notas
        """
        data_inicio = datetime.now() - timedelta(days=dias)

        query = text("""
            SELECT
                COUNT(*) as quantidade_notas,
                COALESCE(SUM(valor_total), 0) as total_despesas
            FROM nota_fiscal
            WHERE data_emissao >= :data_inicio
        """)

        result = self.db.session.execute(query, {'data_inicio': data_inicio})
        row = result.fetchone()

        return {
            'periodo_dias': dias,
            'quantidade_notas': row[0],
            'total_despesas': float(row[1]) if row[1] else 0
        }

    def get_despesas_por_classificacao(self, limit: int = 10) -> List[Dict]:
        """
        Retorna as despesas agrupadas por classificação.

        Args:
            limit: Número máximo de classificações a retornar

        Returns:
            Lista com classificações e totais
        """
        query = text("""
            SELECT
                classificacao_despesa,
                COUNT(*) as quantidade,
                SUM(valor_total) as total
            FROM nota_fiscal
            WHERE classificacao_despesa IS NOT NULL
            GROUP BY classificacao_despesa
            ORDER BY total DESC
            LIMIT :limit
        """)

        result = self.db.session.execute(query, {'limit': limit})
        rows = result.fetchall()

        return [
            {
                'classificacao': row[0],
                'quantidade': row[1],
                'total': float(row[2]) if row[2] else 0
            }
            for row in rows
        ]

    def get_maiores_fornecedores(self, limit: int = 10) -> List[Dict]:
        """
        Retorna os maiores fornecedores por valor total.

        Args:
            limit: Número de fornecedores a retornar

        Returns:
            Lista com fornecedores e totais
        """
        query = text("""
            SELECT
                razao_social_fornecedor,
                cnpj_fornecedor,
                COUNT(*) as quantidade_notas,
                SUM(valor_total) as total_gasto
            FROM nota_fiscal
            GROUP BY razao_social_fornecedor, cnpj_fornecedor
            ORDER BY total_gasto DESC
            LIMIT :limit
        """)

        result = self.db.session.execute(query, {'limit': limit})
        rows = result.fetchall()

        return [
            {
                'fornecedor': row[0],
                'cnpj': row[1],
                'quantidade_notas': row[2],
                'total_gasto': float(row[3]) if row[3] else 0
            }
            for row in rows
        ]

    def search_by_fornecedor(self, termo_busca: str) -> List[Dict]:
        """
        Busca notas fiscais por nome do fornecedor.

        Args:
            termo_busca: Termo para buscar no nome do fornecedor

        Returns:
            Lista de notas fiscais encontradas
        """
        query = text("""
            SELECT
                id,
                razao_social_fornecedor,
                cnpj_fornecedor,
                numero_nota,
                data_emissao,
                valor_total,
                classificacao_despesa
            FROM nota_fiscal
            WHERE LOWER(razao_social_fornecedor) LIKE LOWER(:termo)
            ORDER BY data_emissao DESC
            LIMIT 20
        """)

        result = self.db.session.execute(query, {'termo': f'%{termo_busca}%'})
        rows = result.fetchall()

        return [
            {
                'id': row[0],
                'fornecedor': row[1],
                'cnpj': row[2],
                'numero_nota': row[3],
                'data_emissao': row[4].strftime('%d/%m/%Y') if row[4] else None,
                'valor_total': float(row[5]) if row[5] else 0,
                'classificacao': row[6]
            }
            for row in rows
        ]

    def get_resumo_financeiro(self) -> Dict[str, Any]:
        """
        Retorna um resumo geral do sistema financeiro.

        Returns:
            Dicionário com resumo financeiro completo
        """
        # Total de notas
        query_total_notas = text("SELECT COUNT(*) FROM nota_fiscal")
        total_notas = self.db.session.execute(query_total_notas).scalar()

        # Total geral
        query_total_geral = text("SELECT COALESCE(SUM(valor_total), 0) FROM nota_fiscal")
        total_geral = self.db.session.execute(query_total_geral).scalar()

        # Total últimos 30 dias
        data_30_dias = datetime.now() - timedelta(days=30)
        query_30_dias = text("""
            SELECT COALESCE(SUM(valor_total), 0)
            FROM nota_fiscal
            WHERE data_emissao >= :data_inicio
        """)
        total_30_dias = self.db.session.execute(
            query_30_dias,
            {'data_inicio': data_30_dias}
        ).scalar()

        # Quantidade de fornecedores únicos
        query_fornecedores = text("""
            SELECT COUNT(DISTINCT cnpj_fornecedor) FROM nota_fiscal
        """)
        total_fornecedores = self.db.session.execute(query_fornecedores).scalar()

        return {
            'total_notas_fiscais': total_notas,
            'valor_total_geral': float(total_geral) if total_geral else 0,
            'valor_ultimos_30_dias': float(total_30_dias) if total_30_dias else 0,
            'total_fornecedores_unicos': total_fornecedores
        }
