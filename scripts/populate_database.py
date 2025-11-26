#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para popular o banco de dados com dados de teste.
Pode ser executado diretamente ou via interface web.
"""

import os
import sys
from pathlib import Path

# Adicionar diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from flask import has_app_context, current_app


def read_sql_file():
    """Lê o arquivo SQL de seed."""
    sql_file = Path(__file__).parent / 'seed_database.sql'

    if not sql_file.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {sql_file}")

    return sql_file.read_text(encoding='utf-8')


def clear_database():
    """Limpa todas as tabelas do banco de dados."""
    from models import db

    print("🗑️  Limpando banco de dados...")

    def _do_clear():
        try:
            # Desabilitar constraints temporariamente
            db.session.execute(text("SET session_replication_role = 'replica';"))

            # Limpar tabelas em ordem
            tables = [
                'movimento_classificacao',
                'movimento_contas',
                'parcelas_contas',
                'classificacao',
                'pessoas'
            ]

            for table in tables:
                db.session.execute(text(f"TRUNCATE TABLE {table} CASCADE;"))
                print(f"   ✓ Tabela '{table}' limpa")

            # Reabilitar constraints
            db.session.execute(text("SET session_replication_role = 'origin';"))

            db.session.commit()
            print("✅ Banco de dados limpo com sucesso!\n")
            return True

        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro ao limpar banco: {e}\n")
            return False

    # Se já estamos em um contexto Flask, executar diretamente
    if has_app_context():
        return _do_clear()
    else:
        # Caso contrário, criar contexto
        from app import app
        with app.app_context():
            return _do_clear()


def populate_database(clear_first=False):
    """
    Popula o banco de dados com dados de teste.

    Args:
        clear_first (bool): Se True, limpa o banco antes de popular

    Returns:
        tuple: (success: bool, message: str, stats: dict)
    """
    from models import db

    print("=" * 70)
    print("📊 POPULAÇÃO DO BANCO DE DADOS")
    print("=" * 70)
    print()

    # Limpar banco se solicitado
    if clear_first:
        if not clear_database():
            return False, "Erro ao limpar banco de dados", {}

    print("📝 Inserindo dados de teste...")
    print()

    def _do_populate():
        try:
            # Ler arquivo SQL
            sql_content = read_sql_file()

            # Executar o script
            # Dividir por blocos DO $$ para executar separadamente
            statements = sql_content.split('-- ============================================================================')

            for i, statement in enumerate(statements, 1):
                if statement.strip():
                    try:
                        db.session.execute(text(statement))
                        print(f"   ✓ Bloco {i} executado")
                    except Exception as e:
                        # Ignorar erros em comentários vazios
                        if 'syntax error' not in str(e).lower():
                            print(f"   ⚠️  Aviso no bloco {i}: {e}")

            db.session.commit()

            # Obter estatísticas
            stats = {}
            queries = {
                'pessoas': "SELECT COUNT(*) FROM pessoas",
                'classificacoes': "SELECT COUNT(*) FROM classificacao",
                'parcelas': "SELECT COUNT(*) FROM parcelas_contas",
                'movimentos': "SELECT COUNT(*) FROM movimento_contas",
                'relacionamentos': "SELECT COUNT(*) FROM movimento_classificacao"
            }

            print()
            print("📊 Estatísticas:")
            for key, query in queries.items():
                result = db.session.execute(text(query)).scalar()
                stats[key] = result
                print(f"   • {key.capitalize()}: {result}")

            print()
            print("=" * 70)
            print("✅ BANCO DE DADOS POPULADO COM SUCESSO!")
            print("=" * 70)

            total = sum(stats.values())
            return True, f"Sucesso! {total} registros inseridos", stats

        except Exception as e:
            db.session.rollback()
            error_msg = f"Erro ao popular banco: {str(e)}"
            print()
            print("=" * 70)
            print(f"❌ ERRO: {error_msg}")
            print("=" * 70)
            return False, error_msg, {}

    # Se já estamos em um contexto Flask, executar diretamente
    if has_app_context():
        return _do_populate()
    else:
        # Caso contrário, criar contexto
        from app import app
        with app.app_context():
            return _do_populate()


def check_database_status():
    """Verifica o status atual do banco de dados."""
    from models import db

    print("🔍 Verificando status do banco de dados...")
    print()

    def _do_check():
        try:
            queries = {
                'Pessoas': "SELECT COUNT(*) FROM pessoas",
                'Classificações': "SELECT COUNT(*) FROM classificacao",
                'Parcelas': "SELECT COUNT(*) FROM parcelas_contas",
                'Movimentos': "SELECT COUNT(*) FROM movimento_contas",
            }

            for name, query in queries.items():
                count = db.session.execute(text(query)).scalar()
                status = "✅" if count > 0 else "⚠️ "
                print(f"   {status} {name}: {count} registros")

            print()
            return True

        except Exception as e:
            print(f"❌ Erro ao verificar status: {e}")
            print()
            return False

    # Se já estamos em um contexto Flask, executar diretamente
    if has_app_context():
        return _do_check()
    else:
        # Caso contrário, criar contexto
        from app import app
        with app.app_context():
            return _do_check()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Popular banco de dados com dados de teste')
    parser.add_argument('--clear', action='store_true', help='Limpar banco antes de popular')
    parser.add_argument('--status', action='store_true', help='Apenas verificar status do banco')

    args = parser.parse_args()

    if args.status:
        # Apenas verificar status
        check_database_status()
    else:
        # Popular banco
        success, message, stats = populate_database(clear_first=args.clear)

        if not success:
            sys.exit(1)

        sys.exit(0)
