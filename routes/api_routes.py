"""
Rotas da API REST para validação e cadastro de dados.
"""
from flask import Blueprint, request, jsonify
from models.pessoas import Pessoas
from models.classificacao import Classificacao
from models.parcelas_contas import ParcelasContas
from models.movimento_contas import MovimentoContas
from models.nota_fiscal import NotaFiscal, ProdutoNotaFiscal
from datetime import datetime
from models import db
from rag_system import RAGSimple, RAGEmbeddings

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Inicializar o sistema RAG (será configurado depois da inicialização do app)
rag_simple = None
rag_embeddings = None


def init_rag_system(database):
    """Inicializa o sistema RAG com a instância do banco de dados."""
    global rag_simple, rag_embeddings
    rag_simple = RAGSimple(database)

    # Inicializa RAG com embeddings (pode demorar devido ao carregamento do modelo)
    try:
        print("Inicializando RAG com Embeddings...")
        rag_embeddings = RAGEmbeddings(database)
        print("RAG com Embeddings inicializado com sucesso!")
    except Exception as e:
        print(f"Erro ao inicializar RAG com Embeddings: {e}")
        rag_embeddings = None


@api_bp.route('/validar', methods=['POST'])
def validar_dados():
    """
    Verifica se fornecedor, faturado e classificação de despesa existem no banco de dados
    Adaptado para funcionar com a interface existente
    """
    data = request.json
    print("Dados recebidos para validação:", data)  # Log para debug

    # Verificar fornecedor
    fornecedor_info = {
        'existe': False,
        'id': None
    }

    # Adaptar para o formato da interface existente
    cnpj_fornecedor = data.get('Fornecedor', {}).get('CNPJ')
    print(f"CNPJ Fornecedor: {cnpj_fornecedor}")  # Log para debug
    if cnpj_fornecedor:
        # Tenta com ambos os tipos possíveis
        fornecedor = Pessoas.verificar_existencia(tipo='CLIENTE-FORNECEDOR', cpf_cnpj=cnpj_fornecedor)
        if not fornecedor:
            fornecedor = Pessoas.verificar_existencia(tipo='FORNECEDOR', cpf_cnpj=cnpj_fornecedor)
        if not fornecedor:
            fornecedor = Pessoas.verificar_existencia(cpf_cnpj=cnpj_fornecedor)  # Tenta sem filtro de tipo

        if fornecedor:
            fornecedor_info['existe'] = True
            fornecedor_info['id'] = fornecedor.id
            print(f"Fornecedor encontrado: {fornecedor.id}")  # Log para debug
        else:
            print("Fornecedor não encontrado no banco")  # Log para debug

    # Verificar faturado
    faturado_info = {
        'existe': False,
        'id': None
    }

    cpf_faturado = data.get('Faturado', {}).get('CPF')
    print(f"CPF Faturado: {cpf_faturado}")  # Log para debug
    if cpf_faturado:
        faturado = Pessoas.verificar_existencia(tipo='FATURADO', cpf_cnpj=cpf_faturado)
        if not faturado:
            faturado = Pessoas.verificar_existencia(cpf_cnpj=cpf_faturado)  # Tenta sem filtro de tipo

        if faturado:
            faturado_info['existe'] = True
            faturado_info['id'] = faturado.id
            print(f"Faturado encontrado: {faturado.id}")  # Log para debug
        else:
            print("Faturado não encontrado no banco")  # Log para debug

    # Verificar classificação de despesa
    despesa_info = {
        'existe': False,
        'id': None
    }

    classificacao_despesa = data.get('Classificacao_Despesa')

    print(f"Classificação Despesa: {classificacao_despesa}")  # Log para debug
    if classificacao_despesa:
        despesa = Classificacao.verificar_existencia('DESPESA', classificacao_despesa)
        if despesa:
            despesa_info['existe'] = True
            despesa_info['id'] = despesa.id
            print(f"Despesa encontrada: {despesa.id}")  # Log para debug
        else:
            print("Classificação de despesa não encontrada no banco")  # Log para debug

    return jsonify({
        'fornecedor': fornecedor_info,
        'faturado': faturado_info,
        'classificacao': despesa_info
    })


