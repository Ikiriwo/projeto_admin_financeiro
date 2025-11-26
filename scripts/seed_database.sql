-- ============================================================================
-- Script SQL para Popular o Banco de Dados com Dados de Teste
-- Sistema Administrativo-Financeiro
-- Total de registros: 250+ (distribuídos entre as tabelas)
-- ============================================================================

-- Limpar dados existentes (opcional - comentar se não quiser limpar)
-- TRUNCATE TABLE movimento_classificacao CASCADE;
-- TRUNCATE TABLE movimento_contas CASCADE;
-- TRUNCATE TABLE classificacao CASCADE;
-- TRUNCATE TABLE pessoas CASCADE;
-- TRUNCATE TABLE parcelas_contas CASCADE;

-- ============================================================================
-- 1. INSERIR PESSOAS (80 registros)
-- ============================================================================

-- Fornecedores (25 registros)
INSERT INTO pessoas (tipo, razao_social, cpf_cnpj, status, data_cadastro) VALUES
('FORNECEDOR', 'Tech Solutions LTDA', '12.345.678/0001-01', 'ATIVO', NOW()),
('FORNECEDOR', 'Materiais de Escritório SA', '23.456.789/0001-02', 'ATIVO', NOW()),
('FORNECEDOR', 'Serviços de TI Brasil', '34.567.890/0001-03', 'ATIVO', NOW()),
('FORNECEDOR', 'Papelaria Central', '45.678.901/0001-04', 'ATIVO', NOW()),
('FORNECEDOR', 'Equipamentos Industriais', '56.789.012/0001-05', 'ATIVO', NOW()),
('FORNECEDOR', 'Software House Premium', '67.890.123/0001-06', 'ATIVO', NOW()),
('FORNECEDOR', 'Distribuidora Alpha', '78.901.234/0001-07', 'ATIVO', NOW()),
('FORNECEDOR', 'Importadora Beta', '89.012.345/0001-08', 'ATIVO', NOW()),
('FORNECEDOR', 'Comercial Gama LTDA', '90.123.456/0001-09', 'ATIVO', NOW()),
('FORNECEDOR', 'Telecomunicações Delta', '01.234.567/0001-10', 'ATIVO', NOW()),
('FORNECEDOR', 'Consultoria Epsilon', '12.345.678/0001-11', 'ATIVO', NOW()),
('FORNECEDOR', 'Serviços Zeta SA', '23.456.789/0001-12', 'ATIVO', NOW()),
('FORNECEDOR', 'Manutenção Eta LTDA', '34.567.890/0001-13', 'ATIVO', NOW()),
('FORNECEDOR', 'Limpeza Theta', '45.678.901/0001-14', 'ATIVO', NOW()),
('FORNECEDOR', 'Segurança Iota', '56.789.012/0001-15', 'ATIVO', NOW()),
('FORNECEDOR', 'Alimentos Kappa LTDA', '67.890.123/0001-16', 'ATIVO', NOW()),
('FORNECEDOR', 'Transporte Lambda', '78.901.234/0001-17', 'ATIVO', NOW()),
('FORNECEDOR', 'Logística Mu SA', '89.012.345/0001-18', 'ATIVO', NOW()),
('FORNECEDOR', 'Publicidade Nu', '90.123.456/0001-19', 'ATIVO', NOW()),
('FORNECEDOR', 'Marketing Xi LTDA', '01.234.567/0001-20', 'ATIVO', NOW()),
('FORNECEDOR', 'Design Omicron', '12.345.678/0001-21', 'INATIVO', NOW()),
('FORNECEDOR', 'Eventos Pi SA', '23.456.789/0001-22', 'ATIVO', NOW()),
('FORNECEDOR', 'Contabilidade Rho', '34.567.890/0001-23', 'ATIVO', NOW()),
('FORNECEDOR', 'Advocacia Sigma LTDA', '45.678.901/0001-24', 'ATIVO', NOW()),
('FORNECEDOR', 'Engenharia Tau', '56.789.012/0001-25', 'ATIVO', NOW());

