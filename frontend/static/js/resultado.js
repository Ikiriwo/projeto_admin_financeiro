/**
 * Script para a página de resultados da extração de nota fiscal
 */

// Funções para alternar entre abas
function showTab(tabId) {
    // Esconde todos os conteúdos de abas
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // Remove a classe active de todos os botões
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Mostra o conteúdo da aba selecionada
    document.getElementById(tabId).classList.add('active');

    // Adiciona a classe active ao botão clicado
    event.target.classList.add('active');
}

// Função para copiar JSON
function copyJson() {
    const jsonText = document.querySelector('.json-code').textContent;
    navigator.clipboard.writeText(jsonText)
        .then(() => {
            alert('JSON copiado para a área de transferência!');
        })
        .catch(err => {
            console.error('Erro ao copiar: ', err);
        });
}

// Inicialização quando a página carrega
document.addEventListener('DOMContentLoaded', function() {
    // Mostrar seções
    document.getElementById('validacao-section').style.display = 'block';
    document.getElementById('itens-section').style.display = 'block';
    document.getElementById('resumo-section').style.display = 'block';

    // Iniciar validação explicitamente
    if (typeof validarDados === 'function') {
        validarDados(window.dadosExtraidos);
    } else {
        console.error('Função validarDados não encontrada');
    }

    // Event listeners para botões de cadastro
    document.getElementById('btn-cadastrar-fornecedor').addEventListener('click', function() {
        if (window.cadastrarFornecedor) {
            window.cadastrarFornecedor(window.dadosExtraidos);
        }
    });

    document.getElementById('btn-cadastrar-faturado').addEventListener('click', function() {
        if (window.cadastrarFaturado) {
            window.cadastrarFaturado(window.dadosExtraidos);
        }
    });

    document.getElementById('btn-cadastrar-classificacao').addEventListener('click', function() {
        if (window.cadastrarClassificacao) {
            window.cadastrarClassificacao(window.dadosExtraidos);
        }
    });

    document.getElementById('btn-confirmar').addEventListener('click', function() {
        if (window.confirmarLancamento) {
            window.confirmarLancamento(window.dadosExtraidos);
        }
    });
});
