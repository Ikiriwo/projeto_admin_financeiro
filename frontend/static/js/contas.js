// Variáveis globais
let movimentosData = [];
let ordemAscendente = true;
let pessoas = [];
let classificacoes = [];

// Carregar dados auxiliares (pessoas e classificações)
async function carregarDadosAuxiliares() {
    try {
        const [resPessoas, resClassificacoes] = await Promise.all([
            fetch('/api/pessoas?incluir_inativos=false'),
            fetch('/api/classificacoes?incluir_inativos=false')
        ]);

        const resultPessoas = await resPessoas.json();
        const resultClassificacoes = await resClassificacoes.json();

        if (resultPessoas.success) {
            pessoas = resultPessoas.data;
        }

        if (resultClassificacoes.success) {
            classificacoes = resultClassificacoes.data;
        }
    } catch (error) {
        console.error('Erro ao carregar dados auxiliares:', error);
    }
}

// Carregar todos os registros ATIVOS
function carregarTodos() {
    const incluirInativos = document.getElementById('incluirInativos').checked;
    const url = `/api/movimentos?incluir_inativos=${incluirInativos}`;

    fetch(url)
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                movimentosData = result.data;
                renderizarTabela(movimentosData);
                atualizarContador(movimentosData.length);
            } else {
                alert('Erro ao carregar movimentos: ' + result.error);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao carregar movimentos');
        });
}

// Buscar com filtros
function carregarMovimentos() {
    const tipo = document.getElementById('filtroTipo').value;
    const idMin = document.getElementById('filtroIdMin').value;
    const incluirInativos = document.getElementById('incluirInativos').checked;

    const url = `/api/movimentos?tipo=${tipo}&incluir_inativos=${incluirInativos}`;

    fetch(url)
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                let dados = result.data;

                // Filtrar por ID mínimo
                if (idMin) {
                    dados = dados.filter(m => m.id >= parseInt(idMin));
                }

                movimentosData = dados;
                renderizarTabela(movimentosData);
                atualizarContador(movimentosData.length);
            } else {
                alert('Erro ao buscar movimentos: ' + result.error);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao buscar movimentos');
        });
}

// Renderizar tabela
function renderizarTabela(dados) {
    const tbody = document.getElementById('tbodyMovimentos');

    if (dados.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="8" class="text-center text-muted">
                    <i class="fas fa-inbox"></i> Nenhum registro encontrado
                </td>
            </tr>
        `;
        return;
    }

    tbody.innerHTML = dados.map(movimento => `
        <tr>
            <td>${movimento.id}</td>
            <td>
                <span class="badge badge-${movimento.tipo === 'APAGAR' ? 'danger' : 'success'}">
                    ${movimento.tipo}
                </span>
            </td>
            <td>${movimento.fornecedor_cliente_nome || 'N/A'}</td>
            <td>${movimento.faturado_nome || 'N/A'}</td>
            <td>R$ ${parseFloat(movimento.valor).toFixed(2)}</td>
            <td>
                <span class="badge badge-${movimento.status === 'ATIVO' ? 'success' : 'danger'}">
                    ${movimento.status}
                </span>
            </td>
            <td>${formatarData(movimento.data_movimento)}</td>
            <td>
                <div class="btn-group btn-group-sm">
                    <button class="btn btn-info" onclick="verDetalhes(${movimento.id})" title="Ver Detalhes">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn btn-warning" onclick="abrirModalEditar(${movimento.id})" title="Editar">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-danger" onclick="excluirMovimento(${movimento.id})" title="Excluir"
                            ${movimento.status === 'INATIVO' ? 'disabled' : ''}>
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

// Ordenar tabela por coluna
function ordenarTabela(coluna) {
    const campos = ['id', 'tipo', 'fornecedor_cliente_nome', 'faturado_nome', 'valor', 'status', 'data_movimento'];
    const campo = campos[coluna];

    movimentosData.sort((a, b) => {
        let valorA = a[campo] || '';
        let valorB = b[campo] || '';

        if (campo === 'id' || campo === 'valor') {
            return ordemAscendente ? valorA - valorB : valorB - valorA;
        }

        if (valorA < valorB) return ordemAscendente ? -1 : 1;
        if (valorA > valorB) return ordemAscendente ? 1 : -1;
        return 0;
    });

    ordemAscendente = !ordemAscendente;
    renderizarTabela(movimentosData);
}

// Abrir modal para criar
async function abrirModalCriar() {
    await carregarDadosAuxiliares();

    document.getElementById('modalTitulo').textContent = 'Novo Movimento';
    document.getElementById('formMovimento').reset();
    document.getElementById('movimentoId').value = '';
    document.getElementById('movimentoStatus').value = 'ATIVO';

    popularSelectPessoas();
    popularCheckboxesClassificacoes([]);

    $('#modalMovimento').modal('show');
}

// Abrir modal para editar
async function abrirModalEditar(id) {
    await carregarDadosAuxiliares();

    fetch(`/api/movimentos/${id}`)
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                const movimento = result.data;
                document.getElementById('modalTitulo').textContent = 'Editar Movimento';
                document.getElementById('movimentoId').value = movimento.id;
                document.getElementById('movimentoTipo').value = movimento.tipo;
                document.getElementById('movimentoValor').value = movimento.valor;
                document.getElementById('movimentoStatus').value = movimento.status;

                popularSelectPessoas();
                document.getElementById('movimentoFornecedorCliente').value = movimento.fornecedor_cliente_id;
                document.getElementById('movimentoFaturado').value = movimento.faturado_id;

                const classificacaoIds = movimento.classificacoes.map(c => c.id);
                popularCheckboxesClassificacoes(classificacaoIds);

                $('#modalMovimento').modal('show');
            } else {
                alert('Erro ao carregar movimento: ' + result.error);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao carregar movimento');
        });
}