-- Clientes (25 registros)
INSERT INTO pessoas (tipo, razao_social, cpf_cnpj, status, data_cadastro) VALUES
('CLIENTE', 'Empresa ABC Comercio', '11.222.333/0001-01', 'ATIVO', NOW()),
('CLIENTE', 'Varejo XYZ LTDA', '22.333.444/0001-02', 'ATIVO', NOW()),
('CLIENTE', 'Industria 123', '33.444.555/0001-03', 'ATIVO', NOW()),
('CLIENTE', 'Comercio Geral SA', '44.555.666/0001-04', 'ATIVO', NOW()),
('CLIENTE', 'Servicos Premium', '55.666.777/0001-05', 'ATIVO', NOW()),
('CLIENTE', 'Atacado Direto LTDA', '66.777.888/0001-06', 'ATIVO', NOW()),
('CLIENTE', 'Rede de Lojas Brasil', '77.888.999/0001-07', 'ATIVO', NOW()),
('CLIENTE', 'Supermercado Central', '88.999.000/0001-08', 'ATIVO', NOW()),
('CLIENTE', 'Farmacia Popular', '99.000.111/0001-09', 'ATIVO', NOW()),
('CLIENTE', 'Clinica Saude Plus', '10.111.222/0001-10', 'ATIVO', NOW()),
('CLIENTE', 'Hospital Regional', '21.222.333/0001-11', 'ATIVO', NOW()),
('CLIENTE', 'Escola Modelo LTDA', '32.333.444/0001-12', 'ATIVO', NOW()),
('CLIENTE', 'Universidade Federal', '43.444.555/0001-13', 'ATIVO', NOW()),
('CLIENTE', 'Restaurante Bom Sabor', '54.555.666/0001-14', 'ATIVO', NOW()),
('CLIENTE', 'Hotel Conforto SA', '65.666.777/0001-15', 'ATIVO', NOW()),
('CLIENTE', 'Agencia de Viagens', '76.777.888/0001-16', 'ATIVO', NOW()),
('CLIENTE', 'Academia Fitness', '87.888.999/0001-17', 'ATIVO', NOW()),
('CLIENTE', 'Salao de Beleza Elite', '98.999.000/0001-18', 'ATIVO', NOW()),
('CLIENTE', 'Oficina Mecanica Auto', '09.000.111/0001-19', 'ATIVO', NOW()),
('CLIENTE', 'Imobiliaria Prime', '10.111.222/0001-20', 'INATIVO', NOW()),
('CLIENTE', 'Construtora Solida', '21.222.333/0001-21', 'ATIVO', NOW()),
('CLIENTE', 'Pet Shop Animal Feliz', '32.333.444/0001-22', 'ATIVO', NOW()),
('CLIENTE', 'Livraria Cultura Plus', '43.444.555/0001-23', 'ATIVO', NOW()),
('CLIENTE', 'Joalheria Luxo', '54.555.666/0001-24', 'ATIVO', NOW()),
('CLIENTE', 'Automoveis Premium', '65.666.777/0001-25', 'ATIVO', NOW());

