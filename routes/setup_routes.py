"""
Rotas para configuração inicial do sistema.
Solicita e valida a chave API do Google Gemini via interface web.
"""
from flask import Blueprint, render_template, request, jsonify
import google.generativeai as genai
import os
from pathlib import Path
from dotenv import set_key

setup_bp = Blueprint('setup', __name__, url_prefix='/setup')

ENV_FILE = Path(__file__).parent.parent / '.env'


def test_gemini_key(api_key):
    """
    Testa se a chave API do Gemini é válida fazendo uma requisição real.
    Retorna (True, mensagem_sucesso) ou (False, mensagem_erro)
    """
    try:
        # Configurar API temporariamente
        genai.configure(api_key=api_key)

        # Tentar criar um modelo e fazer uma requisição simples
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content("Diga apenas 'OK' se você está funcionando.")

        if response and response.text:
            return True, "Chave validada com sucesso!"
        else:
            return False, "A API respondeu mas sem conteúdo esperado"

    except Exception as e:
        error_msg = str(e)

        # Mensagens de erro mais amigáveis
        if "API_KEY_INVALID" in error_msg or "invalid" in error_msg.lower():
            return False, "Chave API inválida. Verifique se copiou corretamente."
        elif "PERMISSION_DENIED" in error_msg:
            return False, "Permissão negada. Verifique se a chave tem as permissões necessárias."
        elif "quota" in error_msg.lower():
            return False, "Cota da API excedida. Tente novamente mais tarde ou use outra chave."
        else:
            return False, f"Erro ao validar: {error_msg}"


@setup_bp.route('/')
def setup_page():
    """Página de configuração inicial."""
    return render_template('setup.html')


@setup_bp.route('/configuracoes')
def configuracoes_page():
    """Página de configurações do sistema."""
    return render_template('configuracoes.html')


@setup_bp.route('/validate', methods=['POST'])
def validate_and_save():
    """
    Valida a chave API fornecida e salva no .env se for válida.
    """
    try:
        data = request.json
        api_key = data.get('api_key', '').strip()

        if not api_key:
            return jsonify({
                'success': False,
                'error': 'Chave API não fornecida'
            }), 400

        # Validação básica de formato
        if len(api_key) < 20:
            return jsonify({
                'success': False,
                'error': 'Chave API muito curta. Verifique se copiou corretamente.'
            }), 400

        # Testar a chave com a API real do Gemini
        is_valid, message = test_gemini_key(api_key)

        if not is_valid:
            return jsonify({
                'success': False,
                'error': message
            }), 400

        # Salvar no arquivo .env
        try:
            # Criar .env se não existir
            if not ENV_FILE.exists():
                ENV_FILE.touch()

            # Salvar a chave
            set_key(ENV_FILE, 'GEMINI_API_KEY', api_key)

            # Atualizar variável de ambiente na sessão atual
            os.environ['GEMINI_API_KEY'] = api_key

            # Reconfigurar a API globalmente
            genai.configure(api_key=api_key)

            return jsonify({
                'success': True,
                'message': 'Chave validada e salva com sucesso!'
            })

        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Erro ao salvar a chave: {str(e)}'
            }), 500

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro inesperado: {str(e)}'
        }), 500


@setup_bp.route('/check', methods=['GET'])
def check_configuration():
    """
    Verifica se a configuração está completa.
    Retorna status da chave API.
    """
    api_key = os.environ.get('GEMINI_API_KEY')

    is_configured = bool(api_key and api_key not in ['sua_chave_api_aqui', '', 'YOUR_API_KEY_HERE'])

    return jsonify({
        'configured': is_configured,
        'key_present': bool(api_key),
        'key_preview': f"{api_key[:8]}...{api_key[-4:]}" if is_configured else None
    })
