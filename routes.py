from flask import Blueprint, request, jsonify, render_template
from models.pessoas import Pessoas
from models.classificacao import Classificacao
from models.parcelas_contas import ParcelasContas
from models.movimento_contas import MovimentoContas
from models.nota_fiscal import NotaFiscal, ProdutoNotaFiscal
from datetime import datetime

bp = Blueprint('routes', __name__)

@bp.route('/api/validar', methods=['POST'])
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
    
    # Verificar tanto 'Classificacao Despesa' quanto 'Classificacao_Despesa'
    classificacao_despesa = data.get('Classificacao_Despesa')
    if not classificacao_despesa:
        classificacao_despesa = data.get('Classificacao Despesa')
    
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

@bp.route('/api/cadastrar/fornecedor', methods=['POST'])
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

@bp.route('/api/cadastrar/faturado', methods=['POST'])
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

@bp.route('/api/cadastrar/classificacao', methods=['POST'])
def cadastrar_classificacao():
    """
    Cadastra uma nova classificação de despesa
    """
    data = request.json
    
    classificacao = Classificacao.criar_nova(
        tipo='DESPESA',
        descricao=data.get('Classificacao Despesa')
    )
    
    return jsonify({
        'success': True,
        'id': classificacao.id
    })

@bp.route('/api/lancar', methods=['POST'])
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
        classificacao_despesa=data.get('Classificacao Despesa')
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