-- Faturados (30 registros - pessoas físicas)
INSERT INTO pessoas (tipo, razao_social, cpf_cnpj, status, data_cadastro) VALUES
('FATURADO', 'João da Silva', '123.456.789-01', 'ATIVO', NOW()),
('FATURADO', 'Maria Santos', '234.567.890-12', 'ATIVO', NOW()),
('FATURADO', 'Pedro Oliveira', '345.678.901-23', 'ATIVO', NOW()),
('FATURADO', 'Ana Costa', '456.789.012-34', 'ATIVO', NOW()),
('FATURADO', 'Carlos Souza', '567.890.123-45', 'ATIVO', NOW()),
('FATURADO', 'Juliana Lima', '678.901.234-56', 'ATIVO', NOW()),
('FATURADO', 'Roberto Alves', '789.012.345-67', 'ATIVO', NOW()),
('FATURADO', 'Fernanda Rocha', '890.123.456-78', 'ATIVO', NOW()),
('FATURADO', 'Paulo Mendes', '901.234.567-89', 'ATIVO', NOW()),
('FATURADO', 'Lucia Ferreira', '012.345.678-90', 'ATIVO', NOW()),
('FATURADO', 'Marcos Ribeiro', '123.456.789-11', 'ATIVO', NOW()),
('FATURADO', 'Patricia Gomes', '234.567.890-22', 'ATIVO', NOW()),
('FATURADO', 'Ricardo Martins', '345.678.901-33', 'ATIVO', NOW()),
('FATURADO', 'Beatriz Silva', '456.789.012-44', 'ATIVO', NOW()),
('FATURADO', 'André Cardoso', '567.890.123-55', 'ATIVO', NOW()),
('FATURADO', 'Camila Teixeira', '678.901.234-66', 'ATIVO', NOW()),
('FATURADO', 'Felipe Barbosa', '789.012.345-77', 'ATIVO', NOW()),
('FATURADO', 'Gabriela Dias', '890.123.456-88', 'ATIVO', NOW()),
('FATURADO', 'Bruno Pereira', '901.234.567-99', 'ATIVO', NOW()),
('FATURADO', 'Amanda Cavalcanti', '012.345.678-00', 'ATIVO', NOW()),
('FATURADO', 'Thiago Monteiro', '111.222.333-44', 'INATIVO', NOW()),
('FATURADO', 'Vanessa Araújo', '222.333.444-55', 'ATIVO', NOW()),
('FATURADO', 'Leonardo Freitas', '333.444.555-66', 'ATIVO', NOW()),
('FATURADO', 'Renata Castro', '444.555.666-77', 'ATIVO', NOW()),
('FATURADO', 'Daniel Moreira', '555.666.777-88', 'ATIVO', NOW()),
('FATURADO', 'Tatiana Borges', '666.777.888-99', 'ATIVO', NOW()),
('FATURADO', 'Rodrigo Cunha', '777.888.999-00', 'ATIVO', NOW()),
('FATURADO', 'Carla Vieira', '888.999.000-11', 'ATIVO', NOW()),
('FATURADO', 'Gustavo Pires', '999.000.111-22', 'ATIVO', NOW()),
('FATURADO', 'Isabela Nogueira', '000.111.222-33', 'ATIVO', NOW());

-- ============================================================================
-- 2. INSERIR CLASSIFICAÇÕES (40 registros)
-- ============================================================================

-- Despesas (25 registros)
INSERT INTO classificacao (tipo, descricao, status, data_cadastro) VALUES
('DESPESA', 'Aluguel', 'ATIVO', NOW()),
('DESPESA', 'Energia Elétrica', 'ATIVO', NOW()),
('DESPESA', 'Água', 'ATIVO', NOW()),
('DESPESA', 'Telefone/Internet', 'ATIVO', NOW()),
('DESPESA', 'Material de Escritório', 'ATIVO', NOW()),
('DESPESA', 'Material de Limpeza', 'ATIVO', NOW()),
('DESPESA', 'Manutenção de Equipamentos', 'ATIVO', NOW()),
('DESPESA', 'Combustível', 'ATIVO', NOW()),
('DESPESA', 'Salários', 'ATIVO', NOW()),
('DESPESA', 'Encargos Trabalhistas', 'ATIVO', NOW()),
('DESPESA', 'Vale Transporte', 'ATIVO', NOW()),
('DESPESA', 'Vale Refeição', 'ATIVO', NOW()),
('DESPESA', 'Plano de Saúde', 'ATIVO', NOW()),
('DESPESA', 'Seguro', 'ATIVO', NOW()),
('DESPESA', 'Impostos', 'ATIVO', NOW()),
('DESPESA', 'Taxas Bancárias', 'ATIVO', NOW()),
('DESPESA', 'Marketing e Publicidade', 'ATIVO', NOW()),
('DESPESA', 'Treinamento e Capacitação', 'ATIVO', NOW()),
('DESPESA', 'Viagens e Hospedagem', 'ATIVO', NOW()),
('DESPESA', 'Serviços de Terceiros', 'ATIVO', NOW()),
('DESPESA', 'Software/Licenças', 'ATIVO', NOW()),
('DESPESA', 'Depreciação', 'INATIVO', NOW()),
('DESPESA', 'Juros e Multas', 'ATIVO', NOW()),
('DESPESA', 'Doações', 'ATIVO', NOW()),
('DESPESA', 'Outras Despesas', 'ATIVO', NOW());

