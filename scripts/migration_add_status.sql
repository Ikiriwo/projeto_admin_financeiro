-- ============================================================================
-- SCRIPT DE MIGRAÇÃO: Adicionar campo STATUS às tabelas
-- ============================================================================
-- Execute este script se você já tem um banco de dados existente
-- sem o campo STATUS nas tabelas.
--
-- ATENÇÃO: Faça backup antes de executar!
-- ============================================================================

-- Verificar se os campos já existem (apenas informativo)
SELECT 'Verificando estrutura atual...' as status;

-- ============================================================================
-- 1. Adicionar campo STATUS na tabela PESSOAS
-- ============================================================================
DO $$
BEGIN
    -- Verificar se a coluna já existe
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'pessoas' AND column_name = 'status'
    ) THEN
        -- Adicionar coluna
        ALTER TABLE pessoas ADD COLUMN status VARCHAR(20) DEFAULT 'ATIVO' NOT NULL;
        RAISE NOTICE 'Campo STATUS adicionado à tabela PESSOAS';
    ELSE
        RAISE NOTICE 'Campo STATUS já existe na tabela PESSOAS';
    END IF;
END $$;

-- Atualizar registros existentes para ATIVO (se não estiverem)
UPDATE pessoas SET status = 'ATIVO' WHERE status IS NULL;

-- ============================================================================
-- 2. Adicionar campo STATUS na tabela CLASSIFICACAO
-- ============================================================================
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'classificacao' AND column_name = 'status'
    ) THEN
        ALTER TABLE classificacao ADD COLUMN status VARCHAR(20) DEFAULT 'ATIVO' NOT NULL;
        RAISE NOTICE 'Campo STATUS adicionado à tabela CLASSIFICACAO';
    ELSE
        RAISE NOTICE 'Campo STATUS já existe na tabela CLASSIFICACAO';
    END IF;
END $$;

-- Atualizar registros existentes
UPDATE classificacao SET status = 'ATIVO' WHERE status IS NULL;

-- ============================================================================
-- 3. Adicionar campo STATUS na tabela MOVIMENTO_CONTAS
-- ============================================================================
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'movimento_contas' AND column_name = 'status'
    ) THEN
        ALTER TABLE movimento_contas ADD COLUMN status VARCHAR(20) DEFAULT 'ATIVO' NOT NULL;
        RAISE NOTICE 'Campo STATUS adicionado à tabela MOVIMENTO_CONTAS';
    ELSE
        RAISE NOTICE 'Campo STATUS já existe na tabela MOVIMENTO_CONTAS';
    END IF;
END $$;

-- Atualizar registros existentes
UPDATE movimento_contas SET status = 'ATIVO' WHERE status IS NULL;

-- ============================================================================
-- 4. Criar índices para melhor performance
-- ============================================================================

-- Índice para consultas por STATUS em PESSOAS
CREATE INDEX IF NOT EXISTS idx_pessoas_status ON pessoas(status);

-- Índice para consultas por STATUS em CLASSIFICACAO
CREATE INDEX IF NOT EXISTS idx_classificacao_status ON classificacao(status);

-- Índice para consultas por STATUS em MOVIMENTO_CONTAS
CREATE INDEX IF NOT EXISTS idx_movimento_contas_status ON movimento_contas(status);

-- Índice composto para consultas por TIPO e STATUS em PESSOAS
CREATE INDEX IF NOT EXISTS idx_pessoas_tipo_status ON pessoas(tipo, status);

-- Índice composto para consultas por TIPO e STATUS em CLASSIFICACAO
CREATE INDEX IF NOT EXISTS idx_classificacao_tipo_status ON classificacao(tipo, status);

-- Índice composto para consultas por TIPO e STATUS em MOVIMENTO_CONTAS
CREATE INDEX IF NOT EXISTS idx_movimento_tipo_status ON movimento_contas(tipo, status);

-- ============================================================================
-- 5. Verificação Final
-- ============================================================================
SELECT 'Verificando campos STATUS...' as status;

SELECT
    'pessoas' as tabela,
    COUNT(*) as total_registros,
    SUM(CASE WHEN status = 'ATIVO' THEN 1 ELSE 0 END) as ativos,
    SUM(CASE WHEN status = 'INATIVO' THEN 1 ELSE 0 END) as inativos
FROM pessoas
UNION ALL
SELECT
    'classificacao' as tabela,
    COUNT(*) as total_registros,
    SUM(CASE WHEN status = 'ATIVO' THEN 1 ELSE 0 END) as ativos,
    SUM(CASE WHEN status = 'INATIVO' THEN 1 ELSE 0 END) as inativos
FROM classificacao
UNION ALL
SELECT
    'movimento_contas' as tabela,
    COUNT(*) as total_registros,
    SUM(CASE WHEN status = 'ATIVO' THEN 1 ELSE 0 END) as ativos,
    SUM(CASE WHEN status = 'INATIVO' THEN 1 ELSE 0 END) as inativos
FROM movimento_contas;

-- ============================================================================
-- Migração Concluída!
-- ============================================================================
SELECT '✅ Migração concluída com sucesso!' as resultado;

-- ============================================================================
-- ROLLBACK (use apenas se necessário)
-- ============================================================================
-- ATENÇÃO: Descomente apenas se precisar reverter as mudanças!
--
-- DROP INDEX IF EXISTS idx_pessoas_status;
-- DROP INDEX IF EXISTS idx_classificacao_status;
-- DROP INDEX IF EXISTS idx_movimento_contas_status;
-- DROP INDEX IF EXISTS idx_pessoas_tipo_status;
-- DROP INDEX IF EXISTS idx_classificacao_tipo_status;
-- DROP INDEX IF EXISTS idx_movimento_tipo_status;
--
-- ALTER TABLE pessoas DROP COLUMN IF EXISTS status;
-- ALTER TABLE classificacao DROP COLUMN IF EXISTS status;
-- ALTER TABLE movimento_contas DROP COLUMN IF EXISTS status;
-- ============================================================================
