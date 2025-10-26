import os
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify
import google.generativeai as genai
from PyPDF2 import PdfReader
from datetime import datetime

# Configurações do Flask
app = Flask(__name__, 
           template_folder='projeto_admin_financeiro/templates',
           static_folder='projeto_admin_financeiro/static')
app.config['UPLOAD_FOLDER'] = 'uploads'

# Configuração do PostgreSQL
# Configuração do banco de dados para funcionar com banco de dados global
# Prioriza a variável de ambiente DATABASE_URL para conexão com banco de dados global
# Se não estiver definida, usa as configurações locais ou do Docker
database_url = os.environ.get('DATABASE_URL')

if database_url:
    # Usar a URL de banco de dados global fornecida
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Configuração para ambiente local ou Docker
    # Usando conexão SQLite para evitar problemas de codificação com PostgreSQL
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///admin_financeiro.db"
app.config['SQLALCHEMY_ECHO'] = True  # Ativa logs SQL para debug
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Importação dos modelos
from models import db, init_db
from models.pessoas import Pessoas
from models.classificacao import Classificacao
from models.parcelas_contas import ParcelasContas
from models.movimento_contas import MovimentoContas, movimento_classificacao
from models.nota_fiscal import NotaFiscal, ProdutoNotaFiscal

# Inicialização do banco de dados
init_db(app)

# Importação e registro das rotas
from routes import bp
app.register_blueprint(bp)

# Adicionar rotas para API de validação e cadastro
@app.route('/api/validar', methods=['POST'])
def validar_dados():
    from routes import validar_dados as route_validar_dados
    return route_validar_dados()

@app.route('/api/cadastrar/fornecedor', methods=['POST'])
def cadastrar_fornecedor():
    from routes import cadastrar_fornecedor as route_cadastrar_fornecedor
    return route_cadastrar_fornecedor()

@app.route('/api/cadastrar/faturado', methods=['POST'])
def cadastrar_faturado():
    from routes import cadastrar_faturado as route_cadastrar_faturado
    return route_cadastrar_faturado()

@app.route('/api/cadastrar/classificacao', methods=['POST'])
def cadastrar_classificacao():
    from routes import cadastrar_classificacao as route_cadastrar_classificacao
    return route_cadastrar_classificacao()

@app.route('/api/lancar', methods=['POST'])
def lancar_nota_fiscal():
    from routes import lancar_nota_fiscal as route_lancar_nota_fiscal
    return route_lancar_nota_fiscal()

# --- Definição das Ferramentas e Agente ---

# Configure sua chave da API do Gemini.
genai.configure(api_key="AIzaSyC20cwc-Evxal4LLJo5lsiHpCnT_13VeIg")
model = genai.GenerativeModel('gemini-2.0-flash')

class ProcessadorDeNotaFiscalTool:
    """Uma ferramenta para extrair dados de notas fiscais usando a API do Gemini."""
    def __init__(self, invoice_text):
        self.invoice_text = invoice_text

    def executar(self):
        """
        Chama a API do Gemini com um prompt para extrair os dados da nota fiscal.
        Retorna o dicionário JSON extraído ou None em caso de erro.
        """
        prompt_text = f"""
Extraia os seguintes dados do texto da nota fiscal fornecido.

A saída deve ser um **objeto JSON único e bem formatado**, sem qualquer texto adicional antes ou depois.

A estrutura do JSON deve seguir o seguinte modelo. Para valores decimais, use ponto (.) como separador, não vírgula (,).

Abaixo está a estrutura do JSON, lembre-se que em 'Descricao Produtos' considere somente a descrição do produto sem considerar o codigo do produto.

{{
  "Fornecedor": {{
    "Razao Social": "...",
    "CNPJ": "..."
  }},
  "Faturado": {{
    "Nome": "...",
    "CPF": "..."
  }},
  "Nota Fiscal": "...",
  "Data Emissao": "AAAA-MM-DD",
  "Data de Validade": "AAAA-MM-DD",
  "Descricao Produtos": [
    "Produto",
    "Produto"
  ],
  "Valor Total": 0.0,
  "Quantidade de Parcelas": 0,
  "Classificacao_Despesa": "..."
}}

IMPORTANTE: Use "Classificacao_Despesa" (com underscore) como chave no JSON, não use "Classificacao Despesa".

Categorias para Classificacao_Despesa:
- INSUMOS_AGRICOLAS
- MANUTENCAO_E_OPERACAO
- RECURSOS_HUMANOS
- SERVICOS_OPERACIONAIS
- INFRASTRUTURA_E_UTILIDADES
- ADMINISTRATIVAS
- SEGUROS_E_PROTECAO
- IMPOSTOS_E_TAXAS
- INVESTIMENTOS
- OUTROS

Classifique a despesa de acordo com os produtos na nota fiscal:
- Para itens como 'Sementes', 'Fertilizantes', 'Defensivos Agrícolas', 'Corretivos', classifique como **INSUMOS_AGRICOLAS**.
- Para itens como 'Combustíveis', 'Lubrificantes', 'Peças', 'Parafusos', 'Manutenção de Máquinas', 'Pneus', 'Filtros', 'Correias', 'Ferramentas', 'Utensílios', classifique como **MANUTENCAO_E_OPERACAO**.
- Para itens como 'Mão de Obra Temporária', 'Salários', 'Encargos', classifique como **RECURSOS_HUMANOS**.
- Para itens como 'Frete', 'Transporte', 'Colheita Terceirizada', 'Secagem', 'Armazenagem', 'Pulverização', 'Aplicação', classifique como **SERVICOS_OPERACIONAIS**.
- Para itens como 'Energia Elétrica', 'Arrendamento de Terras', 'Construções', 'Reformas', 'Materiais de Construção', classifique como **INFRASTRUTURA_E_UTILIDADES**.
- Para itens como 'Honorários Contábeis', 'Honorários Advocatícios', 'Despesas Bancárias', 'Despesas Financeiras', classifique como **ADMINISTRATIVAS**.
- Para itens como 'Seguro Agrícola', 'Seguro de Ativos', 'Seguro de Veículos', 'Seguro Prestamista', classifique como **SEGUROS_E_PROTECAO**.
- Para itens como 'ITR', 'IPTU', 'IPVA', 'INCRA-CCIR', 'Impostos', 'Taxas', classifique como **IMPOSTOS_E_TAXAS**.
- Para itens como 'Aquisição de Máquinas', 'Implementos', 'Veículos', 'Imóveis', 'Infraestrutura Rural', classifique como **INVESTIMENTOS**.
- Para todos os outros itens que não se encaixem nas categorias acima, classifique como **OUTROS**.

Texto da nota fiscal:
{self.invoice_text}
"""
        try:
            response = model.generate_content(prompt_text)
            response_text = response.text.strip().replace("```json\n", "").replace("\n```", "").strip()
            return json.loads(response_text)
        except (json.JSONDecodeError, Exception) as e:
            print(f"Erro na ferramenta: {e}")
            return None

