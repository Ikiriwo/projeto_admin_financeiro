#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gerenciador de Configurações Seguras
Solicita chaves API ao usuário se não estiverem configuradas no .env
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv, set_key

# Carregar variáveis de ambiente
load_dotenv()

ENV_FILE = Path(__file__).parent / '.env'


def check_gemini_key():
    """Verifica se a chave GEMINI_API_KEY está configurada."""
    api_key = os.environ.get('GEMINI_API_KEY')

    # Verificar se está vazia ou com valor de exemplo
    if not api_key or api_key in ['sua_chave_api_aqui', '', 'YOUR_API_KEY_HERE']:
        return None

    return api_key


def check_database_url():
    """Verifica se DATABASE_URL está configurada."""
    db_url = os.environ.get('DATABASE_URL')

    if not db_url or 'localhost' in db_url:
        # Se for localhost, está OK para desenvolvimento
        return db_url

    return db_url


def prompt_for_gemini_key():
    """Solicita a chave GEMINI_API_KEY ao usuário via terminal."""
    print("\n" + "="*70)
    print("⚠️  CONFIGURAÇÃO NECESSÁRIA: Google Gemini API Key")
    print("="*70)
    print()
    print("A chave GEMINI_API_KEY não foi encontrada ou está inválida.")
    print()
    print("📝 Como obter sua chave:")
    print("   1. Acesse: https://makersuite.google.com/app/apikey")
    print("   2. Faça login com sua conta Google")
    print("   3. Clique em 'Create API Key'")
    print("   4. Copie a chave gerada")
    print()
    print("🔒 SEGURANÇA:")
    print("   - Sua chave será salva APENAS localmente no arquivo .env")
    print("   - O arquivo .env NÃO é enviado para o Git (está no .gitignore)")
    print("   - NUNCA compartilhe sua chave API publicamente")
    print()
    print("="*70)
    print()

    while True:
        api_key = input("Digite sua GEMINI_API_KEY (ou 'sair' para cancelar): ").strip()

        if api_key.lower() == 'sair':
            print("\n❌ Configuração cancelada. O sistema não pode iniciar sem a chave API.")
            return None

        if len(api_key) < 20:
            print("⚠️  Chave muito curta. Verifique se copiou corretamente.")
            continue

        # Confirmar
        print()
        print(f"Chave fornecida: {api_key[:10]}...{api_key[-10:]}")
        confirma = input("Confirma esta chave? (s/n): ").strip().lower()

        if confirma == 's':
            return api_key
        else:
            print("Vamos tentar novamente...\n")


def save_to_env_file(key, value):
    """Salva uma variável no arquivo .env."""
    try:
        # Criar .env se não existir
        if not ENV_FILE.exists():
            ENV_FILE.touch()
            print(f"✅ Arquivo .env criado em: {ENV_FILE}")

        # Salvar chave
        set_key(ENV_FILE, key, value)

        # Atualizar variável de ambiente na sessão atual
        os.environ[key] = value

        print(f"✅ {key} salva com sucesso no arquivo .env")
        return True

    except Exception as e:
        print(f"❌ Erro ao salvar no .env: {e}")
        return False


def ensure_configuration():
    """
    Garante que todas as configurações necessárias estão presentes.
    Solicita ao usuário se necessário.
    Retorna True se tudo estiver OK, False caso contrário.
    """
    print("\n🔍 Verificando configurações...")

    all_ok = True

    # Verificar GEMINI_API_KEY
    gemini_key = check_gemini_key()

    if not gemini_key:
        print("⚠️  GEMINI_API_KEY não configurada")

        # Solicitar ao usuário
        new_key = prompt_for_gemini_key()

        if not new_key:
            all_ok = False
        else:
            # Salvar no .env
            if save_to_env_file('GEMINI_API_KEY', new_key):
                print()
                print("✅ Chave API configurada com sucesso!")
            else:
                all_ok = False
    else:
        print(f"✅ GEMINI_API_KEY: {gemini_key[:10]}...{gemini_key[-4:]}")

    print()

    # Verificar DATABASE_URL
    db_url = check_database_url()
    if db_url:
        # Mascarar senha na exibição
        masked_url = db_url.split('@')[0].split(':')[0] + ':***@' + db_url.split('@')[1] if '@' in db_url else db_url
        print(f"✅ DATABASE_URL: {masked_url}")
    else:
        print("⚠️  DATABASE_URL não configurada (usando padrão)")

    print()

    if not all_ok:
        print("="*70)
        print("❌ Configuração incompleta. O sistema não pode iniciar.")
        print("="*70)
        return False

    print("="*70)
    print("✅ Todas as configurações estão OK!")
    print("="*70)
    print()

    return True


def check_env_security():
    """Verifica se o .env está protegido no .gitignore."""
    gitignore_file = Path(__file__).parent / '.gitignore'

    if not gitignore_file.exists():
        print("⚠️  .gitignore não encontrado!")
        return False

    with open(gitignore_file, 'r') as f:
        content = f.read()

    if '.env' in content:
        return True
    else:
        print("⚠️  .env não está no .gitignore!")
        print("   Adicionando automaticamente...")

        with open(gitignore_file, 'a') as f:
            f.write("\n# Environment variables (NUNCA commite este arquivo!)\n")
            f.write(".env\n")

        print("✅ .env adicionado ao .gitignore")
        return True


if __name__ == '__main__':
    """Pode ser executado diretamente para configurar o sistema."""
    print("="*70)
    print("🔧 CONFIGURAÇÃO DO SISTEMA")
    print("   Sistema Administrativo-Financeiro")
    print("="*70)

    # Verificar segurança do .gitignore
    check_env_security()

    # Garantir configurações
    if ensure_configuration():
        print("🚀 Sistema pronto para iniciar!")
        print()
        print("Para iniciar a aplicação, execute:")
        print("   python app.py")
        print()
        sys.exit(0)
    else:
        print("❌ Configure as variáveis necessárias antes de continuar.")
        sys.exit(1)
