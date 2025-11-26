#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para inicializar o banco de dados do Sistema Administrativo-Financeiro.

Este script:
1. Cria todas as tabelas do banco de dados
2. Opcionalmente popula com dados de teste

Uso:
    python scripts/init_database.py
    python scripts/init_database.py --seed  # Com dados de teste
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório raiz ao path para importar os módulos
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

import argparse
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

from app import app, db
from models.pessoas import Pessoas
from models.classificacao import Classificacao
from models.movimento_contas import MovimentoContas
from models.parcelas_contas import ParcelasContas
from models.nota_fiscal import NotaFiscal, ProdutoNotaFiscal
from datetime import datetime, date


def create_tables():
    """Cria todas as tabelas do banco de dados."""
    print("🔧 Criando tabelas no banco de dados...")

    with app.app_context():
        try:
            # Criar todas as tabelas
            db.create_all()
            print("✅ Tabelas criadas com sucesso!")
            return True
        except Exception as e:
            print(f"❌ Erro ao criar tabelas: {e}")
            return False


def seed_sample_data():
    """Popula o banco com alguns dados de exemplo para teste rápido."""
    print("🌱 Populando banco com dados de exemplo...")

    with app.app_context():
        try:
            # Verificar se já existem dados
            if Pessoas.query.count() > 0:
                print("⚠️  O banco já contém dados. Deseja continuar? (s/n)")
                resposta = input().lower()
                if resposta != 's':
                    print("❌ Operação cancelada.")
                    return False

            # Criar pessoas de exemplo
            print("  📝 Criando pessoas...")

            fornecedor1 = Pessoas.criar_novo(
                tipo='FORNECEDOR',
                razao_social='Tech Solutions LTDA',
                cpf_cnpj='12.345.678/0001-01'
            )

            fornecedor2 = Pessoas.criar_novo(
                tipo='FORNECEDOR',
                razao_social='Materiais de Escritório SA',
                cpf_cnpj='23.456.789/0001-02'
            )

            cliente1 = Pessoas.criar_novo(
                tipo='CLIENTE',
                razao_social='Empresa ABC Comercio',
                cpf_cnpj='11.222.333/0001-01'
            )

            faturado1 = Pessoas.criar_novo(
                tipo='FATURADO',
                razao_social='João da Silva',
                cpf_cnpj='123.456.789-01'
            )

            faturado2 = Pessoas.criar_novo(
                tipo='FATURADO',
                razao_social='Maria Santos',
                cpf_cnpj='234.567.890-12'
            )

            print(f"  ✅ Criadas {Pessoas.query.count()} pessoas")

            # Criar classificações
            print("  📊 Criando classificações...")

            desp1 = Classificacao.criar_nova('DESPESA', 'Material de Escritório')
            desp2 = Classificacao.criar_nova('DESPESA', 'Energia Elétrica')
            desp3 = Classificacao.criar_nova('DESPESA', 'Aluguel')

            rec1 = Classificacao.criar_nova('RECEITA', 'Venda de Produtos')
            rec2 = Classificacao.criar_nova('RECEITA', 'Prestação de Serviços')

            print(f"  ✅ Criadas {Classificacao.query.count()} classificações")

            # Criar parcelas
            print("  💰 Criando parcelas...")

            parcela1 = ParcelasContas.criar_nova(
                identificacao='PARC-2024-TESTE-001',
                numero_nota='NF-001',
                data_emissao=date(2024, 1, 15),
                data_vencimento=date(2024, 2, 15),
                valor_total=1500.00
            )

            parcela2 = ParcelasContas.criar_nova(
                identificacao='REC-2024-TESTE-001',
                numero_nota='RC-001',
                data_emissao=date(2024, 1, 10),
                data_vencimento=date(2024, 2, 10),
                valor_total=8500.00
            )

            print(f"  ✅ Criadas {ParcelasContas.query.count()} parcelas")

            # Criar movimentos
            print("  💸 Criando movimentos...")

            mov1 = MovimentoContas.criar_novo(
                tipo='APAGAR',
                parcela_id=parcela1.id,
                fornecedor_cliente_id=fornecedor1.id,
                faturado_id=faturado1.id,
                valor=1500.00,
                classificacoes=[desp1, desp2]
            )

            mov2 = MovimentoContas.criar_novo(
                tipo='ARECEBER',
                parcela_id=parcela2.id,
                fornecedor_cliente_id=cliente1.id,
                faturado_id=faturado2.id,
                valor=8500.00,
                classificacoes=[rec1]
            )

            print(f"  ✅ Criados {MovimentoContas.query.count()} movimentos")

            print("✅ Dados de exemplo criados com sucesso!")
            print("\n📊 Resumo:")
            print(f"   - Pessoas: {Pessoas.query.count()}")
            print(f"   - Classificações: {Classificacao.query.count()}")
            print(f"   - Parcelas: {ParcelasContas.query.count()}")
            print(f"   - Movimentos: {MovimentoContas.query.count()}")

            return True

        except Exception as e:
            print(f"❌ Erro ao popular dados: {e}")
            db.session.rollback()
            return False


def main():
    """Função principal do script."""
    parser = argparse.ArgumentParser(
        description='Inicializar banco de dados do Sistema Administrativo-Financeiro'
    )
    parser.add_argument(
        '--seed',
        action='store_true',
        help='Popular banco com dados de exemplo'
    )
    parser.add_argument(
        '--seed-full',
        action='store_true',
        help='Executar script SQL completo (200+ registros)'
    )

    args = parser.parse_args()

    print("=" * 70)
    print("🚀 INICIALIZAÇÃO DO BANCO DE DADOS")
    print("   Sistema Administrativo-Financeiro")
    print("=" * 70)
    print()

    # Verificar conexão com o banco
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ Erro: DATABASE_URL não configurado no .env")
        print("   Configure o arquivo .env antes de continuar.")
        return 1

    print(f"🔌 Conectando ao banco de dados...")
    print(f"   URL: {database_url[:30]}...")
    print()

    # Criar tabelas
    if not create_tables():
        return 1

    print()

    # Popular com dados se solicitado
    if args.seed:
        if not seed_sample_data():
            return 1

    elif args.seed_full:
        print("📜 Para popular com o script SQL completo (200+ registros), execute:")
        print()
        print("   # Local:")
        print(f"   psql -U usuario -d financeiro -f {ROOT_DIR}/scripts/seed_database.sql")
        print()
        print("   # Docker:")
        print("   docker-compose exec db psql -U usuario -d financeiro -f /scripts/seed_database.sql")
        print()

    print()
    print("=" * 70)
    print("✅ INICIALIZAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 70)
    print()
    print("🌐 Para iniciar a aplicação, execute:")
    print("   python app.py")
    print()
    print("🔗 Acesse em: http://localhost:5000")
    print()

    return 0


if __name__ == '__main__':
    sys.exit(main())
