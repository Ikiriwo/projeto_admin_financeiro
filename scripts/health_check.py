#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para verificar a saúde do Sistema Administrativo-Financeiro.

Este script verifica:
1. Conexão com o banco de dados
2. Existência das tabelas necessárias
3. Configuração das variáveis de ambiente
4. API do Google Gemini

Uso:
    python scripts/health_check.py
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório raiz ao path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from dotenv import load_dotenv
import google.generativeai as genai

# Carregar variáveis de ambiente
load_dotenv()


def check_env_variables():
    """Verifica se as variáveis de ambiente estão configuradas."""
    print("🔍 Verificando variáveis de ambiente...")

    required_vars = ['DATABASE_URL', 'GEMINI_API_KEY']
    optional_vars = ['GEMINI_MODEL', 'POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_DB']

    all_ok = True

    for var in required_vars:
        value = os.environ.get(var)
        if value:
            masked_value = value[:10] + '...' if len(value) > 10 else value
            print(f"  ✅ {var}: {masked_value}")
        else:
            print(f"  ❌ {var}: NÃO CONFIGURADO")
            all_ok = False

    print()
    print("  Variáveis opcionais:")
    for var in optional_vars:
        value = os.environ.get(var)
        if value:
            masked_value = value[:10] + '...' if len(value) > 10 else value
            print(f"  ✅ {var}: {masked_value}")
        else:
            print(f"  ⚠️  {var}: não configurado (usando padrão)")

    return all_ok


def check_database():
    """Verifica conexão e estrutura do banco de dados."""
    print("\n🗄️  Verificando banco de dados...")

    try:
        from app import app, db
        from models.pessoas import Pessoas
        from models.classificacao import Classificacao
        from models.movimento_contas import MovimentoContas
        from models.parcelas_contas import ParcelasContas

        with app.app_context():
            # Testar conexão
            db.engine.connect()
            print("  ✅ Conexão estabelecida")

            # Verificar tabelas
            tables = ['pessoas', 'classificacao', 'movimento_contas', 'parcelas_contas']
            existing_tables = db.inspect(db.engine).get_table_names()

            print("\n  Verificando tabelas:")
            all_tables_exist = True
            for table in tables:
                if table in existing_tables:
                    print(f"    ✅ {table}")
                else:
                    print(f"    ❌ {table} - NÃO EXISTE")
                    all_tables_exist = False

            if not all_tables_exist:
                print("\n  ⚠️  Execute: python scripts/init_database.py")
                return False

            # Contar registros
            print("\n  Contagem de registros:")
            print(f"    📊 Pessoas: {Pessoas.query.count()}")
            print(f"    📊 Classificações: {Classificacao.query.count()}")
            print(f"    📊 Movimentos: {MovimentoContas.query.count()}")
            print(f"    📊 Parcelas: {ParcelasContas.query.count()}")

            # Verificar STATUS em registros
            pessoas_ativas = Pessoas.query.filter_by(status='ATIVO').count()
            print(f"\n    ✅ Pessoas ATIVAS: {pessoas_ativas}")

            return True

    except Exception as e:
        print(f"  ❌ Erro: {e}")
        return False


def check_gemini_api():
    """Verifica a API do Google Gemini."""
    print("\n🤖 Verificando API Google Gemini...")

    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key or api_key == 'sua_chave_api_aqui':
        print("  ❌ API Key não configurada corretamente")
        print("     Configure GEMINI_API_KEY no arquivo .env")
        return False

    try:
        genai.configure(api_key=api_key)
        model_name = os.environ.get('GEMINI_MODEL', 'gemini-2.0-flash')

        # Testar com uma requisição simples
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Diga 'OK' se você está funcionando.")

        if response and response.text:
            print(f"  ✅ API funcionando ({model_name})")
            print(f"     Resposta: {response.text[:50]}...")
            return True
        else:
            print("  ⚠️  API respondeu mas sem conteúdo")
            return False

    except Exception as e:
        print(f"  ❌ Erro ao testar API: {e}")
        return False


def check_directories():
    """Verifica se os diretórios necessários existem."""
    print("\n📁 Verificando estrutura de diretórios...")

    required_dirs = [
        'frontend/static/css',
        'frontend/static/js',
        'frontend/templates',
        'models',
        'routes',
        'rag_system',
        'agents',
        'scripts',
        'uploads'
    ]

    all_ok = True
    for dir_path in required_dirs:
        full_path = ROOT_DIR / dir_path
        if full_path.exists():
            print(f"  ✅ {dir_path}")
        else:
            print(f"  ❌ {dir_path} - NÃO EXISTE")
            all_ok = False

            # Criar diretório uploads se não existir
            if dir_path == 'uploads':
                full_path.mkdir(parents=True, exist_ok=True)
                print(f"     ✅ Criado automaticamente")
                all_ok = True

    return all_ok


def check_files():
    """Verifica se os arquivos essenciais existem."""
    print("\n📄 Verificando arquivos essenciais...")

    required_files = [
        'app.py',
        'requirements.txt',
        'Dockerfile',
        'docker-compose.yml',
        '.env.example',
        'README.md',
        'MANUAL_DEPLOY.md'
    ]

    all_ok = True
    for file_path in required_files:
        full_path = ROOT_DIR / file_path
        if full_path.exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - NÃO EXISTE")
            all_ok = False

    # Verificar .env
    env_path = ROOT_DIR / '.env'
    if env_path.exists():
        print(f"  ✅ .env")
    else:
        print(f"  ⚠️  .env - NÃO EXISTE (copie de .env.example)")

    return all_ok


def main():
    """Função principal."""
    print("=" * 70)
    print("🏥 VERIFICAÇÃO DE SAÚDE DO SISTEMA")
    print("   Sistema Administrativo-Financeiro")
    print("=" * 70)
    print()

    results = {
        'env': check_env_variables(),
        'dirs': check_directories(),
        'files': check_files(),
        'database': check_database(),
        'gemini': check_gemini_api()
    }

    print()
    print("=" * 70)
    print("📊 RESUMO DA VERIFICAÇÃO")
    print("=" * 70)
    print()

    status_emoji = {True: '✅', False: '❌'}

    print(f"  {status_emoji[results['env']]} Variáveis de Ambiente")
    print(f"  {status_emoji[results['dirs']]} Estrutura de Diretórios")
    print(f"  {status_emoji[results['files']]} Arquivos Essenciais")
    print(f"  {status_emoji[results['database']]} Banco de Dados")
    print(f"  {status_emoji[results['gemini']]} API Google Gemini")

    all_ok = all(results.values())

    print()
    if all_ok:
        print("✅ SISTEMA SAUDÁVEL - PRONTO PARA USO!")
        print()
        print("🚀 Para iniciar a aplicação:")
        print("   python app.py")
        print()
        print("🔗 Acesse em: http://localhost:5000")
    else:
        print("⚠️  PROBLEMAS DETECTADOS")
        print()
        print("📋 Próximos passos:")
        if not results['env']:
            print("   1. Configure o arquivo .env (copie de .env.example)")
        if not results['database']:
            print("   2. Execute: python scripts/init_database.py")
        if not results['gemini']:
            print("   3. Configure GEMINI_API_KEY no .env")

    print()
    print("=" * 70)
    print()

    return 0 if all_ok else 1


if __name__ == '__main__':
    sys.exit(main())