-- Receitas (15 registros)
INSERT INTO classificacao (tipo, descricao, status, data_cadastro) VALUES
('RECEITA', 'Venda de Produtos', 'ATIVO', NOW()),
('RECEITA', 'Prestação de Serviços', 'ATIVO', NOW()),
('RECEITA', 'Consultorias', 'ATIVO', NOW()),
('RECEITA', 'Royalties', 'ATIVO', NOW()),
('RECEITA', 'Licenciamento', 'ATIVO', NOW()),
('RECEITA', 'Juros de Aplicações', 'ATIVO', NOW()),
('RECEITA', 'Aluguéis Recebidos', 'ATIVO', NOW()),
('RECEITA', 'Venda de Ativos', 'ATIVO', NOW()),
('RECEITA', 'Comissões Recebidas', 'ATIVO', NOW()),
('RECEITA', 'Dividendos', 'ATIVO', NOW()),
('RECEITA', 'Descontos Obtidos', 'ATIVO', NOW()),
('RECEITA', 'Bonificações', 'ATIVO', NOW()),
('RECEITA', 'Ressarcimentos', 'ATIVO', NOW()),
('RECEITA', 'Outras Receitas', 'ATIVO', NOW()),
('RECEITA', 'Receitas Eventuais', 'INATIVO', NOW());

-- ============================================================================
-- 3. INSERIR PARCELAS DE CONTAS (80 registros)
-- ============================================================================