@api_bp.route('/cadastrar/fornecedor', methods=['POST'])
def cadastrar_fornecedor():
    """
    Cadastra um novo fornecedor
    """
    data = request.json

    fornecedor = Pessoas.criar_novo(
        tipo='CLIENTE-FORNECEDOR',
        razao_social=data.get('Fornecedor', {}).get('Razao Social'),
        cpf_cnpj=data.get('Fornecedor', {}).get('CNPJ')
    )

    return jsonify({
        'success': True,
        'id': fornecedor.id
    })


@api_bp.route('/cadastrar/faturado', methods=['POST'])
def cadastrar_faturado():
    """
    Cadastra um novo faturado
    """
    data = request.json

    faturado = Pessoas.criar_novo(
        tipo='FATURADO',
        razao_social=data.get('Faturado', {}).get('Nome'),
        cpf_cnpj=data.get('Faturado', {}).get('CPF')
    )

    return jsonify({
        'success': True,
        'id': faturado.id
    })


@api_bp.route('/cadastrar/classificacao', methods=['POST'])
def cadastrar_classificacao():
    """
    Cadastra uma nova classificação de despesa
    """
    data = request.json

    classificacao = Classificacao.criar_nova(
        tipo='DESPESA',
        descricao=data.get('Classificacao_Despesa')
    )

    return jsonify({
        'success': True,
        'id': classificacao.id
    })


@api_bp.route('/lancar', methods=['POST'])
def lancar_nota_fiscal():
    """
    Processa os dados da nota fiscal, criando registros necessários no banco de dados
    Adaptado para funcionar com a interface existente
    """
    data = request.json

    # Obter IDs dos registros
    fornecedor_id = data.get('fornecedor_id')
    faturado_id = data.get('faturado_id')
    classificacao_id = data.get('classificacao_id')

    # Criar parcela
    identificacao = f"NF-{data.get('Nota Fiscal')}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    parcela = ParcelasContas.criar_nova(
        identificacao=identificacao,
        numero_nota=data.get('Nota Fiscal'),
        data_emissao=datetime.strptime(data.get('Data Emissao'), '%d/%m/%Y').date() if '/' in data.get('Data Emissao', '') else datetime.strptime(data.get('Data Emissao'), '%Y-%m-%d').date(),
        data_vencimento=datetime.now().date(),  # Data de vencimento não está disponível na interface
        valor_total=float(data.get('Valor Total'))
    )

    # Obter objetos a partir dos IDs
    from models import db
    fornecedor = Pessoas.query.get(fornecedor_id)
    faturado = Pessoas.query.get(faturado_id)
    classificacao = Classificacao.query.get(classificacao_id)

    # Criar movimento
    movimento = MovimentoContas.criar_novo(
        tipo='APAGAR',
        parcela_id=parcela.id,
        fornecedor_cliente_id=fornecedor.id,
        faturado_id=faturado.id,
        valor=float(data.get('Valor Total')),
        classificacoes=[classificacao]
    )

    # Criar nota fiscal
    nota_fiscal = NotaFiscal(
        razao_social_fornecedor=data.get('Fornecedor', {}).get('Razao Social'),
        cnpj_fornecedor=data.get('Fornecedor', {}).get('CNPJ'),
        nome_faturado=data.get('Faturado', {}).get('Nome'),
        cpf_faturado=data.get('Faturado', {}).get('CPF'),
        numero_nota=data.get('Nota Fiscal'),
        data_emissao=datetime.strptime(data.get('Data Emissao'), '%d/%m/%Y').date() if '/' in data.get('Data Emissao', '') else datetime.strptime(data.get('Data Emissao'), '%Y-%m-%d').date(),
        data_validade=datetime.now().date(),  # Data de validade não está disponível na interface
        valor_total=float(data.get('Valor Total')),
        quantidade_parcelas=1,
        classificacao_despesa=data.get('Classificacao_Despesa')
    )

    db.session.add(nota_fiscal)
    db.session.commit()

    # Adicionar produtos se houver
    if 'Descricao Produtos' in data and data['Descricao Produtos']:
        for produto_desc in data['Descricao Produtos']:
            produto = ProdutoNotaFiscal(
                nota_fiscal_id=nota_fiscal.id,
                descricao=produto_desc
            )
            db.session.add(produto)
        db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Nota fiscal processada com sucesso!',
        'nota_fiscal_id': nota_fiscal.id,
        'movimento_id': movimento.id
    })


