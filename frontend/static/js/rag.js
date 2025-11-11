/**
 * Sistema RAG - Interface JavaScript
 * Gerencia a interface de perguntas e respostas usando RAG
 */

// Estado da aplicação
const state = {
    currentMethod: 'simple',
    isLoading: false,
    examples: []
};

// Elementos do DOM
const elements = {
    questionInput: null,
    askButton: null,
    responseSection: null,
    responseContent: null,
    responseMethod: null,
    responseMetadata: null,
    metadataContent: null,
    loadingIndicator: null,
    errorSection: null,
    errorMessage: null,
    examplesList: null,
    methodRadios: null,
    statusValue: null,
    indexedCount: null,
    indexButton: null,
    embeddingsRadio: null
};

/**
 * Inicializa a aplicação quando o DOM estiver carregado
 */
document.addEventListener('DOMContentLoaded', function() {
    initElements();
    initEventListeners();
    loadStatus();
    loadExamples();
});

/**
 * Inicializa as referências dos elementos do DOM
 */
function initElements() {
    elements.questionInput = document.getElementById('questionInput');
    elements.askButton = document.getElementById('askButton');
    elements.responseSection = document.getElementById('responseSection');
    elements.responseContent = document.getElementById('responseContent');
    elements.responseMethod = document.getElementById('responseMethod');
    elements.responseMetadata = document.getElementById('responseMetadata');
    elements.metadataContent = document.getElementById('metadataContent');
    elements.loadingIndicator = document.getElementById('loadingIndicator');
    elements.errorSection = document.getElementById('errorSection');
    elements.errorMessage = document.getElementById('errorMessage');
    elements.examplesList = document.getElementById('examplesList');
    elements.methodRadios = document.querySelectorAll('input[name="method"]');
    elements.statusValue = document.getElementById('statusValue');
    elements.indexedCount = document.getElementById('indexedCount');
    elements.indexButton = document.getElementById('indexButton');
    elements.embeddingsRadio = document.getElementById('embeddingsRadio');
}

/**
 * Inicializa os event listeners
 */
function initEventListeners() {
    // Botão de perguntar
    elements.askButton.addEventListener('click', handleAskQuestion);

    // Enter no textarea
    elements.questionInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && e.ctrlKey) {
            handleAskQuestion();
        }
    });

    // Mudança de método
    elements.methodRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            state.currentMethod = this.value;
            console.log('Método selecionado:', state.currentMethod);
        });
    });

    // Botão de indexar
    if (elements.indexButton) {
        elements.indexButton.addEventListener('click', handleIndexDocuments);
    }
}

/**
 * Carrega os exemplos de perguntas da API
 */
async function loadExamples() {
    try {
        const response = await fetch('/api/rag/examples');
        const data = await response.json();

        if (data.success && data.examples) {
            state.examples = data.examples;
            renderExamples();
        } else {
            elements.examplesList.innerHTML = '<p class="error">Erro ao carregar exemplos</p>';
        }
    } catch (error) {
        console.error('Erro ao carregar exemplos:', error);
        elements.examplesList.innerHTML = '<p class="error">Erro ao carregar exemplos</p>';
    }
}

/**
 * Renderiza os exemplos na interface
 */
function renderExamples() {
    if (state.examples.length === 0) {
        elements.examplesList.innerHTML = '<p>Nenhum exemplo disponível</p>';
        return;
    }

    elements.examplesList.innerHTML = '';

    state.examples.forEach(example => {
        const exampleDiv = document.createElement('div');
        exampleDiv.className = 'example-item';
        exampleDiv.textContent = example;
        exampleDiv.addEventListener('click', () => {
            elements.questionInput.value = example;
            elements.questionInput.focus();
        });
        elements.examplesList.appendChild(exampleDiv);
    });
}

/**
 * Handler para o botão de perguntar
 */
async function handleAskQuestion() {
    const question = elements.questionInput.value.trim();

    if (!question) {
        showError('Por favor, digite uma pergunta');
        return;
    }

    if (state.isLoading) {
        return;
    }

    // Esconde seções anteriores
    hideError();
    hideResponse();

    // Mostra loading
    showLoading();

    try {
        const response = await fetch('/api/rag/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: question,
                method: state.currentMethod
            })
        });

        const data = await response.json();

        hideLoading();

        if (data.success) {
            showResponse(data);
        } else {
            showError(data.error || 'Erro ao processar pergunta');
        }
    } catch (error) {
        hideLoading();
        console.error('Erro ao fazer pergunta:', error);
        showError('Erro de conexão com o servidor');
    }
}

