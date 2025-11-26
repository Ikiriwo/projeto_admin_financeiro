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


# ==================== ROTAS CRUD PARA PESSOAS ====================

@api_bp.route('/pessoas', methods=['GET'])
def listar_pessoas():
    """
    Lista todas as pessoas (filtro opcional por tipo).
    Query params: tipo (FORNECEDOR, CLIENTE, FATURADO), incluir_inativos (true/false)
    """
    try:
        tipo = request.args.get('tipo')
        incluir_inativos = request.args.get('incluir_inativos', 'false').lower() == 'true'

        pessoas = Pessoas.listar_todos(tipo=tipo, incluir_inativos=incluir_inativos)

        return jsonify({
            'success': True,
            'data': [{
                'id': p.id,
                'tipo': p.tipo,
                'razao_social': p.razao_social,
                'cpf_cnpj': p.cpf_cnpj,
                'status': p.status,
                'data_cadastro': p.data_cadastro.isoformat() if p.data_cadastro else None
            } for p in pessoas]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao listar pessoas: {str(e)}'
        }), 500


@api_bp.route('/pessoas/<int:pessoa_id>', methods=['GET'])
def obter_pessoa(pessoa_id):
    """
    Obtém uma pessoa específica por ID.
    """
    try:
        pessoa = Pessoas.query.get(pessoa_id)
        if not pessoa:
            return jsonify({
                'success': False,
                'error': 'Pessoa não encontrada'
            }), 404

        return jsonify({
            'success': True,
            'data': {
                'id': pessoa.id,
                'tipo': pessoa.tipo,
                'razao_social': pessoa.razao_social,
                'cpf_cnpj': pessoa.cpf_cnpj,
                'status': pessoa.status,
                'data_cadastro': pessoa.data_cadastro.isoformat() if pessoa.data_cadastro else None
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao obter pessoa: {str(e)}'
        }), 500


@api_bp.route('/pessoas', methods=['POST'])
def criar_pessoa():
    """
    Cria uma nova pessoa.
    Body: { tipo, razao_social, cpf_cnpj }
    """
    try:
        data = request.json

        # Validar campos obrigatórios
        if not data.get('tipo') or not data.get('razao_social') or not data.get('cpf_cnpj'):
            return jsonify({
                'success': False,
                'error': 'Campos obrigatórios: tipo, razao_social, cpf_cnpj'
            }), 400

        # Verificar se já existe
        existe = Pessoas.verificar_existencia(cpf_cnpj=data['cpf_cnpj'], incluir_inativos=True)
        if existe:
            return jsonify({
                'success': False,
                'error': 'Pessoa já cadastrada com este CPF/CNPJ'
            }), 400

        pessoa = Pessoas.criar_novo(
            tipo=data['tipo'],
            razao_social=data['razao_social'],
            cpf_cnpj=data['cpf_cnpj']
        )

        return jsonify({
            'success': True,
            'message': 'Pessoa criada com sucesso',
            'data': {
                'id': pessoa.id,
                'tipo': pessoa.tipo,
                'razao_social': pessoa.razao_social,
                'cpf_cnpj': pessoa.cpf_cnpj,
                'status': pessoa.status
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Erro ao criar pessoa: {str(e)}'
        }), 500


@api_bp.route('/pessoas/<int:pessoa_id>', methods=['PUT'])
def atualizar_pessoa(pessoa_id):
    """
    Atualiza uma pessoa existente.
    Body: { tipo, razao_social, cpf_cnpj } (campos opcionais)
    """
    try:
        pessoa = Pessoas.query.get(pessoa_id)
        if not pessoa:
            return jsonify({
                'success': False,
                'error': 'Pessoa não encontrada'
            }), 404

        data = request.json
        campos_atualizaveis = {}

        if 'tipo' in data:
            campos_atualizaveis['tipo'] = data['tipo']
        if 'razao_social' in data:
            campos_atualizaveis['razao_social'] = data['razao_social']
        if 'cpf_cnpj' in data:
            # Verificar se o novo CPF/CNPJ já existe em outra pessoa
            existe = Pessoas.query.filter(
                Pessoas.cpf_cnpj == data['cpf_cnpj'],
                Pessoas.id != pessoa_id
            ).first()
            if existe:
                return jsonify({
                    'success': False,
                    'error': 'CPF/CNPJ já cadastrado para outra pessoa'
                }), 400
            campos_atualizaveis['cpf_cnpj'] = data['cpf_cnpj']

        pessoa.atualizar(**campos_atualizaveis)

        return jsonify({
            'success': True,
            'message': 'Pessoa atualizada com sucesso',
            'data': {
                'id': pessoa.id,
                'tipo': pessoa.tipo,
                'razao_social': pessoa.razao_social,
                'cpf_cnpj': pessoa.cpf_cnpj,
                'status': pessoa.status
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Erro ao atualizar pessoa: {str(e)}'
        }), 500


@api_bp.route('/pessoas/<int:pessoa_id>', methods=['DELETE'])
def excluir_pessoa(pessoa_id):
    """
    Realiza exclusão lógica de uma pessoa (altera status para INATIVO).
    """
    try:
        pessoa = Pessoas.query.get(pessoa_id)
        if not pessoa:
            return jsonify({
                'success': False,
                'error': 'Pessoa não encontrada'
            }), 404

        pessoa.excluir_logico()

        return jsonify({
            'success': True,
            'message': 'Pessoa excluída com sucesso (exclusão lógica)'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Erro ao excluir pessoa: {str(e)}'
        }), 500


# ==================== ROTAS CRUD PARA CLASSIFICAÇÕES ====================

@api_bp.route('/classificacoes', methods=['GET'])
def listar_classificacoes():
    """
    Lista todas as classificações (filtro opcional por tipo).
    Query params: tipo (RECEITA, DESPESA), incluir_inativos (true/false)
    """
    try:
        tipo = request.args.get('tipo')
        incluir_inativos = request.args.get('incluir_inativos', 'false').lower() == 'true'

        classificacoes = Classificacao.listar_todos(tipo=tipo, incluir_inativos=incluir_inativos)

        return jsonify({
            'success': True,
            'data': [{
                'id': c.id,
                'tipo': c.tipo,
                'descricao': c.descricao,
                'status': c.status,
                'data_cadastro': c.data_cadastro.isoformat() if c.data_cadastro else None
            } for c in classificacoes]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao listar classificações: {str(e)}'
        }), 500


@api_bp.route('/classificacoes/<int:classificacao_id>', methods=['GET'])
def obter_classificacao(classificacao_id):
    """
    Obtém uma classificação específica por ID.
    """
    try:
        classificacao = Classificacao.query.get(classificacao_id)
        if not classificacao:
            return jsonify({
                'success': False,
                'error': 'Classificação não encontrada'
            }), 404

        return jsonify({
            'success': True,
            'data': {
                'id': classificacao.id,
                'tipo': classificacao.tipo,
                'descricao': classificacao.descricao,
                'status': classificacao.status,
                'data_cadastro': classificacao.data_cadastro.isoformat() if classificacao.data_cadastro else None
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao obter classificação: {str(e)}'
        }), 500


@api_bp.route('/classificacoes', methods=['POST'])
def criar_classificacao():
    """
    Cria uma nova classificação.
    Body: { tipo, descricao }
    """
    try:
        data = request.json

        # Validar campos obrigatórios
        if not data.get('tipo') or not data.get('descricao'):
            return jsonify({
                'success': False,
                'error': 'Campos obrigatórios: tipo, descricao'
            }), 400

        # Verificar se já existe
        existe = Classificacao.verificar_existencia(
            tipo=data['tipo'],
            descricao=data['descricao'],
            incluir_inativos=True
        )
        if existe:
            return jsonify({
                'success': False,
                'error': 'Classificação já cadastrada com este tipo e descrição'
            }), 400

        classificacao = Classificacao.criar_nova(
            tipo=data['tipo'],
            descricao=data['descricao']
        )

        return jsonify({
            'success': True,
            'message': 'Classificação criada com sucesso',
            'data': {
                'id': classificacao.id,
                'tipo': classificacao.tipo,
                'descricao': classificacao.descricao,
                'status': classificacao.status
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Erro ao criar classificação: {str(e)}'
        }), 500


@api_bp.route('/classificacoes/<int:classificacao_id>', methods=['PUT'])
def atualizar_classificacao(classificacao_id):
    """
    Atualiza uma classificação existente.
    Body: { tipo, descricao } (campos opcionais)
    """
    try:
        classificacao = Classificacao.query.get(classificacao_id)
        if not classificacao:
            return jsonify({
                'success': False,
                'error': 'Classificação não encontrada'
            }), 404

        data = request.json
        campos_atualizaveis = {}

        if 'tipo' in data:
            campos_atualizaveis['tipo'] = data['tipo']
        if 'descricao' in data:
            campos_atualizaveis['descricao'] = data['descricao']

        # Verificar duplicação se tipo ou descrição foram alterados
        if 'tipo' in data or 'descricao' in data:
            novo_tipo = data.get('tipo', classificacao.tipo)
            nova_descricao = data.get('descricao', classificacao.descricao)

            existe = Classificacao.query.filter(
                Classificacao.tipo == novo_tipo,
                Classificacao.descricao == nova_descricao,
                Classificacao.id != classificacao_id
            ).first()
            if existe:
                return jsonify({
                    'success': False,
                    'error': 'Já existe uma classificação com este tipo e descrição'
                }), 400

        classificacao.atualizar(**campos_atualizaveis)

        return jsonify({
            'success': True,
            'message': 'Classificação atualizada com sucesso',
            'data': {
                'id': classificacao.id,
                'tipo': classificacao.tipo,
                'descricao': classificacao.descricao,
                'status': classificacao.status
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Erro ao atualizar classificação: {str(e)}'
        }), 500


@api_bp.route('/classificacoes/<int:classificacao_id>', methods=['DELETE'])
def excluir_classificacao(classificacao_id):
    """
    Realiza exclusão lógica de uma classificação (altera status para INATIVO).
    """
    try:
        classificacao = Classificacao.query.get(classificacao_id)
        if not classificacao:
            return jsonify({
                'success': False,
                'error': 'Classificação não encontrada'
            }), 404

        classificacao.excluir_logico()

        return jsonify({
            'success': True,
            'message': 'Classificação excluída com sucesso (exclusão lógica)'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Erro ao excluir classificação: {str(e)}'
        }), 500


# ==================== ROTAS CRUD PARA MOVIMENTO CONTAS ====================

@api_bp.route('/movimentos', methods=['GET'])
def listar_movimentos():
    """
    Lista todos os movimentos contábeis (filtro opcional por tipo).
    Query params: tipo (APAGAR, ARECEBER), incluir_inativos (true/false)
    """
    try:
        tipo = request.args.get('tipo')
        incluir_inativos = request.args.get('incluir_inativos', 'false').lower() == 'true'

        movimentos = MovimentoContas.listar_todos(tipo=tipo, incluir_inativos=incluir_inativos)

        return jsonify({
            'success': True,
            'data': [{
                'id': m.id,
                'tipo': m.tipo,
                'parcela_id': m.parcela_id,
                'fornecedor_cliente_id': m.fornecedor_cliente_id,
                'fornecedor_cliente_nome': m.fornecedor_cliente.razao_social if m.fornecedor_cliente else None,
                'faturado_id': m.faturado_id,
                'faturado_nome': m.faturado.razao_social if m.faturado else None,
                'valor': m.valor,
                'status': m.status,
                'data_movimento': m.data_movimento.isoformat() if m.data_movimento else None,
                'classificacoes': [{'id': c.id, 'descricao': c.descricao, 'tipo': c.tipo} for c in m.classificacoes]
            } for m in movimentos]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao listar movimentos: {str(e)}'
        }), 500


@api_bp.route('/movimentos/<int:movimento_id>', methods=['GET'])
def obter_movimento(movimento_id):
    """
    Obtém um movimento específico por ID.
    """
    try:
        movimento = MovimentoContas.query.get(movimento_id)
        if not movimento:
            return jsonify({
                'success': False,
                'error': 'Movimento não encontrado'
            }), 404

        return jsonify({
            'success': True,
            'data': {
                'id': movimento.id,
                'tipo': movimento.tipo,
                'parcela_id': movimento.parcela_id,
                'fornecedor_cliente_id': movimento.fornecedor_cliente_id,
                'fornecedor_cliente_nome': movimento.fornecedor_cliente.razao_social if movimento.fornecedor_cliente else None,
                'faturado_id': movimento.faturado_id,
                'faturado_nome': movimento.faturado.razao_social if movimento.faturado else None,
                'valor': movimento.valor,
                'status': movimento.status,
                'data_movimento': movimento.data_movimento.isoformat() if movimento.data_movimento else None,
                'classificacoes': [{'id': c.id, 'descricao': c.descricao, 'tipo': c.tipo} for c in movimento.classificacoes]
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao obter movimento: {str(e)}'
        }), 500


@api_bp.route('/movimentos', methods=['POST'])
def criar_movimento():
    """
    Cria um novo movimento contábil.
    Body: { tipo, parcela_id, fornecedor_cliente_id, faturado_id, valor, classificacao_ids[] }
    """
    try:
        data = request.json

        # Validar campos obrigatórios
        required_fields = ['tipo', 'fornecedor_cliente_id', 'faturado_id', 'valor']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Campo obrigatório ausente: {field}'
                }), 400

        # Obter classificações se fornecidas
        classificacoes = []
        if 'classificacao_ids' in data and data['classificacao_ids']:
            classificacoes = Classificacao.query.filter(
                Classificacao.id.in_(data['classificacao_ids'])
            ).all()

        movimento = MovimentoContas.criar_novo(
            tipo=data['tipo'],
            parcela_id=data.get('parcela_id'),
            fornecedor_cliente_id=data['fornecedor_cliente_id'],
            faturado_id=data['faturado_id'],
            valor=float(data['valor']),
            classificacoes=classificacoes
        )

        return jsonify({
            'success': True,
            'message': 'Movimento criado com sucesso',
            'data': {
                'id': movimento.id,
                'tipo': movimento.tipo,
                'valor': movimento.valor,
                'status': movimento.status
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Erro ao criar movimento: {str(e)}'
        }), 500


@api_bp.route('/movimentos/<int:movimento_id>', methods=['PUT'])
def atualizar_movimento(movimento_id):
    """
    Atualiza um movimento existente.
    Body: { tipo, fornecedor_cliente_id, faturado_id, valor, classificacao_ids[] } (campos opcionais)
    """
    try:
        movimento = MovimentoContas.query.get(movimento_id)
        if not movimento:
            return jsonify({
                'success': False,
                'error': 'Movimento não encontrado'
            }), 404

        data = request.json
        campos_atualizaveis = {}

        if 'tipo' in data:
            campos_atualizaveis['tipo'] = data['tipo']
        if 'fornecedor_cliente_id' in data:
            campos_atualizaveis['fornecedor_cliente_id'] = data['fornecedor_cliente_id']
        if 'faturado_id' in data:
            campos_atualizaveis['faturado_id'] = data['faturado_id']
        if 'valor' in data:
            campos_atualizaveis['valor'] = float(data['valor'])
        if 'classificacao_ids' in data:
            classificacoes = Classificacao.query.filter(
                Classificacao.id.in_(data['classificacao_ids'])
            ).all()
            campos_atualizaveis['classificacoes'] = classificacoes

        movimento.atualizar(**campos_atualizaveis)

        return jsonify({
            'success': True,
            'message': 'Movimento atualizado com sucesso',
            'data': {
                'id': movimento.id,
                'tipo': movimento.tipo,
                'valor': movimento.valor,
                'status': movimento.status
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Erro ao atualizar movimento: {str(e)}'
        }), 500


@api_bp.route('/movimentos/<int:movimento_id>', methods=['DELETE'])
def excluir_movimento(movimento_id):
    """
    Realiza exclusão lógica de um movimento (altera status para INATIVO).
    """
    try:
        movimento = MovimentoContas.query.get(movimento_id)
        if not movimento:
            return jsonify({
                'success': False,
                'error': 'Movimento não encontrado'
            }), 404

        movimento.excluir_logico()

        return jsonify({
            'success': True,
            'message': 'Movimento excluído com sucesso (exclusão lógica)'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Erro ao excluir movimento: {str(e)}'
        }), 500