class AgenteProcessador:
    """Um agente que decide qual ferramenta usar para a tarefa."""
    def __init__(self, ferramentas):
        self.ferramentas = ferramentas

    def executar_tarefa(self, tarefa, dados):
        """
        O agente decide qual ferramenta usar para a tarefa.
        Para este exemplo, a decisão é baseada na string da tarefa.
        """
        if "processar nota fiscal" in tarefa.lower():
            ferramenta = self.ferramentas.get("processador_nf")
            if ferramenta:
                # O agente executa a ferramenta com os dados fornecidos
                return ferramenta.executar()
        return None

# --- Funções Auxiliares e Rotas do Flask ---

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

@app.route('/')
def index():
    return render_template('index.html', title="Upload Nota Fiscal")

@app.route('/consultas')
def consultas():
    # Buscar todas as notas fiscais do banco de dados
    notas_fiscais = NotaFiscal.query.all()
    return render_template('consultas.html', title="Consultas / Banco de Dados", notas_fiscais=notas_fiscais)

@app.route('/processar', methods=['POST'])
def processar():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    try:
        invoice_text = extract_text_from_pdf(filepath)
        
        # O agente é instanciado e a ferramenta é fornecida a ele
        processador_nf_tool = ProcessadorDeNotaFiscalTool(invoice_text)
        agente = AgenteProcessador({"processador_nf": processador_nf_tool})

        # O agente recebe a tarefa e a executa
        resultado = agente.executar_tarefa("Processar nota fiscal", invoice_text)

        if resultado:
            # Converte o dicionário em uma string JSON formatada para exibição
            # NO TERMINAL e para ser passado para o template.
            resultado_json_str = json.dumps(resultado, indent=2, ensure_ascii=False)
            print("\n--- JSON Formatado ---")
            print(resultado_json_str)
            print("------------------------")
            
            # Salvar no banco de dados
            try:
                # Converter string de data para objeto date
                data_emissao = datetime.strptime(resultado.get('Data Emissao', ''), '%Y-%m-%d').date() if resultado.get('Data Emissao') else None
                data_validade = datetime.strptime(resultado.get('Data de Validade', ''), '%Y-%m-%d').date() if resultado.get('Data de Validade') else None
                
                # Criar nova nota fiscal
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
                    classificacao_despesa=resultado.get('Classificacao Despesa')
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
                
            except Exception as e:
                db.session.rollback()
                print(f"Erro ao salvar no banco de dados: {e}")
            
            # Retorna o resultado para o template 'resultado.html', incluindo
            # a string JSON para a aba 'JSON'
            return render_template('resultado.html', title="Resultado", resultado=resultado, resultado_json=resultado_json_str)
        else:
            return jsonify({'status': 'error', 'message': 'O agente falhou ao processar a nota fiscal.'}), 500

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

if __name__ == "__main__":

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Criar tabelas no banco de dados
    with app.app_context():
        db.create_all()
        
    app.run(host='0.0.0.0', debug=True)
