// Funções para validação e cadastro de dados da nota fiscal

// Validar dados no banco de dados
function validarDados(dadosExtraidos) {
    // Atualizar status para "Verificando..."
    document.getElementById('status-fornecedor').textContent = "Verificando...";
    document.getElementById('status-fornecedor').className = "status-badge status-verificando";
    
    document.getElementById('status-faturado').textContent = "Verificando...";
    document.getElementById('status-faturado').className = "status-badge status-verificando";
    
    document.getElementById('status-classificacao').textContent = "Verificando...";
    document.getElementById('status-classificacao').className = "status-badge status-verificando";
    
    // Fazer requisição para API de validação
    fetch('/api/validar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dadosExtraidos)
    })
    .then(response => response.json())
    .then(data => {
        // Atualizar status do fornecedor
        if (data.fornecedor.existe) {
            document.getElementById('status-fornecedor').textContent = "Cadastrado";
            document.getElementById('status-fornecedor').className = "status-badge status-ok";
            document.getElementById('id-fornecedor').textContent = data.fornecedor.id;
            document.getElementById('resumo-id-fornecedor').textContent = dadosExtraidos.Fornecedor.Razao_Social + " (ID: " + data.fornecedor.id + ")";
        } else {
            document.getElementById('status-fornecedor').textContent = "Não Cadastrado";
            document.getElementById('status-fornecedor').className = "status-badge status-pendente";
            document.getElementById('btn-cadastrar-fornecedor').style.display = "block";
        }
        
        // Atualizar status do faturado
        if (data.faturado.existe) {
            document.getElementById('status-faturado').textContent = "Cadastrado";
            document.getElementById('status-faturado').className = "status-badge status-ok";
            document.getElementById('id-faturado').textContent = data.faturado.id;
            document.getElementById('resumo-id-faturado').textContent = dadosExtraidos.Faturado.Nome + " (ID: " + data.faturado.id + ")";
        } else {
            document.getElementById('status-faturado').textContent = "Não Cadastrado";
            document.getElementById('status-faturado').className = "status-badge status-pendente";
            document.getElementById('btn-cadastrar-faturado').style.display = "block";
        }
        
        // Atualizar status da classificação
        if (data.classificacao.existe) {
            document.getElementById('status-classificacao').textContent = "Cadastrado";
            document.getElementById('status-classificacao').className = "status-badge status-ok";
            document.getElementById('id-classificacao').textContent = data.classificacao.id;
            document.getElementById('resumo-id-classificacao').textContent = dadosExtraidos.Classificacao_Despesa + " (ID: " + data.classificacao.id + ")";
        } else {
            document.getElementById('status-classificacao').textContent = "Não Cadastrado";
            document.getElementById('status-classificacao').className = "status-badge status-pendente";
            document.getElementById('btn-cadastrar-classificacao').style.display = "block";
        }
        
        // Verificar se todos os itens estão cadastrados para habilitar o botão de confirmar
        verificarBotaoConfirmar();
    })
    .catch(error => {
        console.error('Erro ao validar dados:', error);
        document.getElementById('feedback-validacao').textContent = "Erro ao validar dados: " + error.message;
        document.getElementById('feedback-validacao').className = "feedback-text erro";
    });
}

// Cadastrar fornecedor
function cadastrarFornecedor(dadosExtraidos) {
    document.getElementById('btn-cadastrar-fornecedor').disabled = true;
    document.getElementById('btn-cadastrar-fornecedor').textContent = "Cadastrando...";
    
    fetch('/api/cadastrar/fornecedor', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dadosExtraidos)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('status-fornecedor').textContent = "Cadastrado";
            document.getElementById('status-fornecedor').className = "status-badge status-ok";
            document.getElementById('id-fornecedor').textContent = data.id;
            document.getElementById('resumo-id-fornecedor').textContent = dadosExtraidos.Fornecedor.Razao_Social + " (ID: " + data.id + ")";
            document.getElementById('btn-cadastrar-fornecedor').style.display = "none";
            
            // Verificar se todos os itens estão cadastrados
            verificarBotaoConfirmar();
        } else {
            throw new Error("Falha ao cadastrar fornecedor");
        }
    })
    .catch(error => {
        console.error('Erro ao cadastrar fornecedor:', error);
        document.getElementById('btn-cadastrar-fornecedor').disabled = false;
        document.getElementById('btn-cadastrar-fornecedor').textContent = "Tentar Novamente";
    });
}