# ==================== ROTAS DO SISTEMA RAG ====================

@api_bp.route('/rag/ask', methods=['POST'])
def rag_ask_question():
    """
    Endpoint para fazer perguntas ao sistema RAG.

    Recebe uma pergunta em JSON e retorna uma resposta elaborada.
    Suporta dois métodos: RAG_SIMPLE e RAG_EMBEDDINGS
    """
    try:
        data = request.json
        question = data.get('question', '').strip()
        method = data.get('method', 'simple').lower()  # 'simple' ou 'embeddings'

        if not question:
            return jsonify({
                'success': False,
                'error': 'Pergunta não pode estar vazia'
            }), 400

        # Por enquanto, apenas RAG Simple está implementado
        if method == 'simple':
            if rag_simple is None:
                return jsonify({
                    'success': False,
                    'error': 'Sistema RAG não inicializado'
                }), 500

            result = rag_simple.answer_question(question)
            return jsonify(result)

        elif method == 'embeddings':
            if rag_embeddings is None:
                return jsonify({
                    'success': False,
                    'error': 'RAG com embeddings não inicializado. Verifique os logs do servidor.'
                }), 500

            result = rag_embeddings.answer_question(question)
            return jsonify(result)

        else:
            return jsonify({
                'success': False,
                'error': 'Método inválido. Use "simple" ou "embeddings"'
            }), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao processar pergunta: {str(e)}'
        }), 500


@api_bp.route('/rag/examples', methods=['GET'])
def rag_get_examples():
    """
    Retorna exemplos de perguntas que o sistema RAG pode responder.
    """
    try:
        if rag_simple is None:
            return jsonify({
                'success': False,
                'error': 'Sistema RAG não inicializado'
            }), 500

        examples = rag_simple.get_available_queries()

        return jsonify({
            'success': True,
            'examples': examples,
            'methods': ['simple', 'embeddings']
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao obter exemplos: {str(e)}'
        }), 500


@api_bp.route('/rag/status', methods=['GET'])
def rag_get_status():
    """
    Retorna o status do sistema RAG.
    """
    status = {
        'success': True,
        'rag_simple_initialized': rag_simple is not None,
        'rag_embeddings_initialized': rag_embeddings is not None,
        'available_methods': []
    }

    if rag_simple is not None:
        status['available_methods'].append('simple')

    if rag_embeddings is not None:
        status['available_methods'].append('embeddings')
        # Adiciona status da indexação
        index_status = rag_embeddings.get_index_status()
        status['index_status'] = index_status

    return jsonify(status)


@api_bp.route('/rag/index', methods=['POST'])
def rag_index_documents():
    """
    Indexa todos os documentos (notas fiscais) para busca semântica.
    """
    try:
        if rag_embeddings is None:
            return jsonify({
                'success': False,
                'error': 'RAG com embeddings não inicializado'
            }), 500

        result = rag_embeddings.index_all_notas_fiscais()
        return jsonify(result)

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao indexar documentos: {str(e)}'
        }), 500


@api_bp.route('/rag/index/<int:nota_id>', methods=['POST'])
def rag_index_nota(nota_id):
    """
    Indexa uma nota fiscal específica.
    """
    try:
        if rag_embeddings is None:
            return jsonify({
                'success': False,
                'error': 'RAG com embeddings não inicializado'
            }), 500

        success = rag_embeddings.index_nota_fiscal(nota_id)

        if success:
            return jsonify({
                'success': True,
                'message': f'Nota fiscal {nota_id} indexada com sucesso'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Erro ao indexar nota fiscal {nota_id}'
            }), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao indexar nota fiscal: {str(e)}'
        }), 500