/**
 * Mostra o indicador de loading
 */
function showLoading() {
    state.isLoading = true;
    elements.loadingIndicator.style.display = 'block';
    elements.askButton.disabled = true;
}

/**
 * Esconde o indicador de loading
 */
function hideLoading() {
    state.isLoading = false;
    elements.loadingIndicator.style.display = 'none';
    elements.askButton.disabled = false;
}

/**
 * Mostra a resposta na interface
 */
function showResponse(data) {
    elements.responseSection.style.display = 'block';

    // Método usado
    const methodLabel = data.method === 'RAG_SIMPLE' ? 'RAG Simples' : 'RAG Embeddings';
    elements.responseMethod.textContent = methodLabel;

    // Resposta
    elements.responseContent.textContent = data.answer;

    // Metadados (se houver)
    if (data.data_retrieved) {
        elements.responseMetadata.style.display = 'block';
        elements.metadataContent.textContent = JSON.stringify({
            query_type: data.query_type,
            method: data.method,
            data_retrieved: data.data_retrieved
        }, null, 2);
    } else {
        elements.responseMetadata.style.display = 'none';
    }

    // Scroll para a resposta
    elements.responseSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Esconde a seção de resposta
 */
function hideResponse() {
    elements.responseSection.style.display = 'none';
}

/**
 * Mostra uma mensagem de erro
 */
function showError(message) {
    elements.errorMessage.textContent = message;
    elements.errorSection.style.display = 'flex';

    // Auto-hide após 5 segundos
    setTimeout(() => {
        hideError();
    }, 5000);
}

/**
 * Esconde a mensagem de erro
 */
function hideError() {
    elements.errorSection.style.display = 'none';
}

/**
 * Carrega o status do sistema RAG
 */
async function loadStatus() {
    try {
        const response = await fetch('/api/rag/status');
        const data = await response.json();

        if (data.success) {
            // Atualiza status
            const methods = data.available_methods || [];
            const statusText = methods.length > 0 ? 'Online' : 'Offline';
            elements.statusValue.textContent = statusText;
            elements.statusValue.className = 'status-value ' + (methods.length > 0 ? 'online' : 'offline');

            // Se embeddings está disponível
            if (methods.includes('embeddings')) {
                elements.embeddingsRadio.disabled = false;

                // Mostra contagem de documentos indexados
                if (data.index_status) {
                    elements.indexedCount.textContent =
                        `${data.index_status.total_documents_indexed} / ${data.index_status.total_notas_fiscais}`;

                    // Mostra botão de indexar se necessário
                    if (data.index_status.total_documents_indexed < data.index_status.total_notas_fiscais) {
                        elements.indexButton.style.display = 'block';
                    }
                }
            } else {
                elements.embeddingsRadio.disabled = true;
                elements.indexedCount.textContent = 'N/A';
            }
        }
    } catch (error) {
        console.error('Erro ao carregar status:', error);
        elements.statusValue.textContent = 'Erro';
        elements.statusValue.className = 'status-value offline';
    }
}

/**
 * Handler para indexar documentos
 */
async function handleIndexDocuments() {
    if (!confirm('Deseja indexar todos os documentos? Isso pode levar alguns minutos.')) {
        return;
    }

    elements.indexButton.disabled = true;
    elements.indexButton.textContent = 'Indexando...';

    try {
        const response = await fetch('/api/rag/index', {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            alert(`Indexação concluída!\nTotal: ${data.total_notas}\nIndexados: ${data.indexed}\nFalharam: ${data.failed}`);
            loadStatus(); // Recarrega o status
        } else {
            alert('Erro ao indexar documentos: ' + (data.error || 'Erro desconhecido'));
        }
    } catch (error) {
        console.error('Erro ao indexar:', error);
        alert('Erro de conexão ao indexar documentos');
    } finally {
        elements.indexButton.disabled = false;
        elements.indexButton.textContent = 'Indexar Documentos';
    }
}