// Cadastrar faturado
function cadastrarFaturado(dadosExtraidos) {
    document.getElementById('btn-cadastrar-faturado').disabled = true;
    document.getElementById('btn-cadastrar-faturado').textContent = "Cadastrando...";
    
    fetch('/api/cadastrar/faturado', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dadosExtraidos)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('status-faturado').textContent = "Cadastrado";
            document.getElementById('status-faturado').className = "status-badge status-ok";
            document.getElementById('id-faturado').textContent = data.id;
            document.getElementById('resumo-id-faturado').textContent = dadosExtraidos.Faturado.Nome + " (ID: " + data.id + ")";
            document.getElementById('btn-cadastrar-faturado').style.display = "none";
            
            // Verificar se todos os itens estão cadastrados
            verificarBotaoConfirmar();
        } else {
            throw new Error("Falha ao cadastrar faturado");
        }
    })
    .catch(error => {
        console.error('Erro ao cadastrar faturado:', error);
        document.getElementById('btn-cadastrar-faturado').disabled = false;
        document.getElementById('btn-cadastrar-faturado').textContent = "Tentar Novamente";
    });
}

// Cadastrar classificação
function cadastrarClassificacao(dadosExtraidos) {
    document.getElementById('btn-cadastrar-classificacao').disabled = true;
    document.getElementById('btn-cadastrar-classificacao').textContent = "Cadastrando...";
    
    fetch('/api/cadastrar/classificacao', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dadosExtraidos)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('status-classificacao').textContent = "Cadastrado";
            document.getElementById('status-classificacao').className = "status-badge status-ok";
            document.getElementById('id-classificacao').textContent = data.id;
            document.getElementById('resumo-id-classificacao').textContent = dadosExtraidos.Classificacao_Despesa + " (ID: " + data.id + ")";
            document.getElementById('btn-cadastrar-classificacao').style.display = "none";
            
            // Verificar se todos os itens estão cadastrados
            verificarBotaoConfirmar();
        } else {
            throw new Error("Falha ao cadastrar classificação");
        }
    })
    .catch(error => {
        console.error('Erro ao cadastrar classificação:', error);
        document.getElementById('btn-cadastrar-classificacao').disabled = false;
        document.getElementById('btn-cadastrar-classificacao').textContent = "Tentar Novamente";
    });
}

// Verificar se todos os itens estão cadastrados para habilitar o botão de confirmar
function verificarBotaoConfirmar() {
    const idFornecedor = document.getElementById('id-fornecedor').textContent;
    const idFaturado = document.getElementById('id-faturado').textContent;
    const idClassificacao = document.getElementById('id-classificacao').textContent;
    
    if (idFornecedor !== "—" && idFaturado !== "—" && idClassificacao !== "—") {
        document.getElementById('btn-confirmar').disabled = false;
    }
}

// Confirmar lançamento
function confirmarLancamento(dadosExtraidos) {
    document.getElementById('btn-confirmar').disabled = true;
    document.getElementById('btn-confirmar').textContent = "Processando...";
    
    // Preparar dados para envio
    const dadosLancamento = {
        ...dadosExtraidos,
        fornecedor_id: document.getElementById('id-fornecedor').textContent,
        faturado_id: document.getElementById('id-faturado').textContent,
        classificacao_id: document.getElementById('id-classificacao').textContent
    };
    
    fetch('/api/lancar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dadosLancamento)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('feedback-lancamento').textContent = "Nota fiscal processada com sucesso!";
            document.getElementById('feedback-lancamento').className = "feedback-text sucesso";
            document.getElementById('btn-confirmar').textContent = "✅ Lançamento Concluído";
            document.getElementById('btn-confirmar').className = "btn-primary concluido";
        } else {
            throw new Error(data.message || "Erro ao processar nota fiscal");
        }
    })
    .catch(error => {
        console.error('Erro ao confirmar lançamento:', error);
        document.getElementById('feedback-lancamento').textContent = "Erro ao processar nota fiscal: " + error.message;
        document.getElementById('feedback-lancamento').className = "feedback-text erro";
        document.getElementById('btn-confirmar').disabled = false;
        document.getElementById('btn-confirmar').textContent = "Tentar Novamente";
    });
}