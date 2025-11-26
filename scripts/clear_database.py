#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script simples para limpar todos os dados do banco de dados.
Uso: python scripts/clear_database.py
"""

import os
import sys
from pathlib import Path

# Adicionar diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from models import db


def clear_all_data():
    """Limpa todos os dados do banco de dados."""
    from app import app

    print("=" * 70)
    print("⚠️  LIMPEZA DO BANCO DE DADOS")
    print("=" * 70)
    print()
    print("Esta operação vai DELETAR TODOS os dados do banco!")
    print()

    # Confirmação
    confirm = input("Digite 'SIM' para confirmar: ").strip().upper()

    if confirm != 'SIM':
        print("\n❌ Operação cancelada.")
        return False

    print()
    print("🗑️  Limpando banco de dados...")
    print()

    with app.app_context():
        try:
            # Desabilitar constraints temporariamente
            db.session.execute(text("SET session_replication_role = 'replica';"))

            # Limpar tabelas em ordem
            tables = [
                'movimento_classificacao',
                'movimento_contas',
                'parcelas_contas',
                'classificacao',
                'pessoas',
                'produtos_nota_fiscal',
                'notas_fiscais'
            ]

            for table in tables:
                try:
                    db.session.execute(text(f"TRUNCATE TABLE {table} CASCADE;"))
                    print(f"   ✓ Tabela '{table}' limpa")
                except Exception as e:
                    print(f"   ⚠️  Tabela '{table}': {e}")

            # Reabilitar constraints
            db.session.execute(text("SET session_replication_role = 'origin';"))

            db.session.commit()
            print()
            print("=" * 70)
            print("✅ BANCO DE DADOS LIMPO COM SUCESSO!")
            print("=" * 70)
            return True

        except Exception as e:
            db.session.rollback()
            print()
            print("=" * 70)
            print(f"❌ ERRO: {e}")
            print("=" * 70)
            return False


if __name__ == '__main__':
    success = clear_all_data()
    sys.exit(0 if success else 1)