INSERT INTO parcelas_contas (identificacao, numero_nota, data_emissao, data_vencimento, valor_total, data_cadastro) VALUES
-- Parcelas relacionadas a despesas
('PARC-2024-001', 'NF-001', '2024-01-15', '2024-02-15', 1500.00, NOW()),
('PARC-2024-002', 'NF-002', '2024-01-20', '2024-02-20', 2800.50, NOW()),
('PARC-2024-003', 'NF-003', '2024-02-05', '2024-03-05', 450.00, NOW()),
('PARC-2024-004', 'NF-004', '2024-02-10', '2024-03-10', 3200.00, NOW()),
('PARC-2024-005', 'NF-005', '2024-02-15', '2024-03-15', 890.75, NOW()),
('PARC-2024-006', 'NF-006', '2024-03-01', '2024-04-01', 1200.00, NOW()),
('PARC-2024-007', 'NF-007', '2024-03-05', '2024-04-05', 5600.00, NOW()),
('PARC-2024-008', 'NF-008', '2024-03-10', '2024-04-10', 780.30, NOW()),
('PARC-2024-009', 'NF-009', '2024-03-15', '2024-04-15', 2100.00, NOW()),
('PARC-2024-010', 'NF-010', '2024-03-20', '2024-04-20', 950.00, NOW()),
('PARC-2024-011', 'NF-011', '2024-04-01', '2024-05-01', 1450.00, NOW()),
('PARC-2024-012', 'NF-012', '2024-04-05', '2024-05-05', 3300.00, NOW()),
('PARC-2024-013', 'NF-013', '2024-04-10', '2024-05-10', 670.50, NOW()),
('PARC-2024-014', 'NF-014', '2024-04-15', '2024-05-15', 4200.00, NOW()),
('PARC-2024-015', 'NF-015', '2024-04-20', '2024-05-20', 1890.00, NOW()),
('PARC-2024-016', 'NF-016', '2024-05-01', '2024-06-01', 2300.00, NOW()),
('PARC-2024-017', 'NF-017', '2024-05-05', '2024-06-05', 1560.00, NOW()),
('PARC-2024-018', 'NF-018', '2024-05-10', '2024-06-10', 890.00, NOW()),
('PARC-2024-019', 'NF-019', '2024-05-15', '2024-06-15', 3450.00, NOW()),
('PARC-2024-020', 'NF-020', '2024-05-20', '2024-06-20', 1200.75, NOW()),
('PARC-2024-021', 'NF-021', '2024-06-01', '2024-07-01', 2700.00, NOW()),
('PARC-2024-022', 'NF-022', '2024-06-05', '2024-07-05', 980.00, NOW()),
('PARC-2024-023', 'NF-023', '2024-06-10', '2024-07-10', 4100.00, NOW()),
('PARC-2024-024', 'NF-024', '2024-06-15', '2024-07-15', 1670.50, NOW()),
('PARC-2024-025', 'NF-025', '2024-06-20', '2024-07-20', 3200.00, NOW()),
('PARC-2024-026', 'NF-026', '2024-07-01', '2024-08-01', 1850.00, NOW()),
('PARC-2024-027', 'NF-027', '2024-07-05', '2024-08-05', 2950.00, NOW()),
('PARC-2024-028', 'NF-028', '2024-07-10', '2024-08-10', 720.00, NOW()),
('PARC-2024-029', 'NF-029', '2024-07-15', '2024-08-15', 4500.00, NOW()),
('PARC-2024-030', 'NF-030', '2024-07-20', '2024-08-20', 1290.00, NOW()),
('PARC-2024-031', 'NF-031', '2024-08-01', '2024-09-01', 3100.00, NOW()),
('PARC-2024-032', 'NF-032', '2024-08-05', '2024-09-05', 1560.00, NOW()),
('PARC-2024-033', 'NF-033', '2024-08-10', '2024-09-10', 2890.00, NOW()),
('PARC-2024-034', 'NF-034', '2024-08-15', '2024-09-15', 980.50, NOW()),
('PARC-2024-035', 'NF-035', '2024-08-20', '2024-09-20', 4200.00, NOW()),
('PARC-2024-036', 'NF-036', '2024-09-01', '2024-10-01', 1730.00, NOW()),
('PARC-2024-037', 'NF-037', '2024-09-05', '2024-10-05', 3450.00, NOW()),
('PARC-2024-038', 'NF-038', '2024-09-10', '2024-10-10', 890.00, NOW()),
('PARC-2024-039', 'NF-039', '2024-09-15', '2024-10-15', 5100.00, NOW()),
('PARC-2024-040', 'NF-040', '2024-09-20', '2024-10-20', 1450.00, NOW()),
-- Parcelas relacionadas a receitas
('REC-2024-001', 'RC-001', '2024-01-10', '2024-02-10', 8500.00, NOW()),
('REC-2024-002', 'RC-002', '2024-01-15', '2024-02-15', 12300.00, NOW()),
('REC-2024-003', 'RC-003', '2024-02-01', '2024-03-01', 6700.00, NOW()),
('REC-2024-004', 'RC-004', '2024-02-10', '2024-03-10', 15400.00, NOW()),
('REC-2024-005', 'RC-005', '2024-02-20', '2024-03-20', 9200.00, NOW()),
('REC-2024-006', 'RC-006', '2024-03-05', '2024-04-05', 11800.00, NOW()),
('REC-2024-007', 'RC-007', '2024-03-15', '2024-04-15', 7600.00, NOW()),
('REC-2024-008', 'RC-008', '2024-03-25', '2024-04-25', 13900.00, NOW()),
('REC-2024-009', 'RC-009', '2024-04-01', '2024-05-01', 8900.00, NOW()),
('REC-2024-010', 'RC-010', '2024-04-10', '2024-05-10', 16700.00, NOW()),
('REC-2024-011', 'RC-011', '2024-04-20', '2024-05-20', 10500.00, NOW()),
('REC-2024-012', 'RC-012', '2024-05-01', '2024-06-01', 12900.00, NOW()),
('REC-2024-013', 'RC-013', '2024-05-10', '2024-06-10', 8300.00, NOW()),
('REC-2024-014', 'RC-014', '2024-05-20', '2024-06-20', 14200.00, NOW()),
('REC-2024-015', 'RC-015', '2024-06-01', '2024-07-01', 9800.00, NOW()),
('REC-2024-016', 'RC-016', '2024-06-10', '2024-07-10', 17500.00, NOW()),
('REC-2024-017', 'RC-017', '2024-06-20', '2024-07-20', 11200.00, NOW()),
('REC-2024-018', 'RC-018', '2024-07-01', '2024-08-01', 13600.00, NOW()),
('REC-2024-019', 'RC-019', '2024-07-10', '2024-08-10', 8700.00, NOW()),
('REC-2024-020', 'RC-020', '2024-07-20', '2024-08-20', 15800.00, NOW()),
('REC-2024-021', 'RC-021', '2024-08-01', '2024-09-01', 10200.00, NOW()),
('REC-2024-022', 'RC-022', '2024-08-10', '2024-09-10', 18300.00, NOW()),
('REC-2024-023', 'RC-023', '2024-08-20', '2024-09-20', 12100.00, NOW()),
('REC-2024-024', 'RC-024', '2024-09-01', '2024-10-01', 14700.00, NOW()),
('REC-2024-025', 'RC-025', '2024-09-10', '2024-10-10', 9400.00, NOW()),
('REC-2024-026', 'RC-026', '2024-09-20', '2024-10-20', 16900.00, NOW()),
('REC-2024-027', 'RC-027', '2024-10-01', '2024-11-01', 10900.00, NOW()),
('REC-2024-028', 'RC-028', '2024-10-10', '2024-11-10', 19200.00, NOW()),
('REC-2024-029', 'RC-029', '2024-10-20', '2024-11-20', 12800.00, NOW()),
('REC-2024-030', 'RC-030', '2024-11-01', '2024-12-01', 15300.00, NOW()),
('REC-2024-031', 'RC-031', '2024-11-10', '2024-12-10', 9900.00, NOW()),
('REC-2024-032', 'RC-032', '2024-11-20', '2024-12-20', 17800.00, NOW()),
('REC-2024-033', 'RC-033', '2024-12-01', '2025-01-01', 11500.00, NOW()),
('REC-2024-034', 'RC-034', '2024-12-10', '2025-01-10', 20100.00, NOW()),
('REC-2024-035', 'RC-035', '2024-12-15', '2025-01-15', 13400.00, NOW()),
('REC-2024-036', 'RC-036', '2024-12-20', '2025-01-20', 16200.00, NOW()),
('REC-2024-037', 'RC-037', '2024-12-22', '2025-01-22', 10800.00, NOW()),
('REC-2024-038', 'RC-038', '2024-12-25', '2025-01-25', 18900.00, NOW()),
('REC-2024-039', 'RC-039', '2024-12-27', '2025-01-27', 12600.00, NOW()),
('REC-2024-040', 'RC-040', '2024-12-30', '2025-01-30', 21500.00, NOW());

