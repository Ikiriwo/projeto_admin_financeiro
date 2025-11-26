# Scripts de Gerenciamento

Scripts utilitários para gerenciar o banco de dados.

## Comandos Rápidos

```bash
# Limpar banco de dados
python scripts/clear_database.py

# Popular com dados de teste (250+ registros)
python scripts/populate_database.py

# Limpar e popular do zero
python scripts/populate_database.py --clear

# Verificar status
python scripts/populate_database.py --status
```

## Scripts Disponíveis

### `clear_database.py` - Limpar Banco
Limpa todos os dados do banco de dados com confirmação.

### `populate_database.py` - Popular Banco
Popula o banco com 250+ registros de teste:
- 80 Pessoas (fornecedores, clientes, faturados)
- 40 Classificações (despesas e receitas)
- 80 Parcelas de contas
- 5+ Movimentos completos

### `init_database.py` - Inicializar Banco
Cria todas as tabelas do zero.

### `health_check.py` - Verificar Saúde
Verifica conectividade e status do banco.