// Popular select de pessoas
function popularSelectPessoas() {
    const selectFornecedor = document.getElementById('movimentoFornecedorCliente');
    const selectFaturado = document.getElementById('movimentoFaturado');

    const fornecedoresClientes = pessoas.filter(p =>
        p.tipo === 'FORNECEDOR' || p.tipo === 'CLIENTE' || p.tipo === 'CLIENTE-FORNECEDOR'
    );
    const faturados = pessoas.filter(p => p.tipo === 'FATURADO' || p.tipo === 'CLIENTE-FORNECEDOR');

    selectFornecedor.innerHTML = '<option value="">Selecione...</option>' +
        fornecedoresClientes.map(p => `<option value="${p.id}">${p.razao_social} (${p.cpf_cnpj})</option>`).join('');

    selectFaturado.innerHTML = '<option value="">Selecione...</option>' +
        faturados.map(p => `<option value="${p.id}">${p.razao_social} (${p.cpf_cnpj})</option>`).join('');
}

// Popular checkboxes de classificações
function popularCheckboxesClassificacoes(classificacaoIdsSelecionadas) {
    const container = document.getElementById('classificacoesCheckboxes');

    if (classificacoes.length === 0) {
        container.innerHTML = '<p class="text-muted">Nenhuma classificação disponível</p>';
        return;
    }

    container.innerHTML = classificacoes.map(c => `
        <div class="form-check">
            <input class="form-check-input" type="checkbox" value="${c.id}" id="class_${c.id}"
                   ${classificacaoIdsSelecionadas.includes(c.id) ? 'checked' : ''}>
            <label class="form-check-label" for="class_${c.id}">
                <span class="badge badge-${c.tipo === 'RECEITA' ? 'success' : 'warning'}">${c.tipo}</span>
                ${c.descricao}
            </label>
        </div>
    `).join('');
}

// Salvar movimento (criar ou atualizar)
function salvarMovimento() {
    const id = document.getElementById('movimentoId').value;
    const tipo = document.getElementById('movimentoTipo').value;
    const valor = document.getElementById('movimentoValor').value;
    const fornecedorClienteId = document.getElementById('movimentoFornecedorCliente').value;
    const faturadoId = document.getElementById('movimentoFaturado').value;

    if (!tipo || !valor || !fornecedorClienteId || !faturadoId) {
        alert('Preencha todos os campos obrigatórios');
        return;
    }

    // Obter classificações selecionadas
    const classificacaoIds = [];
    const checkboxes = document.querySelectorAll('#classificacoesCheckboxes input[type="checkbox"]:checked');
    checkboxes.forEach(cb => classificacaoIds.push(parseInt(cb.value)));

    const dados = {
        tipo: tipo,
        valor: parseFloat(valor),
        fornecedor_cliente_id: parseInt(fornecedorClienteId),
        faturado_id: parseInt(faturadoId),
        classificacao_ids: classificacaoIds
    };

    const url = id ? `/api/movimentos/${id}` : '/api/movimentos';
    const metodo = id ? 'PUT' : 'POST';

    fetch(url, {
        method: metodo,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dados)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            alert(result.message);
            $('#modalMovimento').modal('hide');
            carregarTodos();
        } else {
            alert('Erro: ' + result.error);
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao salvar movimento');
    });
}

// Excluir movimento (exclusão lógica)
function excluirMovimento(id) {
    if (!confirm('Deseja realmente excluir este movimento? (Exclusão lógica)')) {
        return;
    }

    fetch(`/api/movimentos/${id}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            alert(result.message);
            carregarTodos();
        } else {
            alert('Erro: ' + result.error);
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao excluir movimento');
    });
}

// Ver detalhes do movimento
function verDetalhes(id) {
    fetch(`/api/movimentos/${id}`)
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                const m = result.data;
                const classificacoesTexto = m.classificacoes.map(c =>
                    `${c.tipo}: ${c.descricao}`
                ).join('\n');

                alert(`DETALHES DO MOVIMENTO\n\n` +
                      `ID: ${m.id}\n` +
                      `Tipo: ${m.tipo}\n` +
                      `Fornecedor/Cliente: ${m.fornecedor_cliente_nome}\n` +
                      `Faturado: ${m.faturado_nome}\n` +
                      `Valor: R$ ${parseFloat(m.valor).toFixed(2)}\n` +
                      `Status: ${m.status}\n` +
                      `Data: ${formatarData(m.data_movimento)}\n\n` +
                      `Classificações:\n${classificacoesTexto || 'Nenhuma'}`
                );
            } else {
                alert('Erro ao carregar detalhes: ' + result.error);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao carregar detalhes');
        });
}

// Formatar data
function formatarData(dataISO) {
    if (!dataISO) return '';
    const data = new Date(dataISO);
    return data.toLocaleDateString('pt-BR') + ' ' + data.toLocaleTimeString('pt-BR');
}

// Atualizar contador de registros
function atualizarContador(total) {
    document.getElementById('contadorRegistros').textContent = `${total} registro(s) encontrado(s)`;
}

// Carregar dados auxiliares ao carregar a página
document.addEventListener('DOMContentLoaded', carregarDadosAuxiliares);