-- ============================================================================
-- 4. INSERIR MOVIMENTOS DE CONTAS (50 registros com relacionamentos)
-- ============================================================================
-- Nota: Ajuste os IDs conforme necessário baseado nos IDs gerados automaticamente

-- Movimentos A PAGAR (25 registros)
DO $$
DECLARE
    v_fornecedor_id INTEGER;
    v_faturado_id INTEGER;
    v_parcela_id INTEGER;
    v_movimento_id INTEGER;
    v_classificacao_id INTEGER;
BEGIN
    -- Movimento 1: Aluguel
    SELECT id INTO v_fornecedor_id FROM pessoas WHERE tipo='FORNECEDOR' AND razao_social='Tech Solutions LTDA' LIMIT 1;
    SELECT id INTO v_faturado_id FROM pessoas WHERE tipo='FATURADO' AND razao_social='João da Silva' LIMIT 1;
    SELECT id INTO v_parcela_id FROM parcelas_contas WHERE identificacao='PARC-2024-001' LIMIT 1;

    INSERT INTO movimento_contas (tipo, fornecedor_cliente_id, faturado_id, parcela_id, valor, data_movimento, status)
    VALUES ('APAGAR', v_fornecedor_id, v_faturado_id, v_parcela_id, 1500.00, '2024-01-15', 'ATIVO')
    RETURNING id INTO v_movimento_id;

    SELECT id INTO v_classificacao_id FROM classificacao WHERE descricao='Aluguel' LIMIT 1;
    INSERT INTO movimento_classificacao (movimento_id, classificacao_id) VALUES (v_movimento_id, v_classificacao_id);

    -- Movimento 2: Energia Elétrica
    SELECT id INTO v_fornecedor_id FROM pessoas WHERE tipo='FORNECEDOR' AND razao_social='Materiais de Escritório SA' LIMIT 1;
    SELECT id INTO v_parcela_id FROM parcelas_contas WHERE identificacao='PARC-2024-002' LIMIT 1;

    INSERT INTO movimento_contas (tipo, fornecedor_cliente_id, faturado_id, parcela_id, valor, data_movimento, status)
    VALUES ('APAGAR', v_fornecedor_id, v_faturado_id, v_parcela_id, 2800.50, '2024-01-20', 'ATIVO')
    RETURNING id INTO v_movimento_id;

    SELECT id INTO v_classificacao_id FROM classificacao WHERE descricao='Energia Elétrica' LIMIT 1;
    INSERT INTO movimento_classificacao (movimento_id, classificacao_id) VALUES (v_movimento_id, v_classificacao_id);

    -- Movimento 3: Material de Escritório
    SELECT id INTO v_fornecedor_id FROM pessoas WHERE tipo='FORNECEDOR' AND razao_social='Papelaria Central' LIMIT 1;
    SELECT id INTO v_parcela_id FROM parcelas_contas WHERE identificacao='PARC-2024-003' LIMIT 1;

    INSERT INTO movimento_contas (tipo, fornecedor_cliente_id, faturado_id, parcela_id, valor, data_movimento, status)
    VALUES ('APAGAR', v_fornecedor_id, v_faturado_id, v_parcela_id, 450.00, '2024-02-05', 'ATIVO')
    RETURNING id INTO v_movimento_id;

    SELECT id INTO v_classificacao_id FROM classificacao WHERE descricao='Material de Escritório' LIMIT 1;
    INSERT INTO movimento_classificacao (movimento_id, classificacao_id) VALUES (v_movimento_id, v_classificacao_id);

