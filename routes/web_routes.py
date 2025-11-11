"""
Rotas web da aplicação para páginas HTML.
"""
import os
import json
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, current_app
from PyPDF2 import PdfReader
from datetime import datetime

from models import db
from models.nota_fiscal import NotaFiscal
from agents import ProcessadorDeNotaFiscalTool, AgenteProcessador

web_bp = Blueprint('web', __name__)


def extract_text_from_pdf(pdf_file_path):
    """Extrai o texto de um arquivo PDF local."""
    try:
        with open(pdf_file_path, 'rb') as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        raise Exception(f"Erro ao extrair texto do PDF: {e}")


def salvar_nota_fiscal_no_banco(resultado):
    """Salva os dados da nota fiscal no banco de dados."""
    try:
        # Converter string de data para objeto date
        data_emissao = None
        if resultado.get('Data Emissao'):
            data_emissao = datetime.strptime(resultado.get('Data Emissao', ''), '%Y-%m-%d').date()

        data_validade = None
        if resultado.get('Data de Validade'):
            data_validade = datetime.strptime(resultado.get('Data de Validade', ''), '%Y-%m-%d').date()

        # Criar nova nota fiscal
        from models.nota_fiscal import NotaFiscal, ProdutoNotaFiscal
        nova_nota = NotaFiscal(
            razao_social_fornecedor=resultado.get('Fornecedor', {}).get('Razao Social'),
            cnpj_fornecedor=resultado.get('Fornecedor', {}).get('CNPJ'),
            nome_faturado=resultado.get('Faturado', {}).get('Nome'),
            cpf_faturado=resultado.get('Faturado', {}).get('CPF'),
            numero_nota=resultado.get('Nota Fiscal'),
            data_emissao=data_emissao,
            data_validade=data_validade,
            valor_total=float(resultado.get('Valor Total', 0)),
            quantidade_parcelas=int(resultado.get('Quantidade de Parcelas', 0)),
            classificacao_despesa=resultado.get('Classificacao_Despesa')
        )

        db.session.add(nova_nota)
        db.session.flush()  # Para obter o ID da nota fiscal

        # Adicionar produtos
        for produto in resultado.get('Descricao Produtos', []):
            produto_nf = ProdutoNotaFiscal(
                nota_fiscal_id=nova_nota.id,
                descricao=produto
            )
            db.session.add(produto_nf)

        db.session.commit()
        print("Nota fiscal salva no banco de dados com sucesso!")
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao salvar no banco de dados: {e}")
        return False


@web_bp.route('/')
def index():
    """Página principal com formulário de upload."""
    return render_template('index.html', title="Upload Nota Fiscal")


@web_bp.route('/consultas')
def consultas():
    """Página de consultas ao banco de dados."""
    notas_fiscais = NotaFiscal.query.all()
    return render_template('consultas.html', title="Consultas / Banco de Dados", notas_fiscais=notas_fiscais)


@web_bp.route('/rag')
def rag_interface():
    """Página de interface RAG para perguntas inteligentes."""
    return render_template('rag.html', title="Consulta Inteligente - RAG")


@web_bp.route('/processar', methods=['POST'])
def processar():
    """Processa o PDF da nota fiscal e extrai os dados."""
    if 'file' not in request.files:
        return redirect(url_for('web.index'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('web.index'))

    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    try:
        invoice_text = extract_text_from_pdf(filepath)

        # Obter o modelo Gemini do app context
        import google.generativeai as genai
        model = genai.GenerativeModel(current_app.config.get('GEMINI_MODEL', 'gemini-2.0-flash'))

        processador_nf_tool = ProcessadorDeNotaFiscalTool(invoice_text, model)
        agente = AgenteProcessador({"processador_nf": processador_nf_tool})
        resultado = agente.executar_tarefa("Processar nota fiscal", invoice_text)

        if resultado:
            resultado_json_str = json.dumps(resultado, indent=2, ensure_ascii=False)

            salvar_nota_fiscal_no_banco(resultado)

            return render_template('resultado.html', title="Resultado",
                                  resultado=resultado, resultado_json=resultado_json_str)
        else:
            return jsonify({'status': 'error',
                           'message': 'O agente falhou ao processar a nota fiscal.'}), 500

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

    finally:
        if os.path.exists(filepath):
            os.remove(filepath)
