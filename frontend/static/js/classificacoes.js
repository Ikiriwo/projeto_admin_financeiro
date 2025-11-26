// Variáveis globais
let classificacoesData = [];
let ordemAscendente = true;

// Carregar todos os registros ATIVOS
function carregarTodos() {
    const incluirInativos = document.getElementById('incluirInativos').checked;
    const url = `/api/classificacoes?incluir_inativos=${incluirInativos}`;

    fetch(url)
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                classificacoesData = result.data;
                renderizarTabela(classificacoesData);
                atualizarContador(classificacoesData.length);
            } else {
                alert('Erro ao carregar classificações: ' + result.error);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao carregar classificações');
        });
}

// Buscar com filtros
function carregarClassificacoes() {
    const tipo = document.getElementById('filtroTipo').value;
    const busca = document.getElementById('filtroBusca').value.toLowerCase();
    const incluirInativos = document.getElementById('incluirInativos').checked;

    const url = `/api/classificacoes?tipo=${tipo}&incluir_inativos=${incluirInativos}`;

    fetch(url)
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                let dados = result.data;

                // Filtrar por busca local (descrição)
                if (busca) {
                    dados = dados.filter(c =>
                        c.descricao.toLowerCase().includes(busca)
                    );
                }

                classificacoesData = dados;
                renderizarTabela(classificacoesData);
                atualizarContador(classificacoesData.length);
            } else {
                alert('Erro ao buscar classificações: ' + result.error);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao buscar classificações');
        });
}

// Renderizar tabela
function renderizarTabela(dados) {
    const tbody = document.getElementById('tbodyClassificacoes');

    if (dados.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center text-muted">
                    <i class="fas fa-inbox"></i> Nenhum registro encontrado
                </td>
            </tr>
        `;
        return;
    }

    tbody.innerHTML = dados.map(classificacao => `
        <tr>
            <td>${classificacao.id}</td>
            <td>
                <span class="badge badge-${classificacao.tipo === 'RECEITA' ? 'success' : 'warning'}">
                    ${classificacao.tipo}
                </span>
            </td>
            <td>${classificacao.descricao}</td>
            <td>
                <span class="badge badge-${classificacao.status === 'ATIVO' ? 'success' : 'danger'}">
                    ${classificacao.status}
                </span>
            </td>
            <td>${formatarData(classificacao.data_cadastro)}</td>
            <td>
                <div class="btn-group btn-group-sm">
                    <button class="btn btn-warning" onclick="abrirModalEditar(${classificacao.id})" title="Editar">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-danger" onclick="excluirClassificacao(${classificacao.id})" title="Excluir"
                            ${classificacao.status === 'INATIVO' ? 'disabled' : ''}>
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

// Ordenar tabela por coluna
function ordenarTabela(coluna) {
    const campos = ['id', 'tipo', 'descricao', 'status', 'data_cadastro'];
    const campo = campos[coluna];

    classificacoesData.sort((a, b) => {
        let valorA = a[campo];
        let valorB = b[campo];

        if (campo === 'id') {
            return ordemAscendente ? valorA - valorB : valorB - valorA;
        }

        if (valorA < valorB) return ordemAscendente ? -1 : 1;
        if (valorA > valorB) return ordemAscendente ? 1 : -1;
        return 0;
    });

    ordemAscendente = !ordemAscendente;
    renderizarTabela(classificacoesData);
}

// Abrir modal para criar
function abrirModalCriar() {
    document.getElementById('modalTitulo').textContent = 'Nova Classificação';
    document.getElementById('formClassificacao').reset();
    document.getElementById('classificacaoId').value = '';
    document.getElementById('classificacaoStatus').value = 'ATIVO';
    $('#modalClassificacao').modal('show');
}

// Abrir modal para editar
function abrirModalEditar(id) {
    fetch(`/api/classificacoes/${id}`)
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                const classificacao = result.data;
                document.getElementById('modalTitulo').textContent = 'Editar Classificação';
                document.getElementById('classificacaoId').value = classificacao.id;
                document.getElementById('classificacaoTipo').value = classificacao.tipo;
                document.getElementById('classificacaoDescricao').value = classificacao.descricao;
                document.getElementById('classificacaoStatus').value = classificacao.status;
                $('#modalClassificacao').modal('show');
            } else {
                alert('Erro ao carregar classificação: ' + result.error);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao carregar classificação');
        });
}

// Salvar classificação (criar ou atualizar)
function salvarClassificacao() {
    const id = document.getElementById('classificacaoId').value;
    const tipo = document.getElementById('classificacaoTipo').value;
    const descricao = document.getElementById('classificacaoDescricao').value;

    if (!tipo || !descricao) {
        alert('Preencha todos os campos obrigatórios');
        return;
    }

    const dados = {
        tipo: tipo,
        descricao: descricao
    };

    const url = id ? `/api/classificacoes/${id}` : '/api/classificacoes';
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
            $('#modalClassificacao').modal('hide');
            carregarTodos();
        } else {
            alert('Erro: ' + result.error);
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao salvar classificação');
    });
}

// Excluir classificação (exclusão lógica)
function excluirClassificacao(id) {
    if (!confirm('Deseja realmente excluir esta classificação? (Exclusão lógica)')) {
        return;
    }

    fetch(`/api/classificacoes/${id}`, {
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
        alert('Erro ao excluir classificação');
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