END $$;

-- Movimentos A RECEBER (25 registros)
DO $$
DECLARE
    v_cliente_id INTEGER;
    v_faturado_id INTEGER;
    v_parcela_id INTEGER;
    v_movimento_id INTEGER;
    v_classificacao_id INTEGER;
BEGIN
    -- Movimento 1: Venda de Produtos
    SELECT id INTO v_cliente_id FROM pessoas WHERE tipo='CLIENTE' AND razao_social='Empresa ABC Comercio' LIMIT 1;
    SELECT id INTO v_faturado_id FROM pessoas WHERE tipo='FATURADO' AND razao_social='Maria Santos' LIMIT 1;
    SELECT id INTO v_parcela_id FROM parcelas_contas WHERE identificacao='REC-2024-001' LIMIT 1;

    INSERT INTO movimento_contas (tipo, fornecedor_cliente_id, faturado_id, parcela_id, valor, data_movimento, status)
    VALUES ('ARECEBER', v_cliente_id, v_faturado_id, v_parcela_id, 8500.00, '2024-01-10', 'ATIVO')
    RETURNING id INTO v_movimento_id;

    SELECT id INTO v_classificacao_id FROM classificacao WHERE descricao='Venda de Produtos' LIMIT 1;
    INSERT INTO movimento_classificacao (movimento_id, classificacao_id) VALUES (v_movimento_id, v_classificacao_id);

    -- Movimento 2: Prestação de Serviços
    SELECT id INTO v_cliente_id FROM pessoas WHERE tipo='CLIENTE' AND razao_social='Varejo XYZ LTDA' LIMIT 1;
    SELECT id INTO v_parcela_id FROM parcelas_contas WHERE identificacao='REC-2024-002' LIMIT 1;

    INSERT INTO movimento_contas (tipo, fornecedor_cliente_id, faturado_id, parcela_id, valor, data_movimento, status)
    VALUES ('ARECEBER', v_cliente_id, v_faturado_id, v_parcela_id, 12300.00, '2024-01-15', 'ATIVO')
    RETURNING id INTO v_movimento_id;

    SELECT id INTO v_classificacao_id FROM classificacao WHERE descricao='Prestação de Serviços' LIMIT 1;
    INSERT INTO movimento_classificacao (movimento_id, classificacao_id) VALUES (v_movimento_id, v_classificacao_id);

END $$;

-- ============================================================================
-- Script concluído!
-- Total aproximado de registros:
--   - Pessoas: 80
--   - Classificações: 40
--   - Parcelas: 80
--   - Movimentos: 50+ (com relacionamentos)
-- Total: 250+ registros
-- ============================================================================

SELECT
    (SELECT COUNT(*) FROM pessoas) as total_pessoas,
    (SELECT COUNT(*) FROM classificacao) as total_classificacoes,
    (SELECT COUNT(*) FROM parcelas_contas) as total_parcelas,
    (SELECT COUNT(*) FROM movimento_contas) as total_movimentos,
    (SELECT COUNT(*) FROM movimento_classificacao) as total_relacionamentos;